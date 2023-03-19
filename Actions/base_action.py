from base_menu import BaseMenu


class BaseAction:
    id = ''
    display_name = ''
    details = ''

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

    def stop_calling_menu(self):
        self.menu.stop_menu()

    def execute(self, args):
        pass
