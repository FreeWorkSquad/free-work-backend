from pydantic import BaseModel, Field
from typing import Dict, Optional


class DepartmentModel(BaseModel):
    name: str = Field(..., max_length=100, description="부서 기본명")
    i18n_names: Optional[Dict[str, str]] = Field(None, description="부서명 다국어 Map<Locale, String>")
    dept_external_key: str = Field(..., max_length=100, description="부서 외부키")
    parent_dept_external_key: str = Field(..., max_length=100, description="상위부서 외부키(최상위 조직일 경우만 #)")
    dept_email_address: Optional[str] = Field(None, max_length=100, description="부서 이메일 주소")
    external_email_receive_yn: Optional[bool] = Field(None, description="외부이메일 수신여부")
    disp_ord: str = Field(..., max_length=10, description="조직도 부서 노출 순서")
