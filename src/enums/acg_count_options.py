from enum import Enum, auto


class ArgCountOptions(Enum):
    NONE = auto()  # Accepts no argument
    UNIQUE = auto()  # Accepts one argument
    MULTIPLE = auto()  # Accepts one ore more argument(s)
