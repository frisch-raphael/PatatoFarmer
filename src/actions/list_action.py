from src.actions.base_action import BaseAction
from src.utils.table_printer import TablePrinter, TargetInfoMixin
from src.enums.supported_number_of_args import ArgCountOptions
from src.models.target import Target
from prettytable import ALL, DOUBLE_BORDER, ORGMODE, SINGLE_BORDER, PrettyTable
from pony.orm import db_session


class ListAction(BaseAction, TargetInfoMixin):
    arg_count_options = [ArgCountOptions.NONE]
    usage = """List all targets in the database
    
USAGE:
list"""

    def __init__(self, menu):
        super().__init__(menu)

    @db_session
    def _execute(self, args):
        if args:
            print(self.usage)
            return

        # For forms
        forms = Target.list_forms()
        title = "http(s) form target(s)"

        if forms:
            TablePrinter.print_target_table(forms, title, self.forms_fields)

        # For standards
        standards = Target.list_standards()
        title = "Standard targets"
        standards_fields = self.standard_fields

        if standards:
            TablePrinter.print_target_table(standards, title, standards_fields)
