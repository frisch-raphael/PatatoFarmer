from Enums.supported_number_of_args import ArgCountOptions


class ArgChecker:

    def __init__(self, args, supported_count, supported_values=[]):
        self.args = args
        self.supported_count = supported_count
        self.supported_values = supported_values

    def check_help_requested(self):
        return self.args and self.args[0].lower() == 'help'

    def check_arg_count(self):
        if len(self.args) > 1 and not ArgCountOptions.MULTIPLE in self.supported_count:
            return False, "Too many arguments given."
        if not self.args and not ArgCountOptions.NONE in self.supported_count:
            return False, "No argument given."
        one_argument_given = len(self.args) == 1
        supported_options = (ArgCountOptions.UNIQUE, ArgCountOptions.MULTIPLE)
        if one_argument_given and not any(option in self.supported_count for option in supported_options):
            return False, "Unsupported number of arguments given."
        return True, ""

    def check_values(self):
        if self.supported_values and self.args[0] not in self.supported_values:
            return False, f"Supported values are: {', '.join(self.supported_values)}."
        return True, ""

    def check_all(self):
        checks = [self.check_arg_count(), self.check_values()]
        for check_result, error_message in checks:
            if not check_result:
                return False, error_message
        return True, ""
