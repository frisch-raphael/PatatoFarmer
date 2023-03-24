from typing import List
from Actions.base_action import BaseAction


class ExitAction(BaseAction):
    usage = "Exit"

    def execute(self, _: List[str]):
        exit()
