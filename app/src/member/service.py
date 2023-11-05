from app.src.database import db
from app.src.database.collection import Collection
from app.src.models.member import MemberModel, RequestMemberCreate, RequestMemberUpdate


def create_member(request: RequestMemberCreate):
    if db.is_exist(collection=Collection.MEMBERS, query={"member_id": request.member_id}):
        return {"error": "이미 존재하는 아이디입니다."}

    new_member: MemberModel = request
    created_member_id = db.insert_one(collection=Collection.MEMBERS, data=new_member.model_dump())
    return {"member_id": created_member_id}


def get_member(member_id: str):
    founded_member = db.find_one(collection=Collection.MEMBERS, query={"member_id": member_id})
    return {"member": founded_member}


def get_members():
    founded_members = db.find_all(collection=Collection.MEMBERS)
    return {"members": founded_members}


def update_member(member_id: str, request: RequestMemberUpdate):
    if db.is_not_exist(collection=Collection.MEMBERS, query={"member_id": member_id}):
        return{"error": "존재하지 않는 아이디입니다."}

    updated_member: MemberModel = request
    modified_count = db.update_one(
        collection=Collection.MEMBERS,
        query={"member_id": member_id},
        new_data=updated_member.model_dump())
    return {"modified_count": modified_count}


def delete_member(member_id: str, password: str):
    if db.is_not_exist(collection=Collection.MEMBERS, query={"member_id": member_id}):
        return {"deleted": 0}

    deleted_count = db.delete_one(collection=Collection.MEMBERS, query={"member_id": member_id})
    return {"deleted_count": deleted_count}
