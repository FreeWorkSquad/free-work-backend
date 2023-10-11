"""
users API는 간단한 예시로 실제 개발시 attendance API를 참고
"""

from fastapi import APIRouter, Form
from fastapi.responses import JSONResponse

from app.models import APIResponseModel
from app.src.database import db
from app.src.database.collection import Collection

router = APIRouter()  # APIRouter 변수명은 원하는대로 설정 가능


@router.post("/users", tags=["users"], response_model=APIResponseModel, response_class=JSONResponse)
async def create_user(username: str = Form(), password: str = Form()):
    new_user = dict(
        username=username,
        password=password
    )
    created_user = db.insert_one(collection=Collection.USERS, data=new_user)
    return {"result": {"user": created_user.acknowledged}}


@router.get("/users/{username}", tags=["users"], response_model=APIResponseModel, response_class=JSONResponse)
async def get_user(username: str):
    user = db.find_one(collection=Collection.USERS, query={"username": username})
    return {"result": {"username": user.get('username')}}


@router.delete("/users/{username}", tags=["users"], response_model=APIResponseModel, response_class=JSONResponse)
async def delete_user(username: str, password: str = Form()):
    deleted_user = db.delete_one(collection=Collection.USERS, query={"username": username, "password": password})
    return {"result": {"user": deleted_user.deleted_count}}