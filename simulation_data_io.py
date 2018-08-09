import arcpy
from model import Model
from simulation import Simulation
from typing import List
from config import Config


class SimulationDataIO:
    def __init__(self, config):
        # type: (Config) -> None
        self.config = config

#TODO: add test for in_path
    def copy_feature_class_results(self, simulation, model,
                                   model_results_feature_class_path,
                                   rrad_results_feature_class_path):
        # type: (Simulation, Model, str, str) -> None
        field_names, field_names_extended = self.modify_field_names_for_RRAD(model_results_feature_class_path)
        cursor = arcpy.da.SearchCursor(model_results_feature_class_path, field_names)
        row_number = 0
        for row in cursor:
            if row_number%100 == 0:
                print row_number
            row_number += 1
            insert = arcpy.da.InsertCursor(rrad_results_feature_class_path, field_names_extended)
            insert_row = row + (model.model_id,
                                simulation.storm_id,
                                simulation.scenario_id,
                                0)
            insert.insertRow(insert_row)
            pass

    def modify_field_names_for_RRAD(self, model_results_feature_class_path):
        # type: (str) -> (List[str], List[str])
        fields = arcpy.ListFields(model_results_feature_class_path)
        field_names = []
        field_names_extended = []
        for field in fields:
            if field.name == "SHAPE_Area" or field.name == "SHAPE_Length" or field.name == "OBJECTID" or field.name == "SHAPE":
                pass
            else:
                field_names.append(field.name)
                #TODO correct horrible horrible hack to accomadate SDE field length issue
                field_names_extended.append(field.name[0:31])
        field_names_extended.append("SHAPE@")
        field_names_extended.append("Model_ID")
        field_names_extended.append("Storm_ID")
        field_names_extended.append("Dev_Scenario_ID")
        field_names_extended.append("Is_Orphaned")
        field_names.append("SHAPE@")
        return field_names, field_names_extended

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

    def copy_area_results(self, simulation, model):
        # type: (Simulation, Model) -> None
        model_area_results_path = self.area_results_path(simulation)
        rrad_area_results_path = self.config.area_results_sde_path
        self.copy_feature_class_results(simulation, model, model_area_results_path, rrad_area_results_path)

    def copy_link_results(self, simulation, model):
        # type: (Simulation, Model) -> None
        model_link_results_path = self.link_results_path(simulation)
        rrad_link_results_path = self.config.link_results_sde_path
        self.copy_feature_class_results(simulation, model, model_link_results_path, rrad_link_results_path)

    def copy_node_results(self, simulation, model):
        # type: (Simulation, Model) -> None
        model_node_results_path = self.node_results_path(simulation)
        rrad_node_results_path = self.config.node_results_sde_path
        self.copy_feature_class_results(simulation, model, model_node_results_path, rrad_node_results_path)

    def copy_node_flooding_results(self, simulation, model):
        # type: (Simulation, Model) -> None
        model_node_flooding_results_path = self.node_flooding_results_path(simulation)
        rrad_node_flooding_results_path = self.config.flooding_results_sde_path
        self.copy_feature_class_results(simulation, model, model_node_flooding_results_path,
                                        rrad_node_flooding_results_path)

    def read_simulations(self, model):
        # type: (Model) -> None
        pass