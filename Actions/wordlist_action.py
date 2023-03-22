from Actions.base_action import BaseAction
from target import Target
from prettytable import PrettyTable


class WordlistAction(BaseAction):
    usage = """Manage usernamer lists, password lists, and user:pass lists used during bruteforce
    
 USAGE:
 list"""

    def execute(self, args):
        if args:
            print(self.usage)
            return
        