from pydantic import BaseModel, Field
from typing import Optional


class AddressModel(BaseModel):
    zipcode: Optional[str] = Field(None, max_length=10, description="우편번호")
    addr: Optional[str] = Field(None, max_length=100, description="주소")
    addr_dtl: Optional[str] = Field(None, max_length=100, description="상세주소")