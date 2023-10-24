from fastapi import APIRouter, Body, Depends
from fastapi.params import Form
from fastapi.responses import JSONResponse

from app.dependencies import get_token_header
from app.docs.member import request_member_create_examples, request_member_update_examples
from app.models import APIResponseModel
from app.src.member import service as member_service
from app.src.member.service import RequestUserCreate
from app.src.models.user import RequestUserUpdate

router = APIRouter(
    prefix="/members",
    tags=["members"],
    responses={404: {"description": "Not found"}},
    default_response_class=JSONResponse,
    dependencies=[Depends(get_token_header)],
)


@router.post("/users", response_model=APIResponseModel)
async def create_user(request: RequestUserCreate = Body(
    title="회원가입을 위한 인풋 파라미터 설정",
    description="회원가입을 진행하기 위한 다양한 파라미터 설정",
    media_type="application/json",
    examples=request_member_create_examples
)):
    result = member_service.create_user(request)
    return APIResponseModel(result=result)


@router.get("/users/{login_id}", response_model=APIResponseModel)
async def get_user(login_id: str):
    result = member_service.get_user(login_id)
    return APIResponseModel(result=result)


@router.get("/users", response_model=APIResponseModel)
async def get_users():
    result = member_service.get_users()
    return APIResponseModel(result=result)


@router.put("/users/{login_id}", response_model=APIResponseModel)
async def update_user(login_id: str, request: RequestUserUpdate = Body(
    title="회원정보 수정을 위한 인풋 파라미터 설정",
    description="회원정보 수정을 진행하기 위한 다양한 파라미터 설정",
    media_type="application/json",
    examples=request_member_update_examples
)):
    result = member_service.update_user(login_id, request)
    return APIResponseModel(result=result)


@router.delete("/users/{login_id}", response_model=APIResponseModel)
async def delete_user(login_id: str, password: str = Form()):
    result = member_service.delete_user(login_id, password)
    return APIResponseModel(result=result)
