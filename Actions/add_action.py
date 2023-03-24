import readline
from urllib.parse import urlparse
from Dtos.target_dto import TargetDto
from Menus.add_form_menu import AddFormMenu
from Actions.base_action import BaseAction
from Classes.logger import Logger
from pony.orm import db_session

from Model.target import Target


class AddAction(BaseAction):
    usage = """    Add a target to be bruteforced
    add USAGE:
    add <url>
    
    EXAMPLES:
    add http://www.ethicalhackers
    add ftp://10.0.0.1"""

    def __init__(self, menu):
        super().__init__(menu)

    def __http_bruteforce_completer(self, _, state):
        return ['1', '2', '3'][state]

    def __choose_http_bruteforce(self):
        readline.set_completer(self.__http_bruteforce_completer)
        print("What kind of http bruteforce do you want?")
        print("1. form (i.e the url points to a form with a login/password)")
        print("2. http basic")
        print("3. http ntlm")
        choice = ''
        mode = ""
        while not (choice.isdigit() and '1' <= choice <= '3'):
            choice = input("http type>")
            if choice == "1":
                mode = "form"
            elif choice == "2":
                mode = "basic"
            elif choice == "3":
                mode = "ntlm"
            else:
                Logger.warn("Invalid input. Enter a number between 1 and 3.")
        return mode

    def __get_default_port(self, scheme: str):
        return 443 if scheme == 'https' else 80

    @db_session
    def execute(self, args):
        if len(args) != 1:
            print(self.usage)
            return
        url = args[0]
        parsed_uri = urlparse(url)
        mode = parsed_uri.scheme
        if "http" in parsed_uri.scheme:
            mode = f"{parsed_uri.scheme}-{self.__choose_http_bruteforce()}"
        # port = parsed_uri.port if parsed_uri.port else self.__get_default_port(
        #     parsed_uri.scheme)

        target_dto = TargetDto(url=url, mode=mode)
        if "form" in mode:
            add_form_menu = AddFormMenu(target_dto)
            add_form_menu.prepare_and_launch_menu()
            if add_form_menu.has_user_backed:
                return
        Target.from_dto(target_dto)

        try:
            Logger.success(
                f"Added {target_dto.url} target to the database")
        except Exception as e:
            Logger.warn(f"Could not save target to DB: {str(e)}")
