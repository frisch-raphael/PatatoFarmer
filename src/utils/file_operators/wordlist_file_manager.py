import hashlib
from src.utils.logger import Logger
import os
from pony.orm import db_session

from src.models.wordlist import Wordlist


class WordlistFileManager:
    """
    This class is responsible for managing wordlists in the ./wordlists dir.
    It can import wordlists from subdirectories, re-import if the file hash changes, and remove unlinked wordlists.
    """
    __base_path = './wordlists'
    __subdirectories = ['userlists', 'passlists', 'userpasslists']
    __types = ['userlist', 'passlist', 'userpasslist']
    __max_file_size = 1 * 1024 * 1024  # 1 MB

    @staticmethod
    def __compute_md5(file_path: str) -> str:
        hasher = hashlib.md5()
        with open(file_path, 'rb') as file:
            buf = file.read()
            hasher.update(buf)
        return hasher.hexdigest()

    @classmethod
    def import_files_from_subdirs(cls):
        for subdir, wordlist_type in zip(cls.__subdirectories, cls.__types):
            dir_path = os.path.join(cls.__base_path, subdir)
            for file_name_with_ext in os.listdir(dir_path):
                cls.__process_file(file_name_with_ext, dir_path, wordlist_type)

    @classmethod
    def __process_file(cls, file_name_with_ext: str, dir_path: str, wordlist_type: str):
        file_path = os.path.join(dir_path, file_name_with_ext)
        file_size = os.path.getsize(file_path)
        file_hash = cls.__compute_md5(file_path)
        file_name, _ = os.path.splitext(file_name_with_ext)

        if file_size > cls.__max_file_size:
            Logger.warn(
                f"File '{file_name_with_ext}' is too large (>1MB) and will not be added.")
            return

        with db_session:
            wordlist = Wordlist.get(type=wordlist_type, name=file_name)
            if not wordlist:
                cls.__create_wordlist(
                    wordlist_type, file_path, file_name, file_hash)
                Logger.success(
                    f"Wordlist '{file_name}' added to the database.")
            elif wordlist.hash != file_hash:
                wordlist.path = file_path
                wordlist.hash = file_hash
                Logger.success(
                    f"Wordlist '{file_name}' has changed and has been updated in the database.")
            else:
                Logger.verbose(
                    f"Wordlist '{file_name}' already exists in the database and has not changed.")

    @classmethod
    @db_session
    def remove_unlinked_wordlists(cls):
        all_wordlists = Wordlist.select()[:]
        for wordlist in all_wordlists:
            if not os.path.exists(wordlist.path):
                Logger.warn(
                    f"File '{wordlist.name}' not found. Removing Wordlist from the database.")
                wordlist.delete()

    @staticmethod
    @db_session
    def __create_wordlist(wordlist_type: str, file_path: str, name: str, file_hash: str) -> None:
        Wordlist(type=wordlist_type, path=file_path, name=name, hash=file_hash)
