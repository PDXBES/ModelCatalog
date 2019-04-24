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
        return self.class_dict[class_type](self.config)

    def create_object_with_id(self, class_type, db_data_io):
        return self.class_dict[class_type].initialize_with_current_id(self.config, db_data_io)


