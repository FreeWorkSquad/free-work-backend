from fastapi import APIRouter, Body, Depends
from fastapi.params import Form
from fastapi.responses import JSONResponse

from app.dependencies import get_token_header
from app.docs.company import request_company_create_examples, request_company_update_examples
from app.models import APIResponseModel
from app.src.models.company import RequestCompanyCreate, RequestCompanyUpdate
from app.src.company import service as company_service

router = APIRouter(
    prefix="/company",
    tags=["company"],
    responses={404: {"description": "Not found"}},
    default_response_class=JSONResponse,
    dependencies=[Depends(get_token_header)],
)


@router.post("/", response_model=APIResponseModel)
async def create_company(request: RequestCompanyCreate = Body(
    title="회사 생성을 위한 인풋 파라미터 설정",
    description="회사 생성을 진행하기 위한 다양한 파라미터 설정",
    media_type="application/json",
    examples=request_company_create_examples
)):
    result = company_service.create_company(request)
    return APIResponseModel(result=result)


@router.get("/{company_id}", response_model=APIResponseModel)
async def get_company(company_id: str):
    result = company_service.get_company(company_id)
    return APIResponseModel(result=result)


@router.get("/", response_model=APIResponseModel)
async def get_companies():
    result = company_service.get_companies()
    return APIResponseModel(result=result)


@router.put("/{company_id}", response_model=APIResponseModel)
async def update_company(company_id: str, request: RequestCompanyUpdate = Body(
    title="회원정보 수정을 위한 인풋 파라미터 설정",
    description="회원정보 수정을 진행하기 위한 다양한 파라미터 설정",
    media_type="application/json",
    examples=request_company_update_examples
)):
    result = company_service.update_company(company_id, request)
    return APIResponseModel(result=result)


@router.delete("/{company_id}", response_model=APIResponseModel)
async def delete_company(company_id: str, password: str = Form()):
    result = company_service.delete_company(company_id, password)
    return APIResponseModel(result=result)
