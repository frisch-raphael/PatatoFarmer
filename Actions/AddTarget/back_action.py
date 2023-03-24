from Actions.base_action import BaseAction


class BackAction(BaseAction):
    usage = """    Back"""

    def execute(self, args=[]):
        self.stop_calling_menu()
        self.menu.configure_tab_completion()
        self.menu.has_user_backed = True
