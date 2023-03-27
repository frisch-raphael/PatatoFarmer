from typing import List
from Actions.base_action import BaseAction
from Classes.entity_deleter import EntityDeleter
from Classes.nmap_file_importer import NmapFileImporter
from Enums.supported_number_of_args import ArgCountOptions
from Model.target import Target
from pony.orm import db_session


class ImportNmapAction(BaseAction):
    arg_count_options = [ArgCountOptions.UNIQUE]
    usage = """Import targets from a Nmap scan in xml format.


USAGE:
Nmap <file_path>"""

    def _execute(self, args: List[str]):
        if len(args) != 1:
            print(self.usage)
        nmap_file = args[0]
        nmap_importer = NmapFileImporter(nmap_file)
        nmap_importer.process_xml_files()
