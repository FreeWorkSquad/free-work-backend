from fastapi import APIRouter, Body, Depends
from fastapi.params import Form
from fastapi.responses import JSONResponse

from app.dependencies import get_token_header
from app.docs.member import request_member_create_examples, request_member_update_examples
from app.models import APIResponseModel
from app.src.member import service as member_service
from app.src.member.service import RequestMemberCreate
from app.src.models.member import RequestMemberUpdate

router = APIRouter(
    prefix="/member",
    tags=["member"],
    responses={404: {"description": "Not found"}},
    default_response_class=JSONResponse,
    dependencies=[Depends(get_token_header)],
)


@router.post("/", response_model=APIResponseModel)
async def create_member(request: RequestMemberCreate = Body(
    title="회원가입을 위한 인풋 파라미터 설정",
    description="회원가입을 진행하기 위한 다양한 파라미터 설정",
    media_type="application/json",
    examples=request_member_create_examples
)):
    result = member_service.create_member(request)
    return APIResponseModel(result=result)


@router.get("/{member_id}", response_model=APIResponseModel)
async def get_member(member_id: str):
    result = member_service.get_member(member_id)
    return APIResponseModel(result=result)


@router.get("/", response_model=APIResponseModel)
async def get_members():
    result = member_service.get_members()
    return APIResponseModel(result=result)


@router.put("/{member_id}", response_model=APIResponseModel)
async def update_member(member_id: str, request: RequestMemberUpdate = Body(
    title="회원정보 수정을 위한 인풋 파라미터 설정",
    description="회원정보 수정을 진행하기 위한 다양한 파라미터 설정",
    media_type="application/json",
    examples=request_member_update_examples
)):
    result = member_service.update_member(member_id, request)
    return APIResponseModel(result=result)


@router.delete("/{member_id}", response_model=APIResponseModel)
async def delete_member(member_id: str, password: str = Form()):
    result = member_service.delete_member(member_id, password)
    return APIResponseModel(result=result)
