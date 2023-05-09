from src.actions.base_action import BaseActionWithTarget
from src.utils.arg_checker import ArgChecker
from src.utils.logger import Logger
import textwrap
from termcolor import colored
from src.enums.acg_count_options import ArgCountOptions


class ParamUsageNotFoundError(Exception):
    pass


class SetActionUsage():
    base_usage = textwrap.dedent("""        Configure the parameter of your target
                
        \033[1mset USAGE:\033[0m
        set <parameter> <value1> [<value2> [<value3>...]]

        \033[1mEXAMPLES:\033[0m
        set url www.ethicalhackers.fr
        set additional_keywords ethicalhackers ethical hackers
        set pass_user_lists""")

    def __init__(self,
                 name: str,
                 number_of_params: list[ArgCountOptions],
                 additional_usage_help: str = "",
                 examples: list = [],
                 supported_values: list = [],
                 specific_usage: str = ""):
        self.name = name
        self.number_of_params = number_of_params
        self.additional_usage_help = additional_usage_help
        self.examples = examples
        self.supported_values = supported_values
        self.specific_usage = specific_usage

    @classmethod
    def display_base_help(cls):
        print(cls.base_usage)

    @staticmethod
    def no_param():
        Logger.warn(
            "No parameter given. Press tab to display supported parameters for target.")
        SetActionUsage.display_base_help()

    @staticmethod
    def invalid_param(invalid_parameter):
        Logger.warn(
            f"invalid parameter given : {invalid_parameter}. "
            "Press tab to display supported parameters for target.")
        SetActionUsage.display_base_help()

    def __tab_print(self, string):
        print(f"\t{string}")

    def __remove_s(self, s: str):
        if s.endswith('s'):
            return s[:-1]
        return s

    def str_proposing_help(self):
        return f"Type \"set {self.name} help\" for help."

    def display_usage(self, parameter):
        print(colored(f"set {parameter} USAGE:", attrs=['bold']))
        if ArgCountOptions.MULTIPLE in self.number_of_params:
            value1 = f"<{self.__remove_s(parameter)}_1>"
            valuen = f"<{self.__remove_s(parameter)}_n>"
            print(
                f"set {parameter} [{value1} ... {valuen}]")

        if ArgCountOptions.UNIQUE in self.number_of_params:
            usage_value = "|".join(
                self.supported_values) if self.supported_values else f"{parameter}_value"
            print(f"set {parameter} <{usage_value}>")

        if ArgCountOptions.NONE in self.number_of_params:
            print(f"set {parameter}")
        print()

    def display_full_help(self, parameter):
        # print(f"Set the {parameter} for the target.")
        if self.additional_usage_help:
            print()
            print(f"{self.additional_usage_help}")
            print()

        self.display_usage(parameter)

        if self.examples:
            for example in self.examples:
                print(colored("EXAMPLES:", attrs=['bold']))
                print(example)
            print()


class SetAction(BaseActionWithTarget):
    # this is for set, not for set xxxx
    arg_count_options = [ArgCountOptions.MULTIPLE, ArgCountOptions.UNIQUE]
    usage = SetActionUsage.base_usage

    def __init__(self, menu, target_dto):
        super().__init__(menu, target_dto)

    params_usage = [
        SetActionUsage(
            'url',
            [ArgCountOptions.UNIQUE],
            examples=["set url http://www.ethicalhackers.fr"]),
        SetActionUsage(
            'mode',
            [ArgCountOptions.UNIQUE],
            textwrap.dedent("""
                Mode configure how you want to bruteforce the URL. For now, only standard http(s) form are supported."""),
            supported_values=["http-form", "https-form"],
            examples=["set mode http-form", "set mode https-form"]
        ),
        SetActionUsage(
            'pass_user_lists',
            [ArgCountOptions.MULTIPLE, ArgCountOptions.NONE],
            textwrap.dedent("""
                pass_user_lists is a path to a colon separated (user:password) list to bruteforce the target with. 
                One user:password per line.
                If additional_keywords are set, those will also be used during the bruteforce.
                i.e, 'additionnalkeyword' will be used as 'additionnalkeyword:additionnalkeyword'""")
        ),
        SetActionUsage(
            'additional_keywords',
            [ArgCountOptions.MULTIPLE],
            textwrap.dedent(
                """                additional_keywords sets additional keywords that will be used during the bruteforce.
                i.e, if you set "ethicalhackers" as an additional keywords, it will be used as a username and a password during bruteforces.
                Why not just add those words to the username and password lists to begin with?
                Well those lists are meant to be reusable across targets.
                additional_keywords is supposed to hold important words specific to a target.
                By default, additional_keywords is set to words from the url's domain""")
        ),
        SetActionUsage(
            'status',
            [ArgCountOptions.UNIQUE],
            textwrap.dedent(
                """Status specifies whether the bruteforce was already done or not."""),
            supported_values=["todo", "error", "done"]
        ),
        SetActionUsage(
            'login_param',
            [ArgCountOptions.UNIQUE],
            textwrap.dedent(
                """login_param is the parameter name used in the POST data that will hold the value for usernames."""),
            examples=["set login_param username"]),
        SetActionUsage(
            'password_param',
            [ArgCountOptions.UNIQUE],
            textwrap.dedent(
                """password_param is the parameter name used in the POST data that will hold the value for passwords."""),
            examples=["set password_param passwd"])
    ]

    def __get_param_usage_by_name(self, name: str):
        param = next(
            (param for param in self.params_usage if param.name == name), None)
        if not param:
            raise ParamUsageNotFoundError(
                f"Parameter '{name}' not found in params_usage list.")
        return param

    def __is_param_name_valid(self, param_name):
        return hasattr(self.target_dto, param_name)

    def __display_invalid_param_error(self, param_name):
        SetActionUsage.invalid_param(param_name)

    def __get_param_usage_and_checker(self, command_parts):
        param_name = command_parts[0]
        param_usage = self.__get_param_usage_by_name(param_name)
        arguments = command_parts[1:]
        arg_checker = ArgChecker(
            arguments, param_usage.number_of_params, param_usage.supported_values)
        return param_usage, arg_checker

    def __test_usage_correctness_and_display_help(self, command_parts: list[str]):
        if len(command_parts) == 0:
            SetActionUsage.no_param()
            return False

        param_name = command_parts[0]

        # set help
        if param_name.lower() == 'help':
            SetActionUsage.display_base_help()
            return False

        param_usage, arg_checker = self.__get_param_usage_and_checker(
            command_parts)

        # set param help
        if arg_checker.check_help_requested():
            param_usage.display_full_help(param_name)
            return False

        if not self.__is_param_name_valid(param_name):
            self.__display_invalid_param_error(param_name)
            return False

        result, error_message = arg_checker.check_all()
        if not result:
            Logger.warn(f"{error_message} {param_usage.str_proposing_help()}")
            param_usage.display_usage(param_usage.name)
            return False

        return True

    def execute(self, command_parts):
        if not self.__test_usage_correctness_and_display_help(command_parts):
            return

        parameter_name = command_parts[0]
        values = command_parts[1:]

        if len(values) == 1:
            setattr(self.target_dto, parameter_name, values[0])
        else:
            setattr(self.target_dto, parameter_name, values)
        Logger.success(f"{parameter_name} set to '{' '.join(values)}'")
