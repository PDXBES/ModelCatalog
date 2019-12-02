from generic_object import GenericObject
from config import Config
try:
    from typing import List, Any
except:
    pass


class LinkResults(GenericObject):
    def __init__(self, config):
        # type: (Config) -> None
        self.config = config
