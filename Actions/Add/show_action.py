from prettytable import PrettyTable
from Actions.base_action import BaseActionWithTarget
from target import Target


class ShowAction(BaseActionWithTarget):

    def execute(self, args):

        field_names = ["url", "Mode", "Pass / User Lists",
                       "Additional Keywords", "Login Param", "Password Param", "Status"]

        target_dict = {
            'url': self.target.url,
            'Mode': self.target.mode,
            'Pass / User Lists': self.target.pass_user_lists,
            'Additional Keywords': self.target.additional_keywords,
            'Login Param': self.target.login_param,
            'Password Param': self.target.password_param,
            'Status': self.target.status
        }

        table = PrettyTable()
        table.add_column("Attribute", field_names)
        table.add_column("Value", [target_dict[field_name]
                                   for field_name in field_names])

        print(table)
