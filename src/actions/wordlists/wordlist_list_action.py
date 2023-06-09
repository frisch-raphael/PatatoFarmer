from src.actions.base_action import BaseAction
from src.utils.table_printer import TablePrinter
from src.enums.acg_count_options import ArgCountOptions
from pony.orm import db_session


class WordlistListAction(BaseAction):
    arg_count_options = [ArgCountOptions.NONE]
    usage = """List all wordlists in the database
    
USAGE:
list"""

    def __init__(self, menu):
        super().__init__(menu)

    @db_session
    def _execute(self, args):
        wordlist_types = ['userlist', 'passlist', 'userpasslist']
        titles = ['User Lists', 'Pass Lists', 'User-Pass Lists']

        for wordlist_type, title in zip(wordlist_types, titles):
            TablePrinter.print_wordlist_table(wordlist_type, title)

        print("\n")
