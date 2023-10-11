from pydantic import BaseModel, Field


class UserModel(BaseModel):
    username: Field(..., min_length=3, max_length=20)
    password: Field(..., min_length=3, max_length=20)
