from typing import List
from Actions.base_action import BaseAction
from Classes.entity_deleter import EntityDeleter
from Model.target import Target
from pony.orm import db_session


class DeleteAction(BaseAction):
    usage = EntityDeleter.generate_delete_usage_string("delete")

    @db_session
    def execute(self, args: List[str]):
        EntityDeleter.delete_ids(Target, args)
