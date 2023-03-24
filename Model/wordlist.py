from pony.orm import *
from .base import db
from Dtos.wordlist_dto import WordlistDto


class Wordlist(db.Entity):
    type = Required(str)
    path = Required(str)
    name = Required(str)

    @classmethod
    def from_dto(cls, wordlist_dto: 'WordlistDto') -> 'Wordlist':
        return cls(
            type=wordlist_dto.type,
            path=wordlist_dto.path,
            name=wordlist_dto.name,
        )

    @staticmethod
    def list_passlists() -> list['Wordlist']:
        return Wordlist.select(lambda w: w.type == "passlist")[:]

    @staticmethod
    def list_userlists() -> list['Wordlist']:
        return Wordlist.select(lambda w: w.type == "userlist")[:]

    @staticmethod
    def list_userpasslists() -> list['Wordlist']:
        return Wordlist.select(lambda w: w.type == "userpasslist")[:]
