from typing import Any

from pydantic import BaseModel

from app import Log
from app.version import VERSION


class APIResponseModel(BaseModel):
    """기본 API 응답 포맷 by free-work-squad"""
    code: int = -1
    message: str = f"API Response Success ({VERSION})" if Log.is_debug_enable() else "API Response Success"
    result: dict[str, Any] = {}


class AttendanceCheckResponse(BaseModel):
    """출근 신청 결과 포맷"""
    check_in_time: str  # 출근 시간을 문자열로 저장 (예: "2023-10-04 09:00:00")
    login_id: str  # 로그인 ID 정보를 문자열로 저장
    gps_info: str  # GPS 정보를 문자열로 저장 (예: "Latitude: 37.1234, Longitude: 128.5678")


class AttendanceCheckInAPIResponseModel(APIResponseModel):
    """출근 신청 API 응답 포맷 by free-work-squad"""
    message: str = f"출근 신청 성공"
    result: AttendanceCheckResponse


class AttendanceCheckOutAPIResponseModel(APIResponseModel):
    """퇴근 신청 API 응답 포맷 by free-work-squad"""
    message: str = f"퇴근 신청 성공"
    result: AttendanceCheckResponse
