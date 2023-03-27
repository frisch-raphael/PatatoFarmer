from typing import Optional


class WordlistDto:
    def __init__(self, type: Optional[str] = None,
                 path: Optional[str] = None,
                 name: Optional[str] = None,
                 hash: Optional[str] = None):
        self.type = type
        self.path = path
        self.name = name
        self.hash = hash
