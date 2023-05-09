from pony.orm import *

from src.utils.file_operators.nmap_file_importer import FileOperator
from .base import db
from src.dtos.wordlist_dto import WordlistDto


class Wordlist(db.Entity):
    type = Required(str)
    path = Required(str)
    name = Required(str)
    hash = Optional(str)

    @db_session
    def delete(self):
        FileOperator.delete(self.path)
        super(Wordlist, self).delete()

    @classmethod
    def from_dto(cls, wordlist_dto: 'WordlistDto') -> 'Wordlist':
        existing_wordlist = cls.get(name=wordlist_dto.name)
        if existing_wordlist:
            suffix = 1
            new_name = f"{wordlist_dto.name}_{suffix}"
            while cls.get(name=new_name):
                suffix += 1
                new_name = f"{wordlist_dto.name}_{suffix}"
            wordlist_dto.name = new_name

        return cls(
            type=wordlist_dto.type,
            path=wordlist_dto.path,
            name=new_name,
            hash=wordlist_dto.hash
        )

    @staticmethod
    @db_session
    def get_passlists() -> list['Wordlist']:
        return Wordlist.select(lambda w: w.type == "passlist")[:]

    @staticmethod
    @db_session
    def get_userlists() -> list['Wordlist']:
        return Wordlist.select(lambda w: w.type == "userlist")[:]

    @staticmethod
    @db_session
    def get_userpasslists() -> list['Wordlist']:
        return Wordlist.select(lambda w: w.type == "userpasslist")[:]

    @classmethod
    @db_session
    def get_wordlists(cls):
        return [cls.get_userlists(),
                cls.get_passlists(),
                cls.get_userpasslists()]
