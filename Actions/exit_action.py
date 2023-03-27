from typing import List
from Actions.base_action import BaseAction
from Enums.supported_number_of_args import ArgCountOptions


class ExitAction(BaseAction):
    usage = "Exit"
    arg_count_options = [ArgCountOptions.NONE]

    def execute(self, _: List[str]):
        exit()
