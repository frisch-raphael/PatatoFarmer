from bs4 import BeautifulSoup
import requests
import urllib3
from logger import Logger


class ParamFetcher:
    # define lists of possible keywords for login and password parameters as class attributes
    login_keywords = ["login", "email", "user", "name"]
    password_keywords = ["password", "motdepasse",
                         "passe", "passwd", "pwd", "paswd", "mdp"]

    def __init__(self, url):
        # initialize the url and the response attributes
        self.url = url
        self.login_params = set()
        self.password_params = set()
        self.all_params = set()
        self.response = None

    def get_response(self):
        try:
            # check if a global proxy variable is set and use it for the request
            proxy = globals().get("proxy")
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
            if proxy:
                self.response = requests.get(
                    self.url, proxies=proxy, timeout=5, verify=False)
            else:
                self.response = requests.get(self.url, timeout=5, verify=False)

            # check the response status code
            self.response.raise_for_status()

        except requests.exceptions.RequestException as e:
            # handle any errors that occur during the request
            Logger.warn(f"Error: {e}")
            self.response = None

        return self.response

    def fetch_possible_params(self):
        self.get_response()

        # get the parsed html from parse_html method
        soup = BeautifulSoup(self.response.content, "html.parser")
        forms = soup.find_all("form")

        # loop through each form and check if it is a login form
        for form in forms:
            # get the action attribute of the form
            action = form.get("action")

            # get all input elements in the form
            inputs = form.find_all("input")

            # initialize empty sets to store possible login and password parameters

            # loop through each input element and check its type attribute or name attribute for possible keywords
            for input in inputs:
                # get the type and name attributes of the input element
                input_type = input.get("type")
                input_name = input.get("name")
                self.all_params.add(input_name)

                # if the type is password or the name contains a password keyword, add it to password parameters set
                if input_type == "password" or any(keyword.lower() in input_name.lower() for keyword in ParamFetcher.password_keywords):
                    self.password_params.add(input_name)

                # if the name contains a login keyword, add it to login parameters set
                elif any(keyword.lower() in input_name.lower() for keyword in ParamFetcher.login_keywords):
                    self.login_params.add(input_name)

            # if both login and password parameters are found, it is likely a login form
            if self.login_params and self.password_params:
                Logger.verbose(
                    f"Found a possible login form with action: {action}")
                return (self.login_params, self.password_params, self.all_params)
