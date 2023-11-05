from pydantic import BaseModel


class CoordinateType(BaseModel):
    latitude: float
    longitude: float


class attendance_check_type(BaseModel):
    check_in_time: str
    login_id: str
    coordinate: CoordinateType
