from app.src.database import db
from app.src.database.collection import Collection
from app.src.models.user import RequestUserCreate, UserModel


def create_user(request: RequestUserCreate):
    new_user: UserModel = request
    created_user_id = db.insert_one(collection=Collection.USERS, data=new_user.model_dump())
    return {"user_id": created_user_id}


def get_user(login_id: str):
    founded_user = db.find_one(collection=Collection.USERS, query={"login_id": login_id})
    return {"user": founded_user}


def get_users():
    founded_users = db.find_all(collection=Collection.USERS)
    return {"users": founded_users}


def update_user(login_id: str, request: RequestUserCreate):
    updated_user = request
    updated_user_id = db.update_one(collection=Collection.USERS, query={"login_id": login_id}, data=updated_user)
    return {"user_id": updated_user_id}


def delete_user(login_id: str, password: str):
    founded_one = db.find_one(collection=Collection.USERS, query={"login_id": login_id})
    if founded_one is None:
        return {"deleted": 0}

    deleted_count = db.delete_one(collection=Collection.USERS, query={"login_id": login_id})
    return {"deleted": deleted_count}
