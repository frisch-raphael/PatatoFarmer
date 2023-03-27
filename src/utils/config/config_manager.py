import os
import json
from pony.orm import db_session
import src.models
from src.utils.logger import Logger

CONFIG_FILE_NAME = 'config.json'


class ConfigManager:
    CONFIG_FILE = 'config.json'
    DEFAULT_CONFIG = {
        'default_wordlists': []
    }

    @classmethod
    def load_config(cls):
        if not os.path.exists(cls.CONFIG_FILE):
            cls.save_config(cls.DEFAULT_CONFIG)
        with open(cls.CONFIG_FILE, 'r') as f:
            config = json.load(f)
        return config

    @classmethod
    def save_config(cls, config):
        with open(cls.CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=2)

    @classmethod
    @db_session
    def add_default_wordlist(cls, wordlist_name):
        config = cls.load_config()

        wordlist_exists = src.models.Wordlist.exists(name=wordlist_name)
        if not wordlist_exists:
            print(
                f"Wordlist '{wordlist_name}' does not exist in the database.")
            return

        if wordlist_name not in config['default_wordlists']:
            config['default_wordlists'].append(wordlist_name)
            cls.save_config(config)

    @classmethod
    def remove_default_wordlist(cls, wordlist_name):
        config = cls.load_config()

        if wordlist_name in config['default_wordlists']:
            config['default_wordlists'].remove(wordlist_name)
            cls.save_config(config)

    @classmethod
    def get_default_wordlists(cls):
        config = cls.load_config()
        return config['default_wordlists']

    @classmethod
    @db_session
    def set_default_wordlists(cls, wordlist_names: list[str] = []):
        config = cls.load_config()

        # Check if all wordlists exist in the database
        for wordlist_name in wordlist_names:
            wordlist_exists = src.models.Wordlist.exists(name=wordlist_name)
            if not wordlist_exists:
                print(
                    f"Wordlist '{wordlist_name}' does not exist in the database.")
                return

        # Set the default wordlists
        config['default_wordlists'] = wordlist_names
        try:
            cls.save_config(config)
            if wordlist_names:
                Logger.success(
                    f"Configured the following wordlists as default: {', '.join(wordlist_names)}")
            else:
                Logger.warn(
                    f"No default wordlists configured anymore")
        except:
            Logger.warn("Could not save config")
