from timezonefinder import TimezoneFinder
from app.src.member import service as member_service
from app.src.attendance.coordinate_validataion import CoordinateValidationStrategy, CoordinateValidationStrategyDefault
from app.src.attendance.time_validation import TimeValidationStrategy, CheckInTimeValidationStrategyDefault, \
    CheckOutTimeValidationStrategyDefault
from app.src.database import db
from app.src.database.collection import Collection
from app.src.database.fake_database import fake_db
from app.src.models.attendance import attendance_model_instance
from geopy.geocoders import Nominatim
from datetime import datetime
import pytz

from app.src.types import attendance_check_type_instance


class AttendanceCheck:
    """AttendanceCheck: 출퇴근 신청 클래스"""

    _instance = None

    def __init__(
            self,
            check_in_time_validation_strategy: TimeValidationStrategy = CheckInTimeValidationStrategyDefault(),
            check_out_time_validation_strategy: TimeValidationStrategy = CheckOutTimeValidationStrategyDefault(),
            coordinate_validation_strategy: CoordinateValidationStrategy = CoordinateValidationStrategyDefault()
    ):
        self.check_in_time_validation_strategy = check_in_time_validation_strategy
        self.check_out_time_validation_strategy = check_out_time_validation_strategy
        self.coordinate_validation_strategy = coordinate_validation_strategy

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AttendanceCheck, cls).__new__(cls)
        return cls._instance

    def attendance_check_in(self, request) -> attendance_check_type_instance:

        # 1. account_id 정보가 DB에 존재하는지 확인
        account_info = member_service.get_user(request.account_id)
        if not account_info:
            raise ValueError("유효한 계정이 아닙니다.")

        # 2. 위경도를 기반으로 구한 날짜 정보(오늘 날짜,연,월,일)
        current_date = self.get_current_date()

        # 3. 이미 출근 정보가 있는지 확인
        existing_attendance = db.find_one(
            collection=Collection.ATTENDANCE,
            query={
                "login_id": request.account_id,
                "date": current_date,
                "check_out_time": None  # 퇴근 기록이 없는 경우
            }
        )

        if existing_attendance:
            raise ValueError("이미 출근한 상태입니다.")

        # 5. 위경도를 기반으로 구한 시각 정보(현재 시각,시,분,초)이 근무 시작 예정 시간보다 0~30분 이전인지 확인
        current_time = datetime.strptime(
            self.get_current_time(request.coordinate.latitude, request.coordinate.longitude),
            "%H:%M:%S", )
        work_start_time = datetime.strptime(account_info["work_start_time"], "%H:%M:%S", )
        if self.check_in_time_validation_strategy.is_valid(current_time, work_start_time):
            raise ValueError("출근 시간이 유효하지 않습니다.")

        # 6. coordinate가 회사 위경도 정보에서 오차 범위 이내인지 확인
        company_coordinates = account_info["company_coordinates"]
        if not self.coordinate_validation_strategy.is_within_error_range(company_coordinates, request.coordinate):
            raise ValueError("유효한 위치가 아닙니다.")
        new_attendance: attendance_model_instance = {
            "login_id": request.account_id,
            "check_in_time": current_time,
            "check_in_location": {
                "latitude": request.coordinate.latitude,
                "logitude": request.coordinate
            },
            "check_out_time": None,  # 퇴근 시간은 아직 없음
            "check_out_location": None  # 퇴근 위치는 아직 없음
        }
        # 출근 기록 저장
        db.insert_one(collection=Collection.ATTENDANCE, data=new_attendance)

        response = {
            "login_id": request.account_id,
            "date" : current_date,
            "check_in_time": current_time,
            "check_in_location": {
                "latitude": request.coordinate.latitude,
                "longitude": request.coordinate
            }
        }

        return response

    def attendance_check_out(self, request) -> attendance_check_type_instance:
        # 1. account_id 정보가 DB에 존재하는지 확인
        account_info = fake_db.get_account(request.account_id)
        if not account_info:
            raise ValueError("유효한 계정이 아닙니다.")

        # 2. coordinate를 기반으로 구한 시간정보(현재 시각)이 근무 시작 예정 시간보다 0~30분 이전인지 확인
        current_time = datetime.strptime(
            self.get_current_time(request.coordinate.latitude, request.coordinate.longitude),
            "%H:%M:%S", )
        work_end_time = datetime.strptime(account_info["work_end_time"], "%H:%M:%S", )
        if self.check_out_time_validation_strategy.is_valid(current_time, work_end_time):
            raise ValueError("퇴근 시간이 유효하지 않습니다.")  # todo: 퇴근은 업무시간 이전에도 가능하게 로직 변경해야 한다면 추후 리팩토링 필요

        # 3. coordinate가 회사 위경도 정보에서 오차 범위 이내인지 확인
        company_coordinates = account_info["company_coordinates"]
        if not self.coordinate_validation_strategy.is_within_error_range(company_coordinates, request.coordinate):
            raise ValueError("유효한 위치가 아닙니다.")

        # 출근 기록 저장
        self.save_check_out_to_db(request.account_id, current_time, request.coordinate)

        response = {
            "check_in_time": current_time.strftime("%Y-%m-%d %H:%M:%S %Z%z"),
            "login_id": request.account_id,
            "check_in_coordinate": {"Latitude": {request.coordinate.latitude},
                                    "Longitude": {request.coordinate.longitude}}

        }

        return response

    def save_check_out_to_db(self, account_id, check_out_time, coordinate):
        # 퇴근 데이터를 MongoDB에 저장
        attendance_data = {
            "account_id": account_id,
            "check_out_time": check_out_time,
            "check_out_coordinate": coordinate.dict()
        }
        db[Collection.ATTENDANCE.value].insert_one(attendance_data)

    def get_current_date(self):
        # 현재 날짜를 가져오기
        current_datetime = datetime.now()
        current_date = current_datetime.date()

        return current_date

    def get_current_time(self, latitude, longitude):
        # 위도와 경도를 사용하여 위치 정보 가져오기
        geolocator = Nominatim(user_agent="get_current_time")
        location = geolocator.reverse(f"{latitude}, {longitude}")
        if location:
            # 위치 정보에서 타임존 가져오기
            timezone_str = TimezoneFinder().timezone_at(lng=longitude, lat=latitude)
            timezone = pytz.timezone(timezone_str)

            # 현재 시각 가져오기
            current_time = datetime.now(timezone)
            return current_time.strftime("%H:%M:%S")
        else:
            return "위치 정보를 찾을 수 없습니다."

    # def attendance_check_in_update(self, request) -> attendance_check_type_instance:
    #     # 1. account_id 정보가 DB에 존재하는지 확인
    #     account_info = fake_db.get_account(request.account_id)
    #     if not account_info:
    #         raise ValueError("유효한 계정이 아닙니다.")
    #
    #     # 2. coordinate가 회사 위경도 정보에서 오차 범위 이내인지 확인
    #     company_coordinates = account_info["company_coordinates"]
    #     if not self.coordinate_validation_strategy.is_within_error_range(company_coordinates, request.coordinate):
    #         raise ValueError("유효한 위치가 아닙니다.")
    #
    #     # 3. 입력 받은 출근 시간 수정 시각이 유효한지 확인 # Todo
    #     # update_check_in_time = datetime.strptime(account_info["updated_check_in_hour"], "%H:%M:%S", )
    #     # if self.check_in_time_validation_strategy.is_valid(update_check_in_time):
    #     #     raise ValueError("수정된 출근 시간이 유효하지 않습니다.")
    #
    #     # 출근 기록 저장
    #
    #     response = {
    #         "check_in_time": current_time.strftime("%Y-%m-%d %H:%M:%S %Z%z"),
    #         "login_id": request.account_id,
    #         "coordinate": {"Latitude": {request.coordinate.latitude}, "Longitude": {request.coordinate.longitude}}
    #     }
    #
    #     return response
    #
    # def attendance_check_out_update(self, request) -> attendance_check_type_instance:
    #     # 1. account_id 정보가 DB에 존재하는지 확인
    #     account_info = fake_db.get_account(request.account_id)
    #     if not account_info:
    #         raise ValueError("유효한 계정이 아닙니다.")
    #
    #     # 2. coordinate를 기반으로 구한 시간정보(현재 시각)이 근무 시작 예정 시간보다 0~30분 이전인지 확인
    #     current_time = datetime.strptime(
    #         self.get_current_time(request.coordinate.latitude, request.coordinate.longitude),
    #         "%H:%M:%S", )
    #     work_start_time = datetime.strptime(account_info["work_start_time"], "%H:%M:%S", )
    #     if self.check_in_time_validation_strategy.is_valid(current_time, work_start_time):
    #         raise ValueError("출근 시간이 유효하지 않습니다.")
    #
    #     # 3. coordinate가 회사 위경도 정보에서 오차 범위 이내인지 확인
    #     company_coordinates = account_info["company_coordinates"]
    #     if not self.coordinate_validation_strategy.is_within_error_range(company_coordinates, request.coordinate):
    #         raise ValueError("유효한 위치가 아닙니다.")
    #
    #     # 출근 기록 저장
    #     fake_db.save_check_in(request.account_id, current_time)
    #
    #     response = {
    #         "check_in_time": current_time.strftime("%Y-%m-%d %H:%M:%S %Z%z"),
    #         "login_id": request.account_id,
    #         "coordinate": {"Latitude": {request.coordinate.latitude}, "Longitude": {request.coordinate.longitude}}
    #
    #     }
    #
    #     return response
