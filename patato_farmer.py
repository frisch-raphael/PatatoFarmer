from Model.base import db
import appsettings
from pony.orm import sql_debug
from Menus.main_menu import MainMenu
from Classes.wordlist_file_manager import WordlistFileManager

class PatatoFarmer:


    # sql_debug(True)
    db.bind(**appsettings.db_params)
    db.generate_mapping(create_tables=True)

    WordlistFileManager.remove_unlinked_wordlists()
    WordlistFileManager.import_files_from_subdirs()

    menu = MainMenu()
    menu.prepare_and_launch_menu()
