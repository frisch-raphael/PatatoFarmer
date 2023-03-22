from Actions.add_action import AddAction
from Actions.help_action import HelpAction
from Menus.base_menu import BaseMenu
from Actions.delete_action import DeleteAction
from Actions.list_action import ListAction


class MainMenu(BaseMenu):
    # action_options = {'Help': 'help', 'List targets': 'list', 'Add target': 'add', 'Delete targets': 'target',
    #                   'Edit targets': 'edit', 'Bruteforce targets': 'bruteforce', 'Export targets': 'export'}
    # edit_options = {'url': 'url', 'Protocol': 'protocol'}
    def __init__(self):
        super().__init__()
        self.current_action_options += [
            {
                "id": "list",
                "display_name": "List targets",
                "hint": "List all targets in the database"
            },
            {
                "id": "add",
                "display_name": "Add target",
                "hint": "Add a new target to the database"
            },
            {
                "id": "delete",
                "display_name": "Delete targets",
                "hint": "Delete target(s) from the database"
            },
            {
                "id": "import",
                "display_name": "Import targets",
                "hint": "Import target from a nmap scan"
            },
            {
                "id": "export",
                "display_name": "Export targets",
                "hint": "Export targets to an XML file"
            },

        ]

    def prepare_and_launch_menu(self):
        super().prepare_and_launch_menu("PatatoFarmer>")
