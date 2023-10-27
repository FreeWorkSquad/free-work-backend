from app.src.database import db
from app.src.database.collection import Collection
from app.src.models.user import RequestUserCreate, UserModel, RequestUserUpdate


def create_user(request: RequestUserCreate):
    if is_exist_user(request.login_id):
        return {"error": "이미 존재하는 아이디입니다."}

    new_user: UserModel = request
    created_user_id = db.insert_one(collection=Collection.USERS, data=new_user.model_dump())
    return {"user_id": created_user_id}


def is_exist_user(login_id: str):
    founded_user = db.find_one(collection=Collection.USERS, query={"login_id": login_id})
    return founded_user is not None


def is_not_exist_user(login_id: str):
    return not is_exist_user(login_id)


def get_user(login_id: str):
    founded_user = db.find_one(collection=Collection.USERS, query={"login_id": login_id})
    return {"user": founded_user}


def get_users():
    founded_users = db.find_all(collection=Collection.USERS)
    return {"users": founded_users}


def update_user(login_id: str, request: RequestUserUpdate):
    if is_not_exist_user(login_id):
        return{"error": "존재하지 않는 아이디입니다."}

    updated_user: UserModel = request
    modified_count = db.update_one(
        collection=Collection.USERS,
        query={"login_id": login_id},
        new_data=updated_user.model_dump())
    return {"modified_count": modified_count}


def delete_user(login_id: str, password: str):
    founded_one = db.find_one(collection=Collection.USERS, query={"login_id": login_id})
    if founded_one is None:
        return {"deleted": 0}

    deleted_count = db.delete_one(collection=Collection.USERS, query={"login_id": login_id})
    return {"deleted_count": deleted_count}
