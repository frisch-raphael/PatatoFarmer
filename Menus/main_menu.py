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
                "hint": "List all targets in the database",
                "submenu": "Target"
            },
            {
                "id": "add",
                "display_name": "Add target",
                "hint": "Add a new target to the database",
                "submenu": "Target"
            },
            {
                "id": "delete",
                "display_name": "Delete targets",
                "hint": "Delete target(s) from the database",
                "submenu": "Target"
            },
            {
                "id": "import",
                "display_name": "Import targets",
                "hint": "Import target from a nmap scan",
                "submenu": "Target"
            },
            {
                "id": "export",
                "display_name": "Export targets",
                "hint": "Export targets to an XML file",
                "submenu": "Target"
            },
            {
                "id": "add_wordlist",
                "display_name": "Add wordlists",
                "hint": "Add a new wordlist to the database",
                "submenu": "Wordlist"
            },
            {
                "id": "reload_wordlists",
                "display_name": "Reloads wordlists from subdirectories",
                "hint": "Reloads wordlists from subdirectories. Use this command if you modified wordlists directly from ./Wordlists",
                "submenu": "Wordlist"
            },
            {
                "id": "list_wordlists",
                "display_name": "List wordlists",
                "hint": "List all wordlists in the database",
                "submenu": "Wordlist"
            },
            {
                "id": "delete_wordlist",
                "display_name": "Delete wordlists",
                "hint": "Delete wordlist(s) from the database",
                "submenu": "Wordlist"
            }
        ]

    def prepare_and_launch_menu(self):
        super().prepare_and_launch_menu("PatatoFarmer>")
