import readline
from src.menus.base_menu import BaseMenu
from src.models.target import Target


class AddFormMenu(BaseMenu):

    def __init__(self, target: Target):
        super().__init__()
        self.current_action_options += [
            {
                "id": "back",
                "hint": "Go back to previous menu."
            },
            {
                "id": "show",
                "hint": "Show current target parameters."
            },
            {
                "id": "set",
                "hint": "Set target parameter. Press set + tab for auto completion."
            },
            {
                "id": "fetch_parameters",
                "hint": "Try to guess which parameters are used for login and password from the URL given as target."
            },
            {
                "id": "save",
                "hint": "Save target to database."
            }
        ]
        self.target = target

    def _completer(self, text, state):
        """
        This function is used by the readline library to generate tab completions.
        """
        buffer = readline.get_line_buffer()
        if buffer.startswith("set"):
            target_properties = [
                'login_param', 'password_param', 'status', 'additional_keywords'
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

    def _execute_action(self, action_id, args):
        from src.factories.action_factory import ActionFactory
        action_cls = ActionFactory.create_action(action_id)
        if action_id == 'back' or action_id == 'help':
            action = action_cls(self)
        else:
            action = action_cls(self, self.target)
        action.execute(args)

    def prepare_and_launch_menu(self):
        readline.set_completer(self._completer)
        readline.parse_and_bind('tab: complete')
        super().launch_menu("add http target>")
