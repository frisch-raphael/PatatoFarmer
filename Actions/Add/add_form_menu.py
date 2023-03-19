import readline
from Actions.Add.back_action import BackAction
from base_menu import BaseMenu
from target import Target


class AddFormMenu(BaseMenu):
    current_action_options = [
        {
            "id": "back",
            "class": BackAction,
        },
        {
            "id": "set",
            "class": None,
        },
        {
            "id": "fetch parameters",
            "class": None,
        }
    ]

    def __init__(self, target: Target):
        self.target = target
        super().__init__()

    def __completer(self, text, state):
        """
        This function is used by the readline library to generate tab completions.
        """
        buffer = readline.get_line_buffer()
        print(buffer)
        if buffer.startswith("set"):
            target_properties = [
                attr for attr in dir(self.target) if not callable(getattr(self.target, attr)) and not attr.startswith("__")
            ]
            matches = [
                prop for prop in target_properties if prop.startswith(text.lower())]
        else:
            ids = self._get_ids()
            matches = [id for id in ids if id.startswith(text.lower())]

        try:
            return matches[state]
        except IndexError:
            return IndexError

    def prepare_and_launch_menu(self):
        readline.set_completer(self.__completer)
        readline.parse_and_bind('tab: complete')
        super().prepare_and_launch_menu("add target>")
