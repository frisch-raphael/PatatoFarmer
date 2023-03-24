from pydantic import ColorError
from Actions.base_action import BaseActionWithTarget
from Classes.logger import Logger
from enum import Enum, auto
import textwrap
from termcolor import colored


class NumberOfParamsOptions(Enum):
    NONE = auto()  # the set parameter action accepts no argument
    UNIQUE = auto()  # the set parameter action accepts one argument
    MULTIPLE = auto()  # the set parameter action accepts one ore more argument(s)


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
                 number_of_params: list[NumberOfParamsOptions],
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
        if NumberOfParamsOptions.MULTIPLE in self.number_of_params:
            value1 = f"<{self.__remove_s(parameter)}_1>"
            valuen = f"<{self.__remove_s(parameter)}_n>"
            print(
                f"set {parameter} [{value1} ... {valuen}]")

        if NumberOfParamsOptions.UNIQUE in self.number_of_params:
            usage_value = "|".join(
                self.supported_values) if self.supported_values else f"{parameter}_value"
            print(f"set {parameter} <{usage_value}>")

        if NumberOfParamsOptions.NONE in self.number_of_params:
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

    usage = SetActionUsage.base_usage

    params_usage = [
        SetActionUsage(
            'url',
            [NumberOfParamsOptions.UNIQUE],
            examples=["set url http://www.ethicalhackers.fr"]),
        SetActionUsage(
            'mode',
            [NumberOfParamsOptions.UNIQUE],
            textwrap.dedent("""
                Mode configure how you want to bruteforce the URL. For now, only standard http(s) form are supported."""),
            supported_values=["http-form", "https-form"],
            examples=["set mode http-form", "set mode https-form"]
        ),
        SetActionUsage(
            'pass_user_lists',
            [NumberOfParamsOptions.MULTIPLE, NumberOfParamsOptions.NONE],
            textwrap.dedent("""
                pass_user_lists is a path to a colon separated (user:password) list to bruteforce the target with. 
                One user:password per line.
                If additional_keywords are set, those will also be used during the bruteforce.
                i.e, 'additionnalkeyword' will be used as 'additionnalkeyword:additionnalkeyword'""")
        ),
        SetActionUsage(
            'additional_keywords',
            [NumberOfParamsOptions.MULTIPLE],
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
            [NumberOfParamsOptions.UNIQUE],
            textwrap.dedent(
                """Status specifies whether the bruteforce was already done or not."""),
            supported_values=["todo", "error", "done"]
        ),
        SetActionUsage(
            'login_param',
            [NumberOfParamsOptions.UNIQUE],
            textwrap.dedent(
                """login_param is the parameter name used in the POST data that will hold the value for usernames."""),
            examples=["set login_param username"]),
        SetActionUsage(
            'password_param',
            [NumberOfParamsOptions.UNIQUE],
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

    def __test_usage_correctness_and_display_help(self, command_parts: list[str]):
        # Check that the user inputed an parameter and not just "set"
        if len(command_parts) == 0:
            SetActionUsage.no_param()
            return False

        # start checking cases where the user did input a parameter to set
        if len(command_parts) >= 1:
            arguments = command_parts[1:]
            param_name = command_parts[0]
            param_usage = self.__get_param_usage_by_name(param_name)

            # Check if the user asked for help
            if arguments and arguments[0].lower() == 'help':
                param_usage.display_full_help(param_name)
                return False

            # Check that the inputed parameter is supported
            if not hasattr(self.target_dto, param_name):
                SetActionUsage.invalid_param(param_name)
                return False

            # check that the supported parameter is not used with more than one argument if it does not support multiple arguments
            if len(arguments) > 1 and not NumberOfParamsOptions.MULTIPLE in param_usage.number_of_params:
                Logger.warn(
                    f"Too many arguments given. {param_usage.str_proposing_help()}")
                param_usage.display_usage(param_usage.name)
                return False

            # check that the supported parameter is called with arguments if it needs it
            if not arguments and not NumberOfParamsOptions.NONE in param_usage.number_of_params:
                Logger.warn(
                    f"No argument given. {param_usage.str_proposing_help()}")
                param_usage.display_usage(param_usage.name)
                return False

            # Check that if one argument is given, it is indeed supported by param_usage
            one_argument_given = len(arguments) == 1
            supported_options = (NumberOfParamsOptions.UNIQUE,
                                 NumberOfParamsOptions.MULTIPLE)
            if one_argument_given and not any(option in param_usage.number_of_params for option in supported_options):
                Logger.warn(
                    f"Unsupported number of arguments given. {param_usage.str_proposing_help()}")
                param_usage.display_usage(param_usage.name)
                return False

            if param_usage.supported_values and arguments[0] not in param_usage.supported_values:
                Logger.warn(
                    f"Supported values are: {', '.join(param_usage.supported_values)}.")
                # param_usage.display_usage(param_usage.name)
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
