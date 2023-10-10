from timezonefinder import TimezoneFinder
from pydantic import constr

from app.models import Coordinate, AttendanceCheckResponse
from app.src.database.fake_database import fake_db
from app.src.types import attendance_check_in_type
from geopy.geocoders import Nominatim
from datetime import datetime
import pytz


class AttendanceCheck:
    """AttendanceCheck: 출퇴근 신청 클래스"""
    DEFAULT_ACCOUNT_ID: constr = "freeworksquad"
    DEFAULT_COORDINATE: Coordinate = Coordinate(latitude=0.0, longitude=0.0)

    def __init__(
            self,
            account_id: constr,
            coordinate: Coordinate
    ):
        self.coordinate = coordinate if coordinate is not None else AttendanceCheck.DEFAULT_COORDINATE
        self.account_id = account_id if account_id is not None else AttendanceCheck.DEFAULT_ACCOUNT_ID

    def attendance_check_in(self) -> attendance_check_in_type:
        # 1. account_id 정보가 DB에 존재하는지 확인
        account_info = fake_db.get_account(self.account_id)
        if not account_info:
            raise ValueError("유효한 계정이 아닙니다.")

        # 2. coordinate를 기반으로 구한 시간정보(현재 시각)이 근무 시작 예정 시간보다 0~30분 이전인지 확인
        current_time = datetime.strptime(self.get_current_time(self.coordinate.latitude, self.coordinate.longitude),"%H:%M:%S",)
        work_start_time = datetime.strptime(account_info["work_start_time"], "%H:%M:%S",)
        time_difference = (current_time - work_start_time).total_seconds() / 60  # 분 단위로 차이 계산
        if time_difference < 0 or time_difference > 30:
            raise ValueError("출근 시간이 유효하지 않습니다.")

        # 3. coordinate가 회사 위경도 정보에서 오차 범위 이내인지 확인
        company_coordinates = account_info["company_coordinates"]
        if not self.is_within_error_range(company_coordinates, self.coordinate):
            raise ValueError("유효한 위치가 아닙니다.")

        # 출근 기록 저장
        fake_db.save_check_in(self.account_id, current_time)

        response = {
            "check_in_time": current_time.strftime("%Y-%m-%d %H:%M:%S %Z%z"),
            "login_id": self.account_id,
            "coordinate": f"Latitude: {self.coordinate.latitude}, Longitude: {self.coordinate.longitude}"
        }

        return response

    def is_within_error_range(self, coord1, coord2, max_error=0.01):
        # 좌표 간의 거리 계산
        lat1, lon1 = coord1.latitude, coord1.longitude
        lat2, lon2 = coord2.latitude, coord2.longitude
        distance = ((lat1 - lat2) ** 2 + (lon1 - lon2) ** 2) ** 0.5
        return distance <= max_error

    def get_current_time(self, latitude, longitude):
        # 위도와 경도를 사용하여 위치 정보 가져오기
        geolocator = Nominatim(user_agent="get_current_time")
        location = geolocator.reverse(f"{latitude}, {longitude}")
        if location:
            # 위치 정보에서 타임존 가져오기
            timezone_str = TimezoneFinder().timezone_at(lng=longitude,lat=latitude)
            timezone = pytz.timezone(timezone_str)

            # 현재 시각 가져오기
            current_time = datetime.now(timezone)
            return current_time.strftime("%H:%M:%S")
        else:
            return "위치 정보를 찾을 수 없습니다."
