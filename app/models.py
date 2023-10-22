from typing import Any

from pydantic import BaseModel, constr, Field

from app import Log
from app.version import VERSION


class APIResponseModel(BaseModel):
    """기본 API 응답 포맷 by free-work-squad"""
    code: int = -1
    message: str = f"API Response Success ({VERSION})" if Log.is_debug_enable() else "API Response Success"
    result: dict[str, Any] = {}


class Coordinate(BaseModel):
    """위,경도 정보"""
    latitude: float = Field(
        title="위도",
        description="위치 인식에 필요한 위도 정보",
        ge=-90.0,  # 최소값
        le=90.0,  # 최대값
        default=0.0  # 기본값
    )
    longitude: float = Field(
        title="경도",
        description="위치 인식에 필요한 경도 정보",
        ge=-180.0,  # 최소값
        le=180.0,  # 최대값
        default=0.0  # 기본값
    )


class AttendanceCheckRequest(BaseModel):
    """출근 신청 요청 포맷"""
    account_id: constr(
        min_length=6,
        max_length=14,
        to_lower= True, # 대소문자 구분 없음
        strip_whitespace=True  # 앞뒤 공백 제거
        ) = Field(
        title="account ID",
        description="계정 ID 정보"
    )

    coordinate: Coordinate = Field(
        title="위/경도 정보",
        description="위치 인식에 필요한 위/경도 정보"
    )


class AttendanceCheckResponse(BaseModel):
    """출근 신청 결과 포맷"""
    check_in_time: str  # 출근 시간을 문자열로 저장 (예: "2023-10-04 09:00:00")
    login_id: str  # 로그인 ID 정보를 문자열로 저장
    coordinate: Coordinate  # GPS 정보를 문자열로 저장 (예: "Latitude: 37.1234, Longitude: 128.5678")


class AttendanceCheckInAPIResponseModel(APIResponseModel):
    """출근 신청 API 응답 포맷 by free-work-squad"""
    code: int = 0
    message: str = f"출근 신청 성공"
    result: AttendanceCheckResponse


class AttendanceCheckOutAPIResponseModel(APIResponseModel):
    """퇴근 신청 API 응답 포맷 by free-work-squad"""
    code: int = 0
    message: str = f"퇴근 신청 성공"
    result: AttendanceCheckResponse
