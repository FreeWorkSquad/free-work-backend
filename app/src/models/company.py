from pydantic import BaseModel, Field
from typing import Dict, Optional


class CompanyModel(BaseModel):
    place_nm: str = Field(..., max_length=100, description="사업장명")
    place_nm_i18n_names: Dict[str, str] = Field(..., description="사업장 다국어명 Map<Locale, String>")
    corporate_num: str = Field(..., max_length=30, description="법인번호 또는 대표자주민번호")
    corporate_nm: str = Field(..., max_length=100, description="법인명 또는 상호")
    category: Optional[str] = Field(None, max_length=1, description="사업장구분(1:대리인, 2:법인사업자, 3:개인사업자)")
    phone_num: Optional[str] = Field(None, max_length=30, description="전화번호")
    corp_regist_num: str = Field(..., max_length=30, description="사업자등록번호")
    corp_regist_sub_num: Optional[int] = Field(None, description="종사업장번호(4자리)")
    boss_nm: str = Field(..., max_length=100, description="사업장명")
    boss_nm_i18n_names: Dict[str, str] = Field({}, description="사업장 다국어명 Map<Locale, String>")
    use_yn: str = Field(..., max_length=1, description="사용여부(Y/N)")
    zipcode: Optional[str] = Field(None, max_length=10, description="우편번호")
    addr: Optional[str] = Field(None, max_length=100, description="주소")
    addr_dtl: Optional[str] = Field(None, max_length=100, description="상세주소")
    biz_type: Optional[str] = Field(None, max_length=100, description="업종")
    biz_cond: Optional[str] = Field(None, max_length=100, description="업태")
    tex_office_code: Optional[int] = Field(None, description="세무서코드")
    add_tex_declare_yn: Optional[str] = Field(None, max_length=1, description="부가세신고여부")
    end_ymd: Optional[str] = Field(None, max_length=10, description="사업장종료일")


class RequestCompanyCreate(CompanyModel):
    pass
