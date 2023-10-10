"""
PUT, POST, GET 에 대한 다양한 API 예시를 작성해놨으니 참고해서 개발을 진행한다.
되도록이면 Swagger에서 API를 쉽게 파악하기 위해 API 및 Body, Path, Query에 대한 설명을 작성한다.
"""

from fastapi import APIRouter, Depends, Body
from fastapi.responses import JSONResponse

from app.dependencies import get_token_header
from app.docs.attendance import  attendance_example1
from app.models import APIResponseModel, AttendanceCheckRequest, AttendanceCheckInAPIResponseModel
from app.src.attendance.attendance_check import AttendanceCheck
from app.src.types import attendance_check_in_type

fake_attendance_db = {"attendance": {"name": "junwork"}, "timestamp": {"time": "2023-09-17 15:13:47 28.15274"}}

router = APIRouter(
    prefix="/attendance",
    tags=["attendance"],
    dependencies=[Depends(get_token_header)],
)


# 1. mock data를 사용하는 경우

@router.post("/check/in", response_model=AttendanceCheckInAPIResponseModel, response_class=JSONResponse)
async def work_start(
        request: AttendanceCheckRequest = Body(
            title="출근 신청을 위한 인풋 파라미터 설정",
            description="출근 신청을 진행하기 위한 다양한 파라미터 설정",
            media_type="application/json",
            example=attendance_example1
        )
):
    """
    출근 신청 API \n
    위/경도 정보와 계정 ID 정보를 가지고 출근 신청 요청을 응답합니다.\n
    """
    attendance_check_in_response: attendance_check_in_type = AttendanceCheck(
        account_id=request.account_id,
        coordinate=request.coordinate
        ).attendance_check_in()
    return {"result": attendance_check_in_response}


@router.post("/check/out", response_model=APIResponseModel, response_class=JSONResponse)
async def work_end():
    return {"result": {"name": fake_attendance_db["attendance"]["name"], "time": fake_attendance_db["timestamp"]}}
