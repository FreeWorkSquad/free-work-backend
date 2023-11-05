from app.src.database import db
from app.src.database.collection import Collection
from app.src.models.company import CompanyModel, RequestCompanyCreate, RequestCompanyUpdate


def create_company(request: RequestCompanyCreate):
    if db.is_exist(collection=Collection.COMPANIES, query={"company_id": request.company_id}):
        return {"error": "이미 존재하는 회사입니다."}

    if db.is_not_exist(collection=Collection.MEMBERS, query={"member_id": request.boss_id}):
        return {"error": "존재하지 않는 회원입니다."}

    new_company: CompanyModel = request
    created_company_id = db.insert_one(collection=Collection.COMPANIES, data=new_company.model_dump())
    return {"company_id": created_company_id}


def get_company(company_id: str):
    founded_company = db.find_one(collection=Collection.COMPANIES, query={"company_id": company_id})
    return {"company": founded_company}


def get_companies():
    founded_companies = db.find_all(collection=Collection.COMPANIES)
    return {"companies": founded_companies}


def update_company(company_id: str, request: RequestCompanyUpdate):
    if db.is_not_exist(collection=Collection.COMPANIES, query={"company_id": company_id}):
        return{"error": "존재하지 않는 회사입니다."}

    updated_company: CompanyModel = request
    modified_count = db.update_one(
        collection=Collection.COMPANIES,
        query={"company_id": company_id},
        new_data=updated_company.model_dump())
    return {"modified_count": modified_count}


def delete_company(company_id: str, password: str):
    if db.is_not_exist(collection=Collection.COMPANIES, query={"company_id": company_id}):
        return {"deleted": 0}

    deleted_count = db.delete_one(collection=Collection.COMPANIES, query={"company_id": company_id})
    return {"deleted_count": deleted_count}
