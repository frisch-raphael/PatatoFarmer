from src.actions.base_action import BaseAction
from src.enums.acg_count_options import ArgCountOptions


class BackAction(BaseAction):
    usage = """Back"""
    arg_count_options = [ArgCountOptions.NONE]

    def execute(self, args=[]):
        self.stop_calling_menu()
        self.menu.configure_tab_completion()
        self.menu.has_user_backed = True
