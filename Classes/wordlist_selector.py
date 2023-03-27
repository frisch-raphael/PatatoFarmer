import cutie
from termcolor import colored
from Classes.config_manager import ConfigManager
from Model.wordlist import Wordlist
from pony.orm import db_session


class WordlistSelector:
    def __init__(self):
        self.userlists = Wordlist.list_userlists()
        self.passlists = Wordlist.list_passlists()
        self.userpasslists = Wordlist.list_userpasslists()
        self.default_wordlists = ConfigManager.get_default_wordlists()

    @db_session
    def select_wordlists(self) -> list[Wordlist]:
        selected_wordlist_names = self.select_wordlists_strings()

        return [Wordlist.get(name=name) for name in selected_wordlist_names]

    @db_session
    def select_wordlists_strings(self) -> list[Wordlist]:
        # Combine all wordlists with headers
        combined_wordlists = [("passlist", self.passlists),
                              ("userlist", self.userlists), ("userpasslist", self.userpasslists)]
        options = []
        caption_indices = []
        ticked_indices = []

        for group_name, wordlists in combined_wordlists:
            if not wordlists:
                continue
            caption_indices.append(len(options))
            options.append(colored(group_name.capitalize(),
                           attrs=['bold', 'underline']))
            for wordlist in wordlists:
                options.append(wordlist.name)
                if wordlist.name in self.default_wordlists:
                    ticked_indices.append(len(options) - 1)

        # Display wordlists with default wordlists preselected
        print("")
        selected_indices = cutie.select_multiple(
            options,
            caption_indices=caption_indices,
            ticked_indices=ticked_indices,
            minimal_count=0
        )

        return [options[index] for index in selected_indices]
