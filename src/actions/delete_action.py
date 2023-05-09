from typing import List
from src.actions.base_action import BaseAction
from src.utils.entity_deleter import EntityDeleter
from src.enums.acg_count_options import ArgCountOptions
from src.models.target import Target
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
