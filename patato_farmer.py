from Actions.add_action import AddAction
from Actions.delete_action import DeleteAction
from Actions.list_action import ListAction
from base_menu import BaseMenu


class Bruteforcer:
    hostname = ""


class HttpBruteforcer:
    hostname = ""


class PatatorMenu(BaseMenu):
    # action_options = {'Help': 'help', 'List targets': 'list', 'Add target': 'add', 'Delete targets': 'target',
    #                   'Edit targets': 'edit', 'Bruteforce targets': 'bruteforce', 'Export targets': 'export'}
    # edit_options = {'Hostname': 'hostname', 'Protocol': 'protocol'}
    current_action_options = [
        {
            "id": "list",
            "display_name": "List targets",
            "class": ListAction,
            "hint": "List all targets in the database"
        },
        {
            "id": "add",
            "display_name": "Add target",
            "class": AddAction,
            "hint": "Add a new target to the database"
        },
        {
            "id": "help",
            "display_name": "Help",
            "class": None,
            "hint": "Display available commands and their descriptions"
        },
        {
            "id": "export",
            "display_name": "Export targets",
            "class": None,
            "hint": "Export targets to an XML file"
        },
        {
            "id": "delete",
            "display_name": "Delete targets",
            "class": DeleteAction,
            "hint": "Export targets to an XML file"
        },
    ]

    def __init__(self):
        super().__init__()

    def prepare_and_launch_menu(self):
        super().prepare_and_launch_menu("PatatoFarmer>")


menu = PatatorMenu()
menu.prepare_and_launch_menu()
