from pydantic import BaseModel, Field
from typing import List, Dict, Optional

from app.src.models.address import AddressModel
from app.src.models.contact import CellPhoneNumber, OfficePhoneNumber


class MemberModel(BaseModel):
    member_id: str = Field(..., min_length=5, max_length=100, description="회원 고유번호")
    email_address: str = Field(..., min_length=5, max_length=100, description="이메일 주소")
    employ_ymd: str = Field(..., max_length=10, description="입사일(yyyy-MM-dd)")
    cellphone_no: CellPhoneNumber = Field(None, description="개인 연락처")
    office_phone_no: Optional[OfficePhoneNumber] = Field(None, description="사무실 연락처")
    birth_ymd: Optional[str] = Field(None, max_length=30, description="생년월일(yyyy-MM-dd)")
    gender_cd: Optional[str] = Field(None, max_length=30, description="성별(MALE, FEMALE)")
    emp_nick: Optional[str] = Field(None, max_length=100, description="닉네임특수 문자 중 ! @ & ( ) - _ + [ ] { } , . 만 허용")
    locale_type_cd: Optional[str] = Field(None, max_length=30, description="로케일정보")
    tmzn_type_cd: Optional[str] = Field(None, max_length=30, description="타임존정보")
    address: Optional[AddressModel] = Field(None, description="회원 주소")
    name: str = Field(..., max_length=100, description="기본 이름")
    i18n_names: Optional[Dict[str, str]] = Field(None, description="이름 다국어 Map<Locale, String>")
    dept_external_key: str = Field(..., max_length=100, description="부서 외부키")
    concurrent_dept_external_keys: List[str] = Field(..., description="겸직 부서 외부키")
    emp_type_external_key: str = Field(..., max_length=100, description="고용 형태 외부키")
    grade_cd_external_key: Optional[str] = Field(None, max_length=100, description="직급 외부키")
    job_cd_external_key: Optional[str] = Field(None, max_length=100, description="직책 외부키")
    password_setting_type: str = Field(..., max_length=10, description="비밀번호 설정 타입(ADMIN/USER)")
    initialize_password: str = Field(..., max_length=100, description="ADMIN: 초기 비밀번호 / USER: 초대메일 받을 이메일 주소")


class RequestMemberCreate(MemberModel):
    pass


class RequestMemberUpdate(MemberModel):
    pass
