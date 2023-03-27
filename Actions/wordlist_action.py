from Actions.base_action import BaseAction
from Enums.supported_number_of_args import ArgCountOptions
from Model.target import Target
from prettytable import PrettyTable


class WordlistAction(BaseAction):
    arg_count_options = [ArgCountOptions.NONE]
    usage = """Manage usernamer lists, password lists, and user:pass lists used during bruteforce
    
 USAGE:
 list"""

    def _execute(self, args):
        if args:
            print(self.usage)
            return
