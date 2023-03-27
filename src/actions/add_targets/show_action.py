from prettytable import PrettyTable
from src.actions.base_action import BaseActionWithTarget
from src.utils.table_printer import TablePrinter
from src.enums.supported_number_of_args import ArgCountOptions


class ShowAction(BaseActionWithTarget):
    usage = """show"""
    arg_count_options = [ArgCountOptions.NONE]

    def _execute(self, args):
        TablePrinter.show_target(self.target_dto)
