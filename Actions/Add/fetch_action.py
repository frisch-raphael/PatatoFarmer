from logger import Logger
from Actions.base_action import BaseActionWithTarget
from Classes.param_fetcher import ParamFetcher
from termcolor import colored


class FetchAction(BaseActionWithTarget):
    usage = """    fetch_parameters"""

    def present_params(self, all_params, sub_params, type):
        print(f"Choose the {type} from the following parameters list:")

        for i, param in enumerate(all_params):
            if param in sub_params:
                print(colored(f"    {i+1}. {param}", 'green', attrs=['bold']))
            else:
                print(f"    {i+1}. {param}")
        print(f"    {len(all_params) + 1}. None of the above")
        # validate that the user input is a valid number and within range
        while True:
            try:
                param_index = int(input(f"{type} param number>"))
                if 1 <= param_index <= len(all_params) + 1:
                    break
                else:
                    Logger.warn("Invalid choice. Please enter a valid number.")
            except ValueError:
                Logger.warn("Invalid input. Please enter a number.")

        if param_index == len(all_params) + 1:
            return None
        else:
            return list(all_params)[param_index - 1]

    def execute(self, args):
        # create an instance of ParamFetcher class with target url as argument
        try:
            login_params, password_params, all_params = ParamFetcher(
                self.target.url).fetch_possible_params()

        except:
            # handle any errors that occur during the request
            return

        # present the user with a numbered list of possible login parameters and ask them to input the number associated to their choice
        login_param = self.present_params(all_params, login_params, "login")
        password_param = self.present_params(
            all_params, password_params, "password")

        # set those parameters inside self.target
        self.target.login_param = login_param
        self.target.password_param = password_param

        if self.target.login_param:
            Logger.success(
                f"Set login parameter to: {self.target.login_param}")
        if self.target.password_param:
            Logger.success(
                f"Set password parameter to: {self.target.password_param}")