from Actions.base_action import BaseAction
from target import Target
from prettytable import PrettyTable


class ListAction(BaseAction):
    usage = """    List all targets in the database
    
    USAGE:
    list"""

    def execute(self, args):
        if args:
            print(self.usage)
        else:
            forms = Target.list_forms()
            table = PrettyTable()
            table.title = "http(s) form target(s)"
            table.field_names = ["ID", "Hostname", "Mode", "Port", "Wordlists",
                                 "Additional Keywords", "Status", "Login Param", "Password Param", "Path"]
            for target in forms:
                table.add_row([target.id, target.hostname, target.mode, target.port, target.wordlists,
                               target.additional_keywords, target.status, target.login_param,
                               target.password_param, target.path])
            print("\n")
            print(table)
            print("\n")
            standards = Target.list_standards()
            table = PrettyTable()
            table.title = "Standard targets"
            table.field_names = ["ID", "Hostname", "Mode", "Port", "Wordlists",
                                 "Additional Keywords", "Status"]
            for target in standards:
                table.add_row([target.id, target.hostname, target.mode, target.port, target.wordlists,
                              target.additional_keywords, target.status])
            print(table)
            print("\n")
