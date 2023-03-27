from typing import List
from src.actions.base_action import BaseAction
from src.utils.entity_deleter import EntityDeleter
from pony.orm import db_session
from src.enums.supported_number_of_args import ArgCountOptions

from src.models import Wordlist


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
