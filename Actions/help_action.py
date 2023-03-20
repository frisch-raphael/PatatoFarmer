from Actions.base_action import BaseAction
# Import any other action classes you have


class HelpAction(BaseAction):

    def execute(self, args):
        action_options = self.get_menu_action_options()
        # Print id, display_name, and details for each action option
        print("\n")
        print("Commands are tab completable.")
        print("\n")
        for action_option in action_options:
            print(f"{action_option['id']}: {action_option['hint']}")
        print("\n")
