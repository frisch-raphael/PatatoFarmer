
from termcolor import colored


class Logger:

    @staticmethod
    def warn(text):
        warning_flag = "[!] "
        print(colored(warning_flag + text, 'red'))

    @staticmethod
    def success(text):
        success_flag = "[*] "
        print(colored(success_flag + text, 'green'))

    def verbose(text):
        success_flag = "[v] "
        print(colored(success_flag + text, 'blue'))
