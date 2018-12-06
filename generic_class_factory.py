from config import Config
try:
    from typing import List, Any, Dict
except:
    pass

class GenericClassFactory():

    def __init__(self, config):
        self.config = config
        self.class_dict = None

    def create_object(self, class_type):
        return self.class_dict[class_type]

    def create_object_with_id(self, class_type, object_data_io):
        return self.class_dict[class_type].initialize_with_current_id(self.config, object_data_io)


