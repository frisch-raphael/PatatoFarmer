from Actions.base_action import BaseAction
from Classes.helper import clear_console
from termcolor import colored


class HelpAction(BaseAction):

    def execute(self, args=[]):

        action_options = self.get_menu_options()

        grouped_options = {}

        for option in action_options:
            if "submenu" not in option or not option["submenu"]:
                if "Commands" not in grouped_options:
                    grouped_options["Commands"] = []
                grouped_options["Commands"].append(option)
            else:
                submenu = option["submenu"]
                if submenu not in grouped_options:
                    grouped_options[submenu] = []
                grouped_options[submenu].append(option)
        print("\n\n")
        print("Actions are tab completable.")
        print("type \"action_name help\" for help.")
        print()
        # if submenu_options:
        for submenu, submenu_options in grouped_options.items():
            print(f"{colored(submenu, attrs=['underline'])}\n")
            for option in submenu_options:
                print(f"\033[1m{option['id']}\033[0m: {option['hint']}")
            print()
        print()
        # else:
        #     print()
        #     print("Actions are tab completable.")
        #     print()
        #     for action_option in action_options:
        #         print(
        #             f"\033[1m{action_option['id']}\033[0m: {action_option['hint']}")
        #     print()
        #     print("type \"action_name help\" for help.")
        #     print()
