from businessclasses.rehab import Rehab
import datetime


class Rrad:

    def __init__(self, config):
        self.config = config

    def create_rehab_for_characterization(self, rrad_db_data_io):
        rehab = Rehab.initialize_with_current_id(self.config, rrad_db_data_io)
        rehab.extract_date = datetime.datetime.today()
        rehab.last_inspection_date = datetime.datetime.today()
        rehab.purpose = "Characterization"
        return rehab