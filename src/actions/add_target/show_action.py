from prettytable import PrettyTable
from actions.base_action import BaseActionWithTarget
from classes.table_printer import TablePrinter
from enums.supported_number_of_args import ArgCountOptions
from models.target import Target


class ShowAction(BaseActionWithTarget):
    usage = """show"""
    arg_count_options = [ArgCountOptions.NONE]

    def _execute(self, args):
        TablePrinter.show_target(self.target_dto)
