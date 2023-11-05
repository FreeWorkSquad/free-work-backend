"""
PUT, POST, GET 에 대한 다양한 API 예시를 작성해놨으니 참고해서 개발을 진행한다.
되도록이면 Swagger에서 API를 쉽게 파악하기 위해 API 및 Body, Path, Query에 대한 설명을 작성한다.
"""

from fastapi import APIRouter, Depends, Body
from fastapi.responses import JSONResponse

from app.dependencies import get_token_header
from app.docs.attendance import attendance_coordinate_example1, attendance_examples
from app.models import AttendanceCheckRequest, AttendanceCheckInAPIResponseModel, \
    AttendanceCheckOutAPIResponseModel
from app.src.attendance.attendance_check import AttendanceCheck
from app.src.types import attendance_check_type

router = APIRouter(
    prefix="/attendance",
    tags=["attendance"],
    dependencies=[Depends(get_token_header)],
)

attendance_checker = AttendanceCheck()


@router.post("/check-in", response_model=AttendanceCheckInAPIResponseModel, response_class=JSONResponse)
async def work_start(
        request: AttendanceCheckRequest = Body(
            title="출근 신청을 위한 인풋 파라미터 설정",
            description="출근 신청을 진행하기 위한 다양한 파라미터 설정",
            media_type="application/json",
            examples=attendance_examples
        )
):
    """
    출근 신청 API \n
    위/경도 정보와 계정 ID 정보를 가지고 출근 신청 요청을 처리하고 응답합니다.\n

    """
    attendance_check_in_response: attendance_check_type = attendance_checker.attendance_check_in(request)
    return {"result": attendance_check_in_response}


@router.post("/check-out", response_model=AttendanceCheckOutAPIResponseModel, response_class=JSONResponse)
async def work_end(
        request: AttendanceCheckRequest = Body(
            title="퇴근 신청을 위한 인풋 파라미터 설정",
            description="퇴근 신청을 진행하기 위한 다양한 파라미터 설정",
            media_type="application/json",
            example=attendance_coordinate_example1
        )
):
    """
    퇴근 신청 API \n
    위/경도 정보와 계정 ID 정보를 가지고 퇴근 신청 요청을 응답합니다.\n
    """
    attendance_check_out_response: attendance_check_type = attendance_checker.attendance_check_out(request)
    return {"result": attendance_check_out_response}
