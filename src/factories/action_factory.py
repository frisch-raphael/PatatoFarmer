from src.actions.add_targets.back_action import BackAction
from src.actions.add_targets.fetch_action import FetchAction
from src.actions.add_targets.save_action import SaveAction
from src.actions.add_targets.set_action import SetAction
from src.actions.add_targets.show_action import ShowAction
from src.actions.wordlists.wordlist_set_default_action import WordlistSetDefaultAction
from src.actions.wordlists.wordlist_delete_action import WordlistDeleteAction
from src.actions.wordlists.wordlist_list_action import WordlistListAction
from src.actions.exit_action import ExitAction
from src.actions.import_nmap_action import ImportNmapAction
from src.actions.list_action import ListAction
from src.actions.add_action import AddAction
from src.actions.help_action import HelpAction
from src.actions.delete_action import DeleteAction
from src.utils.logger import Logger


class ActionFactory:
    @staticmethod
    def create_action(action_id):
        action_map = {
            "exit": ExitAction,
            "list": ListAction,
            "add": AddAction,
            "help": HelpAction,
            # "export": ExportAction,
            "delete": DeleteAction,
            "back": BackAction,
            "set": SetAction,
            "show": ShowAction,
            "save": SaveAction,
            "import_nmap": ImportNmapAction,
            "wordlist_list": WordlistListAction,
            "wordlist_delete": WordlistDeleteAction,
            "wordlist_set_default": WordlistSetDefaultAction,
            "fetch_parameters": FetchAction,
            # "fetch_parameters": FetchAction
        }

        action_class = action_map.get(action_id)
        if action_class is not None:
            return action_class
        else:
            # raise ValueError(f"Invalid action ID: {action_id}")
            Logger.warn(
                f"Invalid action ID: {action_id}. Type Help if you're lost.")
