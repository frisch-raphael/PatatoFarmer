from typing import List
from Actions.base_action import BaseAction
from Classes.entity_deleter import EntityDeleter
from Enums.supported_number_of_args import ArgCountOptions
from Model.target import Target
from pony.orm import db_session


class DeleteAction(BaseAction):
    usage = EntityDeleter.generate_delete_usage_string("target")
    arg_count_options = [ArgCountOptions.UNIQUE, ArgCountOptions.MULTIPLE]

    @db_session
    def _execute(self, args: List[str]):
        if not args:
            print(self.usage)
            return
        if args[0] == "all":
            EntityDeleter.delete_all()
            return
        EntityDeleter.delete_ids(Target, args)
