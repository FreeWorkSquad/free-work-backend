"""
- 예제 단순화를 위한 커스텀 헤더를 사용한다.
- 실제로는 보안, 인증 및 권한 부여를 처리하기 위한 apiKey, http, oauth2, openIdConnect 등의
  통합된 [Security utilites](https://fastapi.tiangolo.com/tutorial/security/)를 사용해야 한다.
- TODO: JWT token 사용하여 공통 인증 서비스 연동
"""
from typing import Annotated

from fastapi import Header

from app import X_TOKEN
from app.src.exception.service import TokenValidationError


async def get_token_header(x_token: Annotated[str, Header()]):
    if x_token != X_TOKEN:
        raise TokenValidationError(x_token)
