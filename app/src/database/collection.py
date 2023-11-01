from enum import Enum

class Collection(Enum):
    USERS = 'users'
    ATTENDANCE = 'attendance'  # 출퇴근 데이터를 저장할 컬렉션


class AttendanceSchema:
    DATE = "date"  # 출퇴근 일자
    ACCOUNT_ID = "account_id"  # 사용자 계정 ID
    CHECK_IN_TIME = "check_in_time"  # 출근 시간
    CHECK_OUT_TIME = "check_out_time"  # 퇴근 시간
    COORDINATE = "coordinate"  # 출퇴근 좌표 정보


