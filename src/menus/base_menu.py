import readline
from src.utils.logger import Logger


class BaseMenu:

    def __init__(self):
        self.current_action_options = [
            {
                "id": "help",
                "display_name": "Help",
                "hint": "Print this message",
                "submenu": "Miscellaneous"
            },
            {
                "id": "exit",
                "display_name": "Exit",
                "hint": "Exit PatatoFarmer",
                "submenu": "Miscellaneous"
            },
        ]
        self.go_on = True
        self.has_user_backed = False
        self.actions_by_id = {
            action['id']: action for action in self.current_action_options}

    def stop_menu(self):
        self.go_on = False

    def __get_display_names(self):
        return [option["display_name"] for option in self.current_action_options]

    def _get_ids(self):
        return [option["id"] for option in self.current_action_options]

    def _execute_action(self, action_id, args):
        from src.factories.action_factory import ActionFactory
        from src.actions.base_action import BaseAction
        action_cls = ActionFactory.create_action(action_id)
        action: BaseAction = action_cls(self)
        action.execute(args)

    def _completer(self, text, state):
        """
        This function is used by the readline library to generate tab completions.
        """
        ids_matching_text = [
            id for id in self._get_ids() if id.startswith(text.lower())
        ]
        try:
            return ids_matching_text[state]
        except IndexError:
            return IndexError

    def configure_tab_completion(self):
        readline.set_completer_delims(' \t\n')
        readline.set_completer(self._completer)
        readline.parse_and_bind('tab: complete')

    def launch_menu(self, prompt):
        while self.go_on:
            user_input = input(prompt)
            user_input_parts = user_input.strip().split()
            if len(user_input_parts) == 0:
                Logger.warn("No action given")
                from src.actions.help_action import HelpAction
                HelpAction(self).execute()
                continue
            chosen_option_id = user_input_parts[0]
            if chosen_option_id in self._get_ids():
                chosen_args = user_input_parts[1:]
                self._execute_action(chosen_option_id, chosen_args)
                # try:
                # self._execute_action(chosen_option_id, chosen_args)
                # except Exception as e:
                #     Logger.warn(str(e))
                # reset completer in case we modified it from another action
                readline.set_completer(self._completer)
            else:
                Logger().warn("Invalid action. Type \"Help\" for help.")

    def prepare_and_launch_menu(self, prompt):
        self.configure_tab_completion()
        self.launch_menu(prompt)
