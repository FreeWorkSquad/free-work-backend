import logging
import os
import sys
import time
from contextlib import asynccontextmanager

import uvicorn
from fastapi import Depends, FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.responses import JSONResponse

from app import SERVICE_CODE, check_env_exist, LOG_LEVEL, MAJOR_VERSION, port, setup_logging, JSON_LOGS, conf
from app.dependencies import get_token_header
from app.internal import admin
from app.routers import attendance, member
from app.src.config import Description, Service
from app.src.exception.service import SampleServiceError
from app.version import SERVICE, GIT_REVISION, GIT_BRANCH, BUILD_DATE, GIT_SHORT_REVISION


@asynccontextmanager
async def lifespan(lifespan_app: FastAPI):
    # startup event
    logging.debug(f"Working Directory: {repr(os.getcwd())}")
    logging.info("Start Python FastAPI Template")
    logging.info("Check env exist ...")
    check_env_exist()
    yield
    # shutdown event
    logging.info("Shut down Python FastAPI Template")


app = FastAPI(
    lifespan=lifespan,
    title=f"{SERVICE} Service",
    description=Description.DESCRIPTION,
    version=f"{MAJOR_VERSION}.{GIT_SHORT_REVISION}",
    dependencies=[Depends(get_token_header)]
)
app.logger = setup_logging(conf=conf, json_logs=JSON_LOGS, log_level=LOG_LEVEL)  # type: ignore

if SERVICE == Service.SAMPLE.value:
    app.include_router(member.router)
    app.include_router(attendance.router)
    app.include_router(
        admin.router,  # app/internal/admin.py 원본을 수정하지 않고 선언 가능
        prefix="/admin",
        tags=["admin"],
        responses={418: {"description": "I'm a teapot"}},
    )


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = f"{process_time:.6f} sec"
    return response


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=200,
        content={
            "code": int(str(SERVICE_CODE) + str(exc.status_code)),
            "message": f"{exc.detail}",
            "result": {
                "headers": exc.headers
            }
        }
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=200,
        content={
            "code": int(f"{SERVICE_CODE}{status.HTTP_422_UNPROCESSABLE_ENTITY}"),
            "message": f"Invalid Request: {exc.errors()[0]['msg']} (type: {exc.errors()[0]['type']}), "
                       f"Check {(exc.errors()[0]['loc'])}",
            "result": {
                "body": exc.body
            }
        }
    )


@app.exception_handler(ValidationError)
async def request_validation_exception_handler(request: Request, exc: ValidationError):
    return JSONResponse(
        status_code=200,
        content={
            "code": int(str(SERVICE_CODE) + str(status.HTTP_422_UNPROCESSABLE_ENTITY)),
            "message": "pydantic model ValidationError 발생",
            "result": {
                "body": exc.errors()
            }
        }
    )


@app.exception_handler(SampleServiceError)
async def custom_exception_handler(request: Request, exc: SampleServiceError):
    return JSONResponse(
        status_code=200,
        content={
            "code": int(exc.code),
            "message": f"{exc.message}",
            "result": exc.result
        }
    )


@app.get("/")
async def root():
    return {"title": app.title, "description": app.description, "version": app.version, "docs_url": app.docs_url}


@app.get("/health")
def health():
    return {
        "status": "UP",
        "service": SERVICE,
        "version": f"{MAJOR_VERSION}.{GIT_SHORT_REVISION}",
        "home_path": os.getcwd(),
        "command": f"{' '.join(sys.argv)}",
        "build_date": BUILD_DATE,
    }


@app.get("/info")
async def info():
    version: str = f"{MAJOR_VERSION}.{GIT_SHORT_REVISION}"
    if 'Unknown' in version:
        version = version.split('.')[0]
    return {
        "service": SERVICE,
        "version": version,
        "git_branch": GIT_BRANCH,
        "git_revision": GIT_REVISION,
        "git_short_revision": GIT_SHORT_REVISION,
        "build_date": BUILD_DATE
    }


# setup logging last, to make sure no library overwrites it
# (they shouldn't, but it happens)

if __name__ == '__main__':
    """IDE 환경에서 debug 할때 사용 바람 - 로그 설정 overriding 순서 때문"""
    uvicorn.run(app="main:app", host="0.0.0.0", port=port, log_level=LOG_LEVEL)
