from pydantic import BaseModel, Field


class CellPhoneNumber(BaseModel):
    number: str = Field(..., pattern="^\\d{3}-\\d{3,4}-\\d{4}$",
                        description="개인 연락처")


class OfficePhoneNumber(BaseModel):
    number: str = Field(..., pattern="^\\d{2,3}-\\d{3,4}-\\d{4}$",
                        description="사무실 연락처")
