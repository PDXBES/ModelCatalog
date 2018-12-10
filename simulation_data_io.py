import arcpy
from model import Model
from simulation import Simulation
try:
    from typing import List, Any
except:
    pass
from config import Config
from model_catalog_db_data_io import ModelCatalogDbDataIo


class SimulationDataIO:
    def __init__(self, config, model_catalog_db_data_io):
        # type: (Config, ModelCatalogDbDataIo) -> None
        self.config = config
        self.model_catalog_db_data_io = model_catalog_db_data_io

    def _id_to_field_map(self, simulation):
        id_to_db_field_mapping = [(simulation.id, "Simulation_ID")]
        return id_to_db_field_mapping

    def area_results_path(self, simulation):
        # type: (Simulation) -> str
        sim_path = simulation.path()
        area_results_path = sim_path + "\\" + "results.gdb" + "\\" + "AreaResults"
        return area_results_path

    def link_results_path(self, simulation):
        # type: (Simulation) -> str
        sim_path = simulation.path()
        link_results_path = sim_path + "\\" + "results.gdb" + "\\" + "LinkResults"
        return link_results_path

    def node_results_path(self, simulation):
        # type: (Simulation) -> str
        sim_path = simulation.path()
        node_results_path = sim_path + "\\" + "results.gdb" + "\\" + "NodeResults"
        return node_results_path

    def node_flooding_results_path(self, simulation):
        # type: (Simulation) -> str
        sim_path = simulation.path()
        node_flooding_results_path = sim_path + "\\" + "results.gdb" + "\\" + "NodeFloodingResults"
        return node_flooding_results_path

    def copy_area_results(self, simulation):
        # type: (Simulation) -> None
        model_area_results_path = self.area_results_path(simulation)
        rrad_area_results_path = self.config.area_results_sde_path
        id_to_db_field_mapping = self._id_to_field_map(simulation)
        self.model_catalog_db_data_io.copy(model_area_results_path, rrad_area_results_path, None, id_to_db_field_mapping)

    def copy_link_results(self, simulation):
        # type: (Simulation) -> None
        model_link_results_path = self.link_results_path(simulation)
        rrad_link_results_path = self.config.link_results_sde_path
        id_to_db_field_mapping = self._id_to_field_map(simulation)
        self.model_catalog_db_data_io.copy(model_link_results_path, rrad_link_results_path, None, id_to_db_field_mapping)

    def copy_node_results(self, simulation):
        # type: (Simulation) -> None
        model_node_results_path = self.node_results_path(simulation)
        rrad_node_results_path = self.config.node_results_sde_path
        id_to_db_field_mapping = self._id_to_field_map(simulation)
        self.model_catalog_db_data_io.copy(model_node_results_path, rrad_node_results_path, None, id_to_db_field_mapping)

    def copy_node_flooding_results(self, simulation):
        # type: (Simulation) -> None
        model_node_flooding_results_path = self.node_flooding_results_path(simulation)
        rrad_node_flooding_results_path = self.config.flooding_results_sde_path
        id_to_db_field_mapping = self._id_to_field_map(simulation)
        self.model_catalog_db_data_io.copy(model_node_flooding_results_path, rrad_node_flooding_results_path, None, id_to_db_field_mapping)

    def copy_area_results_to_memory(self, simulation, output_table_name):
        input_table = self.area_results_path(simulation)
        parent_id_to_db_field_mapping = self._id_to_field_map(simulation)
        self.model_catalog_db_data_io.copy_to_memory(input_table, output_table_name, parent_id_to_db_field_mapping)
