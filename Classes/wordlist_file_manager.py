from .logger import Logger
import os
from pony.orm import db_session

from Model import Wordlist


class WordlistFileManager:
    __base_path = './Wordlists'
    __subdirectories = ['userlists', 'passlists', 'userpasslists']
    __types = ['userlist', 'passlist', 'userpasslist']
    __max_file_size = 1 * 1024 * 1024  # 1 MB

    @classmethod
    def import_files_from_subdirs(cls):
        for subdir, wordlist_type in zip(cls.__subdirectories, cls.__types):
            dir_path = os.path.join(cls.__base_path, subdir)
            for file_name in os.listdir(dir_path):
                file_path = os.path.join(dir_path, file_name)
                file_size = os.path.getsize(file_path)

                if file_size < cls.__max_file_size:
                    name, _ = os.path.splitext(file_name)

                    with db_session:
                        if not cls.__wordlist_exists(wordlist_type, name):
                            cls.__create_wordlist(
                                wordlist_type, file_path, name)
                            Logger.success(
                                f"Wordlist '{name}' added to the database.")
                        else:
                            Logger.verbose(
                                f"Wordlist '{name}' already exists in the database.")
                else:
                    Logger.warn(
                        f"File '{file_name}' is too large (>1MB) and will not be added.")

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
    def __wordlist_exists(wordlist_type: str, name: str) -> bool:
        return Wordlist.exists(type=wordlist_type, name=name)

    @staticmethod
    @db_session
    def __create_wordlist(wordlist_type: str, file_path: str, name: str) -> None:
        Wordlist(type=wordlist_type, path=file_path, name=name)
