import arcpy
from businessclasses.simulation import Simulation
from dataio.db_data_io import DbDataIo
try:
    from typing import List, Any
except:
    pass
from businessclasses.config import Config
from businessclasses.area_results import AreaResults
from businessclasses.node_results import NodeResults
from businessclasses.node_flooding_results import NodeFloodingResults
from businessclasses.link_results import LinkResults
from object_data_io import ObjectDataIo


class SimulationDataIo(ObjectDataIo):
    def __init__(self, config, model_catalog_db_data_io):
        # type: (Config, DbDataIo) -> None
        self.config = config
        self.model_catalog_db_data_io = model_catalog_db_data_io

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

# TODO below this could all be probably moved to a separate class called ModelCatalogSimulationResults or something

    def copy_link_results_to_memory(self, simulation, output_table_name, model_catalog_db_data_io):
        # type: (Simulation, str, DbDataIo) -> None
        input_table = self.link_results_path(simulation)
        self.copy_results_to_memory(input_table, output_table_name, model_catalog_db_data_io, simulation,
                                    "model_catalog_link_result_id", LinkResults)


    def copy_node_results_to_memory(self, simulation, output_table_name, model_catalog_db_data_io):
        # type: (Simulation, str, DbDataIo) -> None
        input_table = self.node_results_path(simulation)
        self.copy_results_to_memory(input_table, output_table_name, model_catalog_db_data_io, simulation,
                                    "model_catalog_node_result_id", NodeResults)

    def copy_node_flooding_results_to_memory(self, simulation, output_table_name, model_catalog_db_data_io):
        # type: (Simulation, str, DbDataIo) -> None
        input_table = self.node_flooding_results_path(simulation)
        self.copy_results_to_memory(input_table, output_table_name, model_catalog_db_data_io, simulation,
                                    "model_catalog_nodef_result_id", NodeFloodingResults)

    def copy_area_results_to_memory(self, simulation, output_table_name, model_catalog_db_data_io):
        # type: (Simulation, str, DbDataIo) -> None
        input_table = self.area_results_path(simulation)
        self.copy_results_to_memory(input_table, output_table_name, model_catalog_db_data_io, simulation,
                                    "model_catalog_area_result_id", AreaResults)

    def copy_results_to_memory(self, input_table, output_table_name, model_catalog_db_data_io, simulation, id_field,
                               object_type):
        arcpy.MakeTableView_management(input_table, output_table_name)
        output_table = model_catalog_db_data_io.workspace + "\\" + output_table_name
        arcpy.CopyRows_management(output_table_name, output_table)
        arcpy.Delete_management(output_table_name)
        model_catalog_db_data_io.add_ids(output_table, id_field, object_type)
        model_catalog_db_data_io.add_parent_id(output_table, "SIMULATION_ID", simulation.id)

    def append_area_results_to_db(self, area_results, model_catalog_db_data_io):
            field_attribute_lookup = AreaResults.input_field_attribute_lookup()
            template_table_path = self.config.results_area_sde_path
            target_path = self.config.results_area_sde_path
            model_catalog_db_data_io.append_objects_to_db(area_results, field_attribute_lookup, template_table_path, target_path)

    def append_simulation_results(self, simulation, model):
        # TODO add tests for the new if statement
        if simulation.required_for_model_catalog(model):
            area_results_table_name = "area_results_table_name"
            link_results_table_name = "link_results_table_name"
            node_results_table_name = "node_results_table_name"
            node_flooding_results_table_name = "node_flooding_results_table_name"

            area_results_table = self.model_catalog_db_data_io.workspace + "\\" + area_results_table_name
            link_results_table = self.model_catalog_db_data_io.workspace + "\\" + link_results_table_name
            node_results_table = self.model_catalog_db_data_io.workspace + "\\" + node_results_table_name
            node_flooding_results_table = self.model_catalog_db_data_io.workspace + "\\" + node_flooding_results_table_name

            self.copy_area_results_to_memory(simulation, area_results_table_name, self.model_catalog_db_data_io)
            self.copy_link_results_to_memory(simulation, link_results_table_name, self.model_catalog_db_data_io)
            self.copy_node_results_to_memory(simulation, node_results_table_name, self.model_catalog_db_data_io)
            self.copy_node_flooding_results_to_memory(simulation, node_flooding_results_table_name, self.model_catalog_db_data_io)

            self.model_catalog_db_data_io.append_table_to_db(area_results_table, self.config.results_area_sde_path)
            self.model_catalog_db_data_io.append_table_to_db(link_results_table, self.config.results_link_sde_path)
            self.model_catalog_db_data_io.append_table_to_db(node_results_table, self.config.results_node_sde_path)
            self.model_catalog_db_data_io.append_table_to_db(node_flooding_results_table, self.config.results_node_flooding_sde_path)

            arcpy.AddMessage("Simulation: " + simulation.sim_desc + " Results written to Model Catalog.")
            arcpy.Delete_management(area_results_table)
            arcpy.Delete_management(link_results_table)
            arcpy.Delete_management(node_results_table)
            arcpy.Delete_management(node_flooding_results_table)
        else:
            arcpy.AddMessage("Simulation: " + simulation.sim_desc + " is not required for the Model Catalog")





