import arcpy
from businessclasses.simulation import Simulation
from dataio.rrad_db_data_io import RradDbDataIo
try:
    from typing import List, Any
except:
    pass
from businessclasses.config import Config
from model_catalog_db_data_io import ModelCatalogDbDataIo
from businessclasses.area import Area
from object_data_io import ObjectDataIo

class SimulationDataIo(ObjectDataIo):
    def __init__(self, config, model_catalog_db_data_io):
        # type: (Config, ModelCatalogDbDataIo) -> None
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

# TODO below this could all be probably moved to a separate class called RradSimulationResults or something

    def copy_link_results_to_memory(self, simulation, output_table_name, rrad_db_data_io):
        # type: (Simulation, str, RradDbDataIo) -> None
        input_table = self.link_results_path(simulation)
        self.copy_results_to_memory(input_table, output_table_name, rrad_db_data_io, simulation, "rrad_link_id", "link")


    def copy_node_results_to_memory(self, simulation, output_table_name, rrad_db_data_io):
        # type: (Simulation, str, RradDbDataIo) -> None
        input_table = self.node_results_path(simulation)
        self.copy_results_to_memory(input_table, output_table_name, rrad_db_data_io, simulation, "rrad_node_id", "node")

    def copy_node_flooding_results_to_memory(self, simulation, output_table_name, rrad_db_data_io):
        # type: (Simulation, str, RradDbDataIo) -> None
        input_table = self.node_flooding_results_path(simulation)
        self.copy_results_to_memory(input_table, output_table_name, rrad_db_data_io, simulation, "rrad_node_flooding_id",
                                    "node_flooding")

    def copy_area_results_to_memory(self, simulation, output_table_name, rrad_db_data_io):
        # type: (Simulation, str, RradDbDataIo) -> None
        input_table = self.area_results_path(simulation)
        rrad_db_data_io.copy_to_memory(input_table, output_table_name)

    def copy_results_to_memory(self, input_table, output_table_name, rrad_db_data_io, simulation, id_field,
                               object_type):
        # copy to memory is the original in case we need to revert
        rrad_db_data_io.copy_to_memory(input_table, output_table_name)
        #rrad_db_data_io.append_to_memory(input_table, output_table_name)
        output_table = rrad_db_data_io.workspace + "\\" + output_table_name
        rrad_db_data_io.add_ids(output_table, id_field, object_type)
        rrad_db_data_io.add_parent_id(output_table, "Simulation_ID", simulation.id)
        #TODO: append to memory adds new block of records but
        #TODO: add_parent_id runs after this on ALL records in the table - fix this

    def append_area_results_to_db(self, area_results, rrad_db_data_io):
            field_attribute_lookup = Area.input_field_attribute_lookup()
            template_table_path = self.config.area_results_sde_path
            target_path = self.config.area_results_sde_path
            rrad_db_data_io.append_objects_to_db(area_results, field_attribute_lookup, template_table_path, target_path)

    #option create new function that appends simulations in a for loop and have the edit sessions cover the for loop
    def append_simulation_results(self, simulation, model, rrad_db_data_io):
        # TODO add tests for the new if statement
        if simulation.required_for_rrad(model):
            link_results_table_name = "link_results_table_name"
            node_results_table_name = "node_results_table_name"
            node_flooding_results_table_name = "node_flooding_results_table_name"

            link_results_table = rrad_db_data_io.workspace + "\\" + link_results_table_name
            node_results_table = rrad_db_data_io.workspace + "\\" + node_results_table_name
            node_flooding_results_table = rrad_db_data_io.workspace + "\\" + node_flooding_results_table_name

            simulation.create_areas(self, rrad_db_data_io)
            self.copy_link_results_to_memory(simulation, link_results_table_name, rrad_db_data_io)
            self.copy_node_results_to_memory(simulation, node_results_table_name, rrad_db_data_io)
            self.copy_node_flooding_results_to_memory(simulation, node_flooding_results_table_name, rrad_db_data_io)

            editor = self.start_editing_session(self.config.RRAD_sde_path)
            try:
                rrad_db_data_io.append_table_to_db(link_results_table, self.config.link_results_sde_path)
                rrad_db_data_io.append_table_to_db(node_results_table, self.config.node_results_sde_path)
                rrad_db_data_io.append_table_to_db(node_flooding_results_table, self.config.node_flooding_results_sde_path)
                self.append_area_results_to_db(simulation.areas, rrad_db_data_io)
                self.stop_editing_session(editor, True)
                arcpy.AddMessage("Results written to RRAD.")
            except:
                self.stop_editing_session(editor, False)

                arcpy.AddMessage("DB Error while adding simulation results. Changes rolled back.")
                raise
            finally:
                arcpy.Delete_management(link_results_table)
                arcpy.Delete_management(node_results_table)
                arcpy.Delete_management(node_flooding_results_table)
        else:
            arcpy.AddMessage("Simulation: " + simulation.sim_desc + " is not required for the RRAD.")

    #TODO: consider moving this out to model
    def append_all_simulation_results(self, model,rrad_db_data_io):

        link_results_table_name = "link_results_table_name"
        node_results_table_name = "node_results_table_name"
        node_flooding_results_table_name = "node_flooding_results_table_name"

        link_results_table = rrad_db_data_io.workspace + "\\" + link_results_table_name
        node_results_table = rrad_db_data_io.workspace + "\\" + node_results_table_name
        node_flooding_results_table = rrad_db_data_io.workspace + "\\" + node_flooding_results_table_name

        self.create_simulation_results_tables_in_memory(link_results_table, link_results_table_name, model,
                                                        node_flooding_results_table, node_flooding_results_table_name,
                                                        node_results_table, node_results_table_name, rrad_db_data_io)

        editor = self.start_editing_session(self.config.RRAD_sde_path)
        try:
            rrad_db_data_io.append_table_to_db(link_results_table, self.config.link_results_sde_path)
            rrad_db_data_io.append_table_to_db(node_results_table, self.config.node_results_sde_path)
            rrad_db_data_io.append_table_to_db(node_flooding_results_table,self.config.node_flooding_results_sde_path)

            for simulation in model.simulations:
                self.append_area_results_to_db(simulation.areas, rrad_db_data_io)

            arcpy.Delete_management(link_results_table)
            arcpy.Delete_management(node_results_table)
            arcpy.Delete_management(node_flooding_results_table)

            self.stop_editing_session(editor, True)
            arcpy.AddMessage("Results written to RRAD.")
        except:
            self.stop_editing_session(editor, False)

            arcpy.AddMessage("DB Error while adding simulation results. Changes rolled back.")
            raise

    def create_simulation_results_tables_in_memory(self, link_results_table, link_results_table_name, model,
                                                   node_flooding_results_table, node_flooding_results_table_name,
                                                   node_results_table, node_results_table_name, rrad_db_data_io):
        first_sim_to_rrad = True
        for simulation in model.simulations:
            if simulation.required_for_rrad(model):

                link_results_table_name_intermediate = "link_results_table_name_intermediate"
                link_results_table_intermediate = rrad_db_data_io.workspace + "\\" + link_results_table_name_intermediate

                node_results_table_name_intermediate = "node_results_table_name_intermediate"
                node_results_table_intermediate = rrad_db_data_io.workspace + "\\" + node_results_table_name_intermediate

                node_flooding_results_table_name_intermediate = "node_flooding_results_table_name_intermediate"
                node_flooding_results_table_intermediate = rrad_db_data_io.workspace + "\\" + node_flooding_results_table_name_intermediate

                simulation.create_areas(self, rrad_db_data_io)

                if first_sim_to_rrad:
                    first_sim_to_rrad = False
                    self.copy_link_results_to_memory(simulation, link_results_table_name, rrad_db_data_io)
                    self.copy_node_results_to_memory(simulation, node_results_table_name, rrad_db_data_io)
                    self.copy_node_flooding_results_to_memory(simulation, node_flooding_results_table_name,
                                                              rrad_db_data_io)

                else:
                    self.copy_link_results_to_memory(simulation, link_results_table_name_intermediate, rrad_db_data_io)
                    arcpy.Append_management(link_results_table_intermediate, link_results_table)
                    arcpy.Delete_management(link_results_table_intermediate)

                    self.copy_node_results_to_memory(simulation, node_results_table_name_intermediate, rrad_db_data_io)
                    arcpy.Append_management(node_results_table_intermediate, node_results_table)
                    arcpy.Delete_management(node_results_table_intermediate)

                    self.copy_node_flooding_results_to_memory(simulation, node_flooding_results_table_name_intermediate,
                                                              rrad_db_data_io)
                    arcpy.Append_management(node_flooding_results_table_intermediate, node_flooding_results_table)
                    arcpy.Delete_management(node_flooding_results_table_intermediate)

            else:
                arcpy.AddMessage("Simulation: " + simulation.sim_desc + " is not required for the RRAD.")



