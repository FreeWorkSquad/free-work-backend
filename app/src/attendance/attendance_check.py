from timezonefinder import TimezoneFinder
from pydantic import constr

from app.models import Coordinate
from app.src.attendance.coordinate_validataion import CoordinateValidationStrategy, CoordinateValidationStrategyDefault
from app.src.attendance.time_validation import TimeValidationStrategy, CheckInTimeValidationStrategyDefault, \
    CheckOutTimeValidationStrategyDefault
from app.src.database.fake_database import fake_db
from app.src.types import attendance_check_type
from geopy.geocoders import Nominatim
from datetime import datetime
import pytz


class AttendanceCheck:
    """AttendanceCheck: 출퇴근 신청 클래스"""
    account_id: constr = "freeworksquad"
    coordinate: Coordinate = Coordinate(latitude=0.0, longitude=0.0)
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

    def attendance_check_in(self, request) -> attendance_check_type:
        # 1. account_id 정보가 DB에 존재하는지 확인
        account_info = fake_db.get_account(request.account_id)
        if not account_info:
            raise ValueError("유효한 계정이 아닙니다.")

        # 2. coordinate를 기반으로 구한 시간정보(현재 시각)이 근무 시작 예정 시간보다 0~30분 이전인지 확인
        current_time = datetime.strptime(
            self.get_current_time(request.coordinate.latitude, request.coordinate.longitude),
            "%H:%M:%S", )
        work_start_time = datetime.strptime(account_info["work_start_time"], "%H:%M:%S", )
        if self.check_in_time_validation_strategy.is_valid(current_time, work_start_time):
            raise ValueError("출근 시간이 유효하지 않습니다.")

        # 3. coordinate가 회사 위경도 정보에서 오차 범위 이내인지 확인
        company_coordinates = account_info["company_coordinates"]
        if not self.coordinate_validation_strategy.is_within_error_range(company_coordinates, request.coordinate):
            raise ValueError("유효한 위치가 아닙니다.")

        # 출근 기록 저장
        fake_db.save_check_in(request.account_id, current_time)

        response = {
            "check_in_time": current_time.strftime("%Y-%m-%d %H:%M:%S %Z%z"),
            "login_id": request.account_id,
            "coordinate": {"Latitude": {request.coordinate.latitude}, "Longitude": {request.coordinate.longitude}}

        }

        return response

    def attendance_check_out(self, reqeust) -> attendance_check_type:
        # 1. account_id 정보가 DB에 존재하는지 확인
        account_info = fake_db.get_account(reqeust.account_id)
        if not account_info:
            raise ValueError("유효한 계정이 아닙니다.")

        # 2. coordinate를 기반으로 구한 시간정보(현재 시각)이 근무 시작 예정 시간보다 0~30분 이전인지 확인
        current_time = datetime.strptime(
            self.get_current_time(reqeust.coordinate.latitude, reqeust.coordinate.longitude),
            "%H:%M:%S", )
        work_end_time = datetime.strptime(account_info["work_end_time"], "%H:%M:%S", )
        if self.check_out_time_validation_strategy.is_valid(current_time, work_end_time):
            raise ValueError("퇴근 시간이 유효하지 않습니다.")  # todo: 퇴근은 업무시간 이전에도 가능하게 로직 변경해야 한다면 추후 리팩토링 필요

        # 3. coordinate가 회사 위경도 정보에서 오차 범위 이내인지 확인
        company_coordinates = account_info["company_coordinates"]
        if not self.coordinate_validation_strategy.is_within_error_range(company_coordinates, reqeust.coordinate):
            raise ValueError("유효한 위치가 아닙니다.")

            # 출근 기록 저장
        fake_db.save_check_out(reqeust.account_id, current_time)

        response = {
            "check_in_time": current_time.strftime("%Y-%m-%d %H:%M:%S %Z%z"),
            "login_id": reqeust.account_id,
            "coordinate": {"Latitude": {reqeust.coordinate.latitude}, "Longitude": {reqeust.coordinate.longitude}}

        }

        return response

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
