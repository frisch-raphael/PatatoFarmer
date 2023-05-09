from enum import Enum, auto


class WordlistOptions(Enum):
    USER = auto()  # Accepts no argument
    PASS = auto()  # Accepts one argument
    USERPASS = auto()  # Accepts one ore more argument(s)
