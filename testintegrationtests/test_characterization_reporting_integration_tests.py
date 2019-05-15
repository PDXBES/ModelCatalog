import unittest
from businessclasses.mapping_snapshot import MappingSnapshot
from dataio.mapping_snapshot_data_io import MappingSnapshotDataIo
from dataio.rrad_mapping_db_data_io import RradMappingDbDataIo
from businessclasses.config import Config
from businessclasses.simulation import Simulation

# This allows a file without a .py extension to be imported (ESRI pyt file)
# executable_path = os.path.dirname(os.path.realpath(__file__))
# pyt_path = os.path.abspath(os.path.join(executable_path, '..', "Mapping_tools.pyt"))
# from imp import load_source
# mapping_tools = load_source("Mapping_tools", pyt_path)

test_flag = "TEST"


class CharacterizationReportIntegrationTest(unittest.TestCase):
    def setUp(self):

        self.config = Config(test_flag)
        self.rrad_mapping_db_data_io = RradMappingDbDataIo(self.config)
        self.mapping_snapshot_data_io = MappingSnapshotDataIo(self.config, self.rrad_mapping_db_data_io)
        self.mapping_snapshot = MappingSnapshot(self.config)

        self.mapping_snapshot.id = 2
        self.mapping_snapshot.snapshot_type_id = "Characterization"
        self.mapping_snapshot.logic = "User Defined"
        self.mapping_snapshot.requested_by = "Keith"
        self.mapping_snapshot.created_by = "Joe"

        self.simulation_1 = Simulation(self.config)
        self.simulation_1.id = 1382
        self.simulation_1.sim_desc = "Simulation_1"

        self.simulation_2 = Simulation(self.config)
        self.simulation_2.id = 1384
        self.simulation_2.sim_desc = "Simulation_2"
        
        self.mapping_snapshot.simulations = [self.simulation_1, self.simulation_2]

    def test_add_mapping_snapshot_called(self):

        self.rrad_mapping_db_data_io.add_mapping_snapshot(self.mapping_snapshot, self.mapping_snapshot_data_io)
