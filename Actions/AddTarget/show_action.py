from prettytable import PrettyTable
from Actions.base_action import BaseActionWithTarget
from Classes.table_printer import TablePrinter
from Enums.supported_number_of_args import ArgCountOptions
from Model.target import Target


class ShowAction(BaseActionWithTarget):
    usage = """show"""
    arg_count_options = [ArgCountOptions.NONE]

    def _execute(self, args):
        TablePrinter.show_target(self.target_dto)
