from typing import List
from Actions.base_action import BaseAction
from Classes.entity_deleter import EntityDeleter
from pony.orm import db_session
from Enums.supported_number_of_args import ArgCountOptions

from Model import Wordlist


class WordlistDeleteAction(BaseAction):
    usage = EntityDeleter.generate_delete_usage_string("wordlist")
    arg_count_options = [ArgCountOptions.UNIQUE, ArgCountOptions.MULTIPLE]

    @db_session
    def _execute(self, args: List[str]):
        if not args:
            print(self.usage)
            return
        if args[0] == "all":
            EntityDeleter.delete_all()
            return
        EntityDeleter.delete_ids(Wordlist, args)
