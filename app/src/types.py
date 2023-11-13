from datetime import datetime

from pydantic import BaseModel


class CoordinateType(BaseModel):
    latitude: float
    longitude: float


class AttendanceCheckType(BaseModel):
    login_id: str
    check_in_time: str
    check_in_location: CoordinateType


example_attendance_check_type = {
    "login_id": "jude0124",
    "date": datetime.now(),
    "check_in_time": "08:50:00",
    "check_in_location": {"latitude": 37.1234, "longitude": 127.5678},
}

attendance_check_type_instance = AttendanceCheckType(**example_attendance_check_type)


class attendance_check_update_type(BaseModel):
    check_in_time: str
    login_id: str
    coordinate: CoordinateType
