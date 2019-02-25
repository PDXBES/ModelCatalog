import arcpy

try:
    from typing import List, Any
except:
    pass
from businessclasses.model import Model
from businessclasses.config import Config
from db_data_io import DbDataIo
from collections import OrderedDict
from object_data_io import ObjectDataIo
from businessclasses.generic_class_factory import GenericClassFactory
from businessclasses.simulation import Simulation
from businessclasses.area import Area
from model_data_io import ModelDataIo


class ModelCatalogDbDataIo(DbDataIo):
    def __init__(self, config):
        # type: (Config) -> None
        self.config = config
        self.current_id_database_table_path = self.config.model_catalog_current_id_table_sde_path
        self.workspace = "in_memory"
        self.class_factory = GenericClassFactory(self.config)
        self.class_factory.class_dict = {"model": Model, "simulation": Simulation, "area": Area}

    def retrieve_current_model_id(self):
        current_model_id = self.retrieve_current_id("model")
        return current_model_id

    def retrieve_current_simulation_id(self):
        current_simulation_id = self.retrieve_current_id("simulation")
        return current_simulation_id

    def retrieve_current_model_alteration_id(self):
        current_model_alteration_id = self.retrieve_current_id("model_alteration")
        return current_model_alteration_id

    def add_model(self, model, model_data_io):
        # type: (Model, ModelDataIo) -> None

        editor = model_data_io.start_editing_session(self.config.model_catalog_sde_path)
        try:
            self.add_object(model, Model.input_field_attribute_lookup(), self.config.model_tracking_sde_path)
            model_data_io.add_simulations(model)
            model_data_io.add_model_alterations(model)
            model_data_io.add_project_types(model)
            model_data_io.stop_editing_session(editor, True)
        except:
            model_data_io.stop_editing_session(editor, False)
            arcpy.AddMessage("DB Error while adding model. Changes rolled back.")
            raise

