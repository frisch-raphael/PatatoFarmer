import pathlib
import readline
from src.utils.readline_completer import ReadlineCompleter
from src.menus.base_menu import BaseMenu


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
                "id": "import_nmap",
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
                "id": "wordlist_add",
                "display_name": "Add wordlists",
                "hint": "Add a new wordlist to the database",
                "submenu": "Wordlist"
            },
            # {
            #     "id": "wordlist_reload",
            #     "display_name": "Reloads wordlists from subdirectories",
            #     "hint": "Reloads wordlists from subdirectories. Use this command if you modified wordlists directly from ./wordlists",
            #     "submenu": "Wordlist"
            # },
            {
                "id": "wordlist_list",
                "display_name": "List wordlists",
                "hint": "List all wordlists in the database",
                "submenu": "Wordlist"
            },
            {
                "id": "wordlist_delete",
                "display_name": "Delete wordlists",
                "hint": "Delete wordlist(s) from the database",
                "submenu": "Wordlist"
            },
            {
                "id": "wordlist_set_default",
                "display_name": "Set default wordlists",
                "hint": "Set default wordlist(s). Created targets will have those wordlists configured",
                "submenu": "Wordlist"
            }
        ]

    def _completer(self, text, state):
        """
        This function is used by the readline library to generate tab completions.
        """
        buffer = readline.get_line_buffer()
        if buffer.lower().startswith("import_nmap"):
            incomplete_path = pathlib.Path(text)
            if incomplete_path.is_dir():
                completions = [p.as_posix() for p in incomplete_path.iterdir()]
            elif incomplete_path.exists():
                completions = [incomplete_path]
            else:
                exists_parts = pathlib.Path('.')
                for part in incomplete_path.parts:
                    test_next_part = exists_parts / part
                    if test_next_part.exists():
                        exists_parts = test_next_part

                completions = []
                for p in exists_parts.iterdir():
                    p_str = p.as_posix()
                    if p_str.startswith(text):
                        completions.append(p_str)
            return completions[state]
        else:
            ids = self._get_ids()
            matches = [id for id in ids if id.startswith(text.lower())]
        try:
            return matches[state]
        except IndexError:
            return IndexError

    def prepare_and_launch_menu(self):
        readline_completer = ReadlineCompleter(self)
        readline.set_completer(readline_completer.complete)
        super().prepare_and_launch_menu("patatofarmer>")
