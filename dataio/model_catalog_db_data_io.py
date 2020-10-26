import arcpy
from datetime import datetime

try:
    from typing import List, Any
except:
    pass
from businessclasses.model import Model
from businessclasses.config import Config
from businessclasses.model_alteration import ModelAlteration
from db_data_io import DbDataIo
from collections import OrderedDict
from object_data_io import ObjectDataIo
from businessclasses.simulation import Simulation
from businessclasses.area_results import AreaResults
from businessclasses.model_alt_bc import ModelAltBc
from businessclasses.model_alt_hydraulic import ModelAltHydraulic
from businessclasses.model_alt_hydrologic import ModelAltHydrologic
from businessclasses.project_type import ProjectType
from dataio import utility
from model_data_io import ModelDataIo
from simulation_data_io import SimulationDataIo
from businessclasses.model_catalog_exception import AppendModelAlterationsException
import sys
import os

class ModelCatalogDbDataIo(DbDataIo):
    def __init__(self, config):
        # type: (Config) -> None
        self.config = config
        self.utility = utility.Utility(self.config)
        self.current_id_database_table_path = self.config.model_catalog_current_id_table_sde_path
        self.workspace = "in_memory"

    def create_output_gdb(self, gdb_full_path_name):
        #gdb_full_path_name = self.utility.gdb_full_path_name(datetime.today(), base_folder)
        if arcpy.Exists(gdb_full_path_name):
            arcpy.AddError("gdb already exists")
            arcpy.ExecuteError()
            sys.exit("gdb already exists") #TODO - make sure this works as expected
        else:
            base_folder = os.path.dirname(gdb_full_path_name)
            gdb_name = os.path.basename(gdb_full_path_name)
            arcpy.AddMessage("Creating gdb " + str(gdb_name))
            arcpy.CreateFileGDB_management(base_folder, gdb_name)

    def retrieve_current_model_id(self):
        current_model_id = self.retrieve_current_id(Model)
        return current_model_id

    def retrieve_current_simulation_id(self):
        current_simulation_id = self.retrieve_current_id(Simulation)
        return current_simulation_id

    def retrieve_current_model_alteration_id(self):
        current_model_alteration_id = self.retrieve_current_id(ModelAlteration)
        return current_model_alteration_id

    def add_model(self, model, model_data_io, simulation_data_io):
        # type: (Model, ModelDataIo, SimulationDataIo) -> None

        editor = model_data_io.start_editing_session(self.config.model_catalog_sde_path)
        try:
            self.append_object_to_db(model, Model.input_field_attribute_lookup(), self.config.model_tracking_sde_path,
                                     self.config.model_tracking_sde_path)
            model_data_io.append_simulations(model)
            model_data_io.append_model_alterations(model)
            model_data_io.append_project_types(model)
            model_data_io.append_storage_table(model)
            model_data_io.append_director_table(model)
            arcpy.AddMessage("Adding Model Geometry Network")
            model_data_io.append_model_network(model)
            arcpy.AddMessage("Model Geometry Network Added")
            if model.write_results_to_model_catalog():
                for simulation in model.simulations:
                    simulation_data_io.append_simulation_results(simulation, model)
            else:
                arcpy.AddMessage("No simulation results will be added to the Model Catalog")

            model_data_io.write_model_registration_file(model)
            if model.model_status_id == self.config.model_status_id["Final"]:
                model_data_io.set_registered_model_to_read_only(model)
            model_data_io.stop_editing_session(editor, True)
        except:
            model_data_io.stop_editing_session(editor, False)
            arcpy.AddMessage("DB Error while adding model. Changes rolled back.")
            e = sys.exc_info()[1]
            arcpy.AddMessage(e.args[0])
            arcpy.AddMessage(e.args[1])
            arcpy.AddMessage(e.args[2])
            raise AppendModelAlterationsException

    def copy_data_to_gdb(self, model_id_list, gdb_full_path_name):
        # call copy_datum_to_gdb for each fc/table
        model_tracking = self.config.model_tracking_sde_path
        areas = self.config.geometry_areas_sde_path
        links = self.config.geometry_links_sde_path
        nodes = self.config.geometry_nodes_sde_path
        storage = self.config.storage_sde_path
        project_types = self.config.project_type_sde_path
        directors = self.config.director_sde_path
        simulations = self.config.simulation_sde_path

        arcpy.AddMessage("Copying Model Tracking")
        self.copy_datum_to_gdb(model_tracking, model_id_list, gdb_full_path_name)
        arcpy.AddMessage("Copying Model Areas")
        self.copy_datum_to_gdb(areas, model_id_list, gdb_full_path_name)
        self.copy_datum_to_gdb(links, model_id_list, gdb_full_path_name)
        self.copy_datum_to_gdb(nodes, model_id_list, gdb_full_path_name)
        self.copy_datum_to_gdb(storage, model_id_list, gdb_full_path_name)
        self.copy_datum_to_gdb(project_types, model_id_list, gdb_full_path_name)
        self.copy_datum_to_gdb(directors, model_id_list, gdb_full_path_name)
        self.copy_datum_to_gdb(simulations, model_id_list, gdb_full_path_name)

    def copy_datum_to_gdb(self, input_data, model_id_list, gdb_full_path_name):
        arcpy.AddMessage("Selecting records")
        arcpy.AddMessage(model_id_list)
        arcpy.AddMessage(input_data)
        arcpy.AddMessage(gdb_full_path_name) #gets to here
        arcpy.AddMessage(self.utility.format_list_for_where_clause(model_id_list))
        arcpy.AddMessage("Model_ID in ({0})".format(self.utility.format_list_for_where_clause(model_id_list)))

        in_memory_selection = arcpy.MakeFeatureLayer_management(input_data, "in_memory\in_memory_selection",
                                                         "Model_ID in ({0})".format(
                                                             self.utility.format_list_for_where_clause(model_id_list)))

        #arcpy.SelectLayerByAttribute_management(intermediate,
                                                #"NEW_SELECTION",
                                                #"Model_ID in ({0})".format(self.utility.format_list_for_where_clause(model_id_list)))
        arcpy.AddMessage("before describe")
        describe = arcpy.Describe(input_data)
        arcpy.AddMessage("before field mapping")
        field_mapping = self._create_field_map_for_gdb_db(input_data)

        arcpy.AddMessage("Creating in memory data")
        try:
            intermediate = arcpy.CreateFeatureclass_management("in_memory",
                                                "intermediate",
                                                describe.shapeType,
                                                input_data)
        except:
            intermediate = arcpy.CreateTable_management("in_memory",
                                         "intermediate",
                                         input_data)

        arcpy.AddMessage("Appending")
        arcpy.Append_management(input_data, intermediate, "NO_TEST", field_mapping)

        arcpy.AddMessage("Saving to gdb")
        try:
            arcpy.FeatureClassToGeodatabase_conversion(intermediate, gdb_full_path_name)
        except:
            arcpy.TableToGeodatabase_conversion(intermediate, gdb_full_path_name)