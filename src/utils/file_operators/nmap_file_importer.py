import glob
from src.utils.logger import Logger
import xml.etree.ElementTree as ET
from pony.orm import db_session
from src.utils.file_operators.file_operator import FileOperator
from src.models.target import Target
from src.utils.config.config_manager import ConfigManager


class NmapFileImporter:

    protocols = ['ftp', 'ssh', 'ftps', 'sftp', 'smtp', 'rdp',
                 'pop', 'imap', 'smb', 'mysql', 'mssql', 'snmp', 'ldap']

    def __init__(self, file_path_with_joker):
        self.file_path_with_joker = file_path_with_joker
        self.file_path = ""

    def process_xml_files(self):
        file_pathes = glob.glob(self.file_path_with_joker)
        for file_path in file_pathes:
            self.file_path = file_path
            xml_content = FileOperator.read(file_path)
            try:
                self.process_xml(xml_content)
            except Exception as e:
                Logger.warn(
                    f"Error while importing \"{file_path}\": \"{str(e)}\"")
                continue

    def process_xml(self, xml_content):
        tree = None
        tree = ET.ElementTree(ET.fromstring(xml_content))
        if not tree:
            Logger.warn(f"Could not get tree in {self.file_path}")
            return
        root = tree.getroot()
        if not root:
            Logger.warn(f"Could not get root in {self.file_path}")
            return

        hosts = root.findall('host')
        if not hosts:
            Logger.warn(f"No host found in {self.file_path}")
            return
        one_service_name_found = False
        for host in hosts:
            address = host.find('address').get('addr')
            hostname = host.find('hostnames/hostname')

            if hostname is not None:
                hostname = hostname.get('name')
            else:
                hostname = address

            for port in host.findall("ports/port"):
                port_id = port.get('portid')
                service = port.find('service')
                service_name = service.get('name')
                if not service_name:
                    continue
                if not port.find('state').get('state') == "open":
                    continue
                if service_name in self.protocols:
                    one_service_name_found = True
                    url = f"{service_name}://{hostname}:{port_id}"
                    if not self.__target_exists(url):
                        self.__create_target(url, service_name)
                    else:
                        Logger.warn(
                            f"Target with URL {url} already exists.")
        if not one_service_name_found:
            Logger.warn(f"No target found in {self.file_path}")

    @db_session
    def __target_exists(self, url):
        return Target.get(url=url) is not None

    @db_session
    def __create_target(self, url, mode):
        Target(url=url, mode=mode, status='todo',
               pass_user_lists=ConfigManager.get_default_wordlists())
        Logger.success(f"Target created: {url}")
