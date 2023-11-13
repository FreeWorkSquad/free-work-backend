from datetime import datetime

from pydantic import BaseModel, Field


class Coordinate(BaseModel):
    latitude: float = Field(..., description="위도 (latitude)")
    longitude: float = Field(..., description="경도 (longitude)")

class AttendanceModel(BaseModel):
    login_id: str = Field(..., min_length=5, max_length=100, description="로그인 아이디")
    date: datetime
    check_in_time: str = Field(..., pattern=r'^\d{2}:\d{2}:\d{2}$', description="출근 시간 (HH:MM:SS)")
    check_in_location: Coordinate = Field(..., description="출근 위치 정보", example={"latitude": 37.1234, "longitude": 127.5678})
    check_out_time: str = Field(..., pattern=r'^\d{2}:\d{2}:\d{2}$', description="퇴근 시간 (HH:MM:SS)")
    check_out_location: Coordinate = Field(..., description="퇴근 위치 정보", example={"latitude": 37.9876, "longitude": 126.5432})

# 예시 데이터
example_data = {
    "login_id": "jude0124",
    "date": datetime.now(),
    "check_in_time": "08:50:00",
    "check_in_location": {"latitude": 37.1234, "longitude": 127.5678},
    "check_out_time": "16:10:00",
    "check_out_location": {"latitude": 37.9876, "longitude": 126.5432}
}

# Pydantic 모델 초기화
attendance_model_instance = AttendanceModel(**example_data)
