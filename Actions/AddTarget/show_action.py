from prettytable import PrettyTable
from Actions.base_action import BaseActionWithTarget
from Model.target import Target


class ShowAction(BaseActionWithTarget):

    def execute(self, args):

        field_names = ["url", "Mode", "Pass / User Lists",
                       "Additional Keywords", "Login Param", "Password Param", "Status"]

        target_dict = {
            'url': self.target_dto.url,
            'Mode': self.target_dto.mode,
            'Pass / User Lists': self.target_dto.pass_user_lists,
            'Additional Keywords': self.target_dto.additional_keywords,
            'Login Param': self.target_dto.login_param,
            'Password Param': self.target_dto.password_param,
            'Status': self.target_dto.status
        }

        table = PrettyTable()
        table.add_column("Attribute", field_names)
        table.add_column("Value", [target_dict[field_name]
                                   for field_name in field_names])

        print(table)
