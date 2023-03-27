from src.utils.logger import Logger
from src.utils.arg_checker import ArgChecker
from src.menus.base_menu import BaseMenu
from src.dtos.target_dto import TargetDto


class BaseAction:
    usage = "No usage for this action implemented yet."
    arg_count_options = []
    supported_values = []

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

    def _execute(self, args):
        pass

    def execute(self, args):
        arg_checker = ArgChecker(
            args, self.arg_count_options, self.supported_values)
        if arg_checker.check_help_requested():
            print(self.usage)
            return
        result, error_message = arg_checker.check_all()
        if not result:
            Logger.warn(f"{error_message}")
            print(self.usage)
            return
        self._execute(args)


class BaseActionWithTarget(BaseAction):

    def __init__(self, menu: BaseMenu, target_dto: TargetDto):
        super().__init__(menu)
        self.target_dto = target_dto
