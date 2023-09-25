"""
PUT, POST, GET 에 대한 다양한 API 예시를 작성해놨으니 참고해서 개발을 진행한다.
되도록이면 Swagger에서 API를 쉽게 파악하기 위해 API 및 Body, Path, Query에 대한 설명을 작성한다.
"""
from typing import Any

from fastapi import APIRouter, Depends, Path, Body, status
from fastapi.responses import JSONResponse

from app import SERVICE_CODE
from app.dependencies import get_token_header
from app.models import APIResponseModel
from app.src.exception.service import SampleServiceError

fake_attendance_db = {"attendance": {"name": "junwork"}, "timestamp": {"time": "2023-09-17 15:13:47 28.15274"}}

router = APIRouter(
    prefix="/attendance",
    tags=["attendance"],
    dependencies=[Depends(get_token_header)],
)


# 1. mock data를 사용하는 경우

@router.post("/work/start", response_model=APIResponseModel, response_class=JSONResponse)
async def work_start():
    return {"result": {"name": fake_attendance_db["attendance"]["name"], "time": fake_attendance_db["timestamp"]}}

@router.post("/work/end", response_model=APIResponseModel, response_class=JSONResponse)
async def work_start():
    return {"result": {"name": fake_attendance_db["attendance"]["name"], "time": fake_attendance_db["timestamp"]}}