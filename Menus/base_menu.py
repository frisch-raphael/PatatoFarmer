import readline
from logger import Logger


class BaseMenu:

    def __init__(self):
        self.current_action_options = [{
            "id": "help",
            "display_name": "Help",
            "hint": "Print this message"
        }]
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
        from Factories.action_factory import ActionFactory
        action_cls = ActionFactory.create_action(action_id)
        action = action_cls(self)
        action.execute(args)

    def __completer(self, text, state):
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

    def __prepare_tab_completion(self):
        readline.set_completer(self.__completer)
        readline.parse_and_bind('tab: complete')

    def launch_menu(self, prompt):
        while self.go_on:
            chosen_option_id = input(prompt)
            chosen_option_parts = chosen_option_id.split()
            chosen_option_id = chosen_option_parts[0]
            if chosen_option_id in self._get_ids():
                chosen_args = chosen_option_parts[1:]
                self._execute_action(chosen_option_id, chosen_args)
                readline.set_completer(self.__completer)
            else:
                Logger().warn("Invalid action")

    def prepare_and_launch_menu(self, prompt):
        self.__prepare_tab_completion()
        self.launch_menu(prompt)
