from Actions.AddTarget.back_action import BackAction
from Actions.AddTarget.fetch_action import FetchAction
from Actions.AddTarget.save_action import SaveAction
from Actions.AddTarget.set_action import SetAction
from Actions.AddTarget.show_action import ShowAction
from Actions.Wordlist.wordlist_set_default_action import WordlistSetDefaultAction
from Actions.Wordlist.wordlist_delete_action import WordlistDeleteAction
from Actions.Wordlist.wordlist_list_action import WordlistListAction
from Actions.exit_action import ExitAction
from Actions.import_nmap_action import ImportNmapAction
from Actions.list_action import ListAction
from Actions.add_action import AddAction
from Actions.help_action import HelpAction
# from Actions.export_action import ExportAction
from Actions.delete_action import DeleteAction
from Classes.logger import Logger


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
