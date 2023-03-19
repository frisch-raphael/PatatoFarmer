import readline
from Actions.Add.add_form_menu import AddFormMenu
from Actions.base_action import BaseAction
from urllib.parse import urlparse
from logger import Logger

from target import Target


class AddAction(BaseAction):
    usage = """    Add a target to be bruteforced
    add USAGE:
    add <url>
    
    EXAMPLES:
    add http://www.ethicalhackers
    add ftp://10.0.0.1"""

    # def __init():

    def __http_bruteforce_completer(self, _, state):
        return ['1', '2', '3'][state]

    def __choose_http_bruteforce(self):
        readline.set_completer(self.__http_bruteforce_completer)
        print("What kind of http bruteforce do you want ?")
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

    def execute(self, args):
        if len(args) != 1:
            print(self.usage)
            return
        parsed_uri = urlparse(args[0])
        mode = parsed_uri.scheme
        if "http" in parsed_uri.scheme:
            mode = f"{parsed_uri.scheme}-{self.__choose_http_bruteforce()}"

        target = Target(hostname=parsed_uri.hostname,
                        mode=mode,
                        port=parsed_uri.port)
        if "form" in mode:
            add_form_menu = AddFormMenu(target)
            add_form_menu.prepare_and_launch_menu()
            if add_form_menu.has_user_backed:
                return

        try:
            target.save_to_db()
            Logger.success(
                f"Added {target.hostname} target to the database")
        except Exception as e:
            Logger.warn("Could not save target to DB")
