from Menus.base_menu import BaseMenu
from target import Target


class BaseAction:
    usage = ""

    def __init__(self, menu: BaseMenu):
        self.menu = menu

    # @classmethod
    # def withTarget(cls, menu: BaseMenu, target: Target):
    #     self.target = target
    #     return cls(menu)

    def _ask_y_or_n(self, question):
        user_input = input(question)
        if user_input.lower() == 'y':
            return True
        elif user_input.lower() == 'n':
            return False
        else:
            print("Invalid input. Please enter 'y' or 'n'.")

    def get_menu_action_options(self):
        return tuple(self.menu.current_action_options)

    def stop_calling_menu(self):
        self.menu.stop_menu()

    def _execute(self, args):
        if args and args[0].lower() == 'help':
            print(self.usage)
            return
        self.execute(args)

    def execute(self, args):
        pass


class BaseActionWithTarget:
    def __init__(self, menu: BaseMenu, target: Target):
        self.menu = menu
        self.target = target
