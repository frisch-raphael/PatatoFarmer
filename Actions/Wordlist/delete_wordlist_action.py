from typing import List
from Actions.base_action import BaseAction
from Classes.entity_deleter import EntityDeleter
from pony.orm import db_session

from Model import Wordlist


class DeleteWordlistAction(BaseAction):
    usage = EntityDeleter.generate_delete_usage_string("wordlist")

    @db_session
    def execute(self, args: List[str]):
        EntityDeleter.delete_ids(Wordlist, args)
