from typing import List
from src.actions.base_action import BaseAction
from src.utils.entity_deleter import EntityDeleter
from src.utils.file_operators.nmap_file_importer import NmapFileImporter
from src.enums.supported_number_of_args import ArgCountOptions


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
