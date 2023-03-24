from Actions.base_action import BaseAction
from Model.wordlist import Wordlist
from prettytable import PrettyTable
from pony.orm import db_session


class ListWordlistActions(BaseAction):
    usage = """List all wordlists in the database
    
USAGE:
list"""

    def __init__(self, menu):
        super().__init__(menu)

    @db_session
    def execute(self, args):
        if args:
            print(self.usage)
            return
        print("aa")
        wordlist_types = ['userlist', 'passlist', 'userpasslist']
        titles = ['User Lists', 'Pass Lists', 'User-Pass Lists']

        for wordlist_type, title in zip(wordlist_types, titles):
            wordlists = Wordlist.select(
                lambda w: w.type == wordlist_type)[:]
            table = PrettyTable()
            table.title = title
            table.field_names = ["ID", "Name", "Path", "Type"]

            for wordlist in wordlists:
                wordlist_dict = {
                    'ID': wordlist.id,
                    'Name': wordlist.name,
                    'Path': wordlist.path,
                    'Type': wordlist.type
                }
                table.add_row([wordlist_dict[field_name]
                               for field_name in table.field_names])

            print()
            print(table)

        print("\n")
