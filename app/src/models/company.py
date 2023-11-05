from pydantic import BaseModel, Field
from typing import Dict, Optional

from app.src.models.address import AddressModel
from app.src.models.contact import OfficePhoneNumber


class CompanyModel(BaseModel):
    company_id: str = Field(..., max_length=30, description="회사 고유번호")
    boss_id: str = Field(..., max_length=30, description="사업주 회원 고유번호")
    boss_nm: str = Field(..., max_length=100, description="기본 사업주명")
    boss_nm_i18n_names: Dict[str, str] = Field({}, description="사업주 다국어명 Map<Locale, String>")
    business_registry_num: Optional[str] = Field(None, max_length=30, description="사업자번호")
    business_registry_nm: Optional[str] = Field(None, max_length=100, description="사업자명")
    business_type: Optional[str] = Field(None, max_length=100, description="업종")
    business_cond: Optional[str] = Field(None, max_length=100, description="업태")
    corporation_num: str = Field(..., max_length=30, description="법인번호 또는 대표자주민번호")
    corporation_nm: str = Field(..., max_length=100, description="법인명 또는 상호")
    place_nm: str = Field(..., max_length=100, description="사업장명")
    place_nm_i18n_names: Dict[str, str] = Field(..., description="사업장 다국어명 Map<Locale, String>")
    category: Optional[str] = Field(None, max_length=1, description="사업장구분(1:대리인, 2:법인사업자, 3:개인사업자)")
    office_phone_no: Optional[OfficePhoneNumber] = Field(None,description="사무실 연락처")
    address: Optional[AddressModel] = Field(None, description="사업장 주소")
    tex_office_code: Optional[int] = Field(None, description="세무서코드")
    add_tex_declare_yn: Optional[str] = Field(None, max_length=1, description="부가세신고여부(Y/N)")
    use_yn: str = Field(..., max_length=1, description="영업여부(Y/N)")
    end_ymd: Optional[str] = Field(None, max_length=10, description="사업장종료일")


class RequestCompanyCreate(CompanyModel):
    pass


class RequestCompanyUpdate(CompanyModel):
    pass
