import unittest
from businessclasses.mapping_snapshot import MappingSnapshot
from dataio.mapping_snapshot_data_io import MappingSnapshotDataIo
from dataio.rrad_mapping_db_data_io import RradMappingDbDataIo
from businessclasses.config import Config
from businessclasses.simulation import Simulation
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
        self.rrad_mapping_db_data_io = RradMappingDbDataIo(self.config)

        self.mapping_snapshot_data_io = MappingSnapshotDataIo(self.config, self.rrad_mapping_db_data_io)
        self.mapping_snapshot = MappingSnapshot(self.config)

        self.mapping_snapshot.id = 3
        self.mapping_snapshot.snapshot_type_id = "Characterization"
        self.mapping_snapshot.logic = "User Defined"
        self.mapping_snapshot.requested_by = "Keith"
        self.mapping_snapshot.created_by = "Joe"

        self.simulation_1 = Simulation(self.config)
        self.simulation_1.id = 1
        self.simulation_1.sim_desc = "Simulation_1"

        self.simulation_2 = Simulation(self.config)
        self.simulation_2.id = 2
        self.simulation_2.sim_desc = "Simulation_2"
        
        self.mapping_snapshot.simulations = [self.simulation_1, self.simulation_2]

    def test_add_mapping_snapshot_called(self):
        self.rrad_mapping_db_data_io.add_mapping_snapshot(self.mapping_snapshot,
                                                          self.mapping_snapshot_data_io,
                                                          self.rrad_db_data_io,
                                                          self.rehab_data_io,
                                                          self.rrad)
