from Menus.base_menu import BaseMenu
from Dtos.target_dto import TargetDto


class BaseAction:
    usage = "No usage for this action implemented yet."

    def __init__(self, menu: BaseMenu):
        self.menu = menu

    def _ask_y_or_n(self, question):
        user_input = input(question)
        if user_input.lower() == 'y':
            return True
        elif user_input.lower() == 'n':
            return False
        else:
            print("Invalid input. Please enter 'y' or 'n'.")

    def get_menu_options(self):
        return tuple(self.menu.current_action_options)

    def stop_calling_menu(self):
        self.menu.stop_menu()

    def execute(self, args):
        pass

    def execute(self, args):
        if args and args[0].lower() == 'help':
            print(self.usage)
            return
        self.execute(args)


class BaseActionWithTarget(BaseAction):

    def __init__(self, menu: BaseMenu, target_dto: TargetDto):
        super().__init__(menu)
        self.target_dto = target_dto
