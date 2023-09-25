from enum import Enum


class Service(Enum):
    SAMPLE = "Free Work"


SERVICE = Service.SAMPLE  # TODO: 사용할 서비스 설정


class ServiceCode:
    CODE = {
        Service.SAMPLE: 100
    }


SERVICE_CODE = ServiceCode.CODE[SERVICE]


class Description:
    if SERVICE == Service.SAMPLE:
        DESCRIPTION = "Free Work Backend Service"
