from Actions.base_action import BaseAction
from helper import clear_console


class HelpAction(BaseAction):

    def execute(self, args=[]):
        action_options = self.get_menu_action_options()
        # Print id, display_name, and details for each action option
        # clear_console()
        print()
        print("Actions are tab completable.")
        print()
        for action_option in action_options:
            print(
                f"\033[1m{action_option['id']}\033[0m: {action_option['hint']}")
        print()
        print("type \"action_name help\" for help.")
        print()
