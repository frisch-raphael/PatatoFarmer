
from termcolor import colored


class Logger:

    @staticmethod
    def warn(text):
        warning_flag = "[!] "
        print(colored("\n" + warning_flag + text + "\n", 'red'))

    @staticmethod
    def success(text):
        success_flag = "[*] "
        print(colored("\n" + success_flag + text + "\n", 'green'))

    def verbose(text):
        success_flag = "[v] "
        print(colored("\n" + success_flag + text + "\n", 'blue'))
