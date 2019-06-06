import unittest
from businessclasses.config import Config
from businessclasses.rrad import Rrad
from dataio.rehab_data_io import RehabDataIo
from dataio.rrad_db_data_io import RradDbDataIo


test_flag = "TEST"


class CharacterizationReportIntegrationTest(unittest.TestCase):
    def setUp(self):
        self.config = Config(test_flag)
        self.rrad = Rrad(self.config)
        self.rrad_db_data_io = RradDbDataIo(self.config)
        self.rehab_data_io = RehabDataIo(self.config, self.rrad_db_data_io)

    def test_RRAD_Rehab(self):
        rehab = self.rrad.create_rehab_for_characterization(self.rrad_db_data_io)
        self.rrad_db_data_io.add_rehab(rehab, self.rehab_data_io)
