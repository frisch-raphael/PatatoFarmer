from typing import List
from src.actions.base_action import BaseAction
from src.utils.config.config_manager import ConfigManager
from src.utils.wordlist_selector import WordlistSelector

from src.enums.acg_count_options import ArgCountOptions


class WordlistSetDefaultAction(BaseAction):
    usage = """Set the default wordlists.
When you create a new target, these default wordlists will be automatically assigned as the wordlists to be used during the brute force attack.
Wordlists are automatically imported from the ./wordlists directory.

There are three types of wordlists: userlists, passlists, and userpasslists. Userpasslists contain one user:pass combination per line.
If you configure a userlist, you must also configure a passlist.
If you configure both a userlist/passlist and a userpasslist, two separate brute force attacks will be initiated:

    1- One that tries each combination of usernames from the userlist and passwords from the passlist.
    2- Another that uses the userpasslists directly, with the provided user:pass combinations.

USAGE
wordlist_set_default"""
    arg_count_options = [ArgCountOptions.NONE]

    def _execute(self, _: List[str]):
        wordlists = WordlistSelector().select_wordlists()
        ConfigManager().set_default_wordlists(
            [wordlist.name for wordlist in wordlists])
