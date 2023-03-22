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
            forms: list[Target] = Target.list_forms()
            table = PrettyTable()
            table.title = "http(s) form target(s)"

            table.field_names = ["ID", "url", "Mode", "Pass / User Lists",
                                 "Additional Keywords", "Login Param",
                                 "Password Param", "Status"]

            for target in forms:
                target_dict = {
                    'ID': target.id,
                    'url': target.url,
                    'Mode': target.mode,
                    'Pass / User Lists': target.pass_user_lists,
                    'Additional Keywords': target.additional_keywords,
                    'Login Param': target.login_param,
                    'Password Param': target.password_param,
                    'Status': target.status
                }
                table.add_row([target_dict[field_name]
                               for field_name in table.field_names])

            print()
            print(table)
            print("\n")
            standards: list[Target] = Target.list_standards()
            table = PrettyTable()
            table.title = "Standard targets"
            table.field_names = ["ID", "url", "Mode", "Port", "User:pass List",
                                 "Additional Keywords", "Status"]

            for target in standards:
                target_dict = {
                    'ID': target.id,
                    'url': target.url,
                    'Mode': target.mode,
                    'Port': target.port,
                    'User:pass List': target.pass_user_lists,
                    'Additional Keywords': target.additional_keywords,
                    'Status': target.status
                }
                table.add_row([target_dict[field_name]
                               for field_name in table.field_names])
            print(table)
            print("\n")
