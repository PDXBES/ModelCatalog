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

    def copy_data_to_gdb(self, input_data, test_field, id_list, gdb_full_path_name):

        rename_basename = os.path.basename(input_data).split(".")[-1]
        arcpy.AddMessage(str(rename_basename) + "...")

        try:
            self.select_and_copy_feature_class(gdb_full_path_name, id_list, input_data, rename_basename, test_field)

        except:
            self.select_and_copy_table(gdb_full_path_name, id_list, input_data, rename_basename, test_field)

    def select_and_copy_table(self, gdb_full_path_name, id_list, input_data, rename_basename, test_field):
        table_view_name = "table_view_selection"
        table_view_selection = arcpy.MakeTableView_management(input_data,
                                                              table_view_name,
                                                              "{0} in ({1})".format(
                                                                  test_field,
                                                                  self.utility.format_list_for_where_clause(id_list))
                                                              )
        if arcpy.GetCount_management(table_view_selection) > 0:
            arcpy.AddMessage("...Copying table to gdb")
            arcpy.TableToGeodatabase_conversion(table_view_selection, gdb_full_path_name)
            arcpy.Rename_management(os.path.join(gdb_full_path_name, table_view_name), rename_basename)
            del table_view_selection
        else:
            pass

    def select_and_copy_feature_class(self, gdb_full_path_name, id_list, input_data, rename_basename, test_field):
        feature_layer_name = "feature_layer_selection"
        feature_layer_selection = arcpy.MakeFeatureLayer_management(input_data,
                                                                    feature_layer_name,
                                                                    "{0} in ({1})".format(
                                                                        test_field,
                                                                        self.utility.format_list_for_where_clause(
                                                                            id_list))
                                                                    )
        if arcpy.GetCount_management(feature_layer_selection) > 0:
            arcpy.AddMessage("...Copying fc to gdb")
            arcpy.FeatureClassToGeodatabase_conversion(feature_layer_name, gdb_full_path_name)
            arcpy.Rename_management(os.path.join(gdb_full_path_name, feature_layer_name), rename_basename)
            del feature_layer_selection
        else:
            pass
