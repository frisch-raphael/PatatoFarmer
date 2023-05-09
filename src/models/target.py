from pony.orm import *
from urllib.parse import urlparse
from src.dtos.target_dto import TargetDto
from .base import db


class Target(db.Entity):
    id = PrimaryKey(int, auto=True)
    url = Required(str)
    mode = Required(str)
    status = Required(str)
    additional_keywords = Optional(StrArray, nullable=True)
    pass_user_lists = Optional(StrArray, nullable=True)
    login_param = Optional(str, nullable=True)
    password_param = Optional(str, nullable=True)

    @classmethod
    def from_dto(cls, target_dto: TargetDto) -> 'Target':
        return cls(
            url=target_dto.url,
            mode=target_dto.mode,
            status=target_dto.status,
            additional_keywords=target_dto.additional_keywords,
            pass_user_lists=target_dto.pass_user_lists,
            login_param=target_dto.login_param,
            password_param=target_dto.password_param
        )

    @property
    def port(self):
        return urlparse(self.url).port
    
    @property
    def port(self):
        return urlparse(self.url).port

    @staticmethod
    def list_forms() -> list['Target']:
        return Target.select(lambda t: "form" in t.mode)[:]

    @staticmethod
    def list_standards() -> list['Target']:
        return Target.select(lambda t: "form" not in t.mode)[:]
