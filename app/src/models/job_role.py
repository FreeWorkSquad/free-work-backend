from pydantic import BaseModel, Field
from typing import Dict, Optional


class JobRoleModel(BaseModel):
    name: str = Field(..., max_length=100, description="직책 (중복허용안함)")
    i18n_names: Optional[Dict[str, str]] = Field(None, description="직책 다국어명 Map<Locale, String>")
    item_used: bool = Field(..., description="사용여부")
    sort_order: str = Field(..., max_length=10, description="직책 노출 순서")
