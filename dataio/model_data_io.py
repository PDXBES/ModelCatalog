import os
import arcpy
import json
import traceback
from businessclasses.config import Config
from stat import S_IREAD, S_IRGRP, S_IROTH, S_IWRITE, S_IWGRP, S_IWOTH
import xml.etree.ElementTree as ET
try:
    from typing import List, Any
except:
    pass
from businessclasses.model import Model
from businessclasses.simulation import Simulation
from businessclasses.node_geometry import NodeGeometry
from businessclasses.link_geometry import LinkGeometry
from businessclasses.area_geometry import AreaGeometry
from businessclasses.storage import Storage
from businessclasses.director import Director
from businessclasses.model_catalog_exception import InvalidModelException
from businessclasses.model_catalog_exception import InvalidModelPathException
from businessclasses.model_catalog_exception import InvalidModelPurposeException
from businessclasses.model_catalog_exception import InvalidModelRegistrationFileException
from db_data_io import DbDataIo
from object_data_io import ObjectDataIo
from businessclasses.model_alt_bc import ModelAltBc
from businessclasses.model_alt_hydraulic import ModelAltHydraulic
from businessclasses.model_alt_hydrologic import ModelAltHydrologic
from businessclasses.model_alteration import ModelAlteration
from businessclasses.project_type import ProjectType

class ModelDataIo(ObjectDataIo):
    def __init__(self, config, db_data_io):
        # type: (Config, DbDataIo) -> None
        self.config = config
        self.db_data_io = db_data_io

    def create_model_geometry(self, model):
        if model.valid:
            model_name = "Links"
            model_in = model.model_path + "\\" + "EmgaatsModel.gdb" + "\\Network\\" + model_name
            model_out = "in_memory\\" + model_name
            arcpy.Dissolve_management(model_in, model_out, "", "", "MULTI_PART")
            cursor = arcpy.da.SearchCursor(model_out, ["Shape@"])
            for row in cursor:
                geometry = row[0]
                model.model_geometry = geometry
            del cursor
            arcpy.Delete_management(model_out)
        else:
            raise InvalidModelException

    def read_simulations(self, model):
        # type: (Model) -> List[Simulation]
        simulations = []  # type: List[Simulation]
        simulation_descriptions = os.walk(model.simulation_folder_path()).next()[1]
        for simulation_description in simulation_descriptions:
            simulation = Simulation.initialize_with_current_id(self.config, self.db_data_io)
            simulation.model_path = model.model_path
            if simulation_description in self.config.standard_simulation_names():
                simulation_desc_parts = simulation_description.split("-")
                storm_type = simulation_desc_parts[0][0]
                # TODO add test for logic regarding for storms that do not follow the naming convention of
                #  design storms (D + storm_name)
                if simulation_desc_parts[0][1:] in self.config.emgaats_design_storms_with_D:
                    storm_name = simulation_desc_parts[0][1:]
                    storm_type = "D"
                elif simulation_desc_parts[0] in self.config.emgaats_design_storms_without_D:
                    storm_name = simulation_desc_parts[0]
                    storm_type = "D"
                else:
                    storm_name = simulation_desc_parts[0]
                    storm_type = "H"

                if len(simulation_desc_parts) == 1:
                    dev_scenario = "EX"
                else:
                    dev_scenario = simulation_desc_parts[1]
            else:
                dev_scenario = "EX"
                storm_type = "U"
                storm_name = "User-defined"
            simulation.storm_id = self.config.storm_id[(storm_name, storm_type)]
            simulation.dev_scenario_id = self.config.dev_scenario_id[dev_scenario]
            simulation.sim_desc = simulation_description
            simulations.append(simulation)
        return simulations

    def append_simulation(self, model_id, simulation):
        # type: (int, Simulation) -> None
        self.append_object_to_db(model_id, simulation, simulation.input_field_attribute_lookup, self.config.simulation_sde_path)

    def append_simulations(self, model):
        # type: (Model) -> None
        for simulation in model.simulations:
            self.append_simulation(model.id, simulation)

    def append_model_alteration(self, model_id, model_alteration):
        # type: (int, ModelAlteration) -> None
        if type(model_alteration) == ModelAltBc:
            self.append_object_to_db(model_id, model_alteration, model_alteration.input_field_attribute_lookup, self.config.model_alt_bc_sde_path)
        elif type(model_alteration) == ModelAltHydrologic:
            self.append_object_to_db(model_id, model_alteration, model_alteration.input_field_attribute_lookup, self.config.model_alt_hydrologic_sde_path)
        elif type(model_alteration) == ModelAltHydraulic:
            self.append_object_to_db(model_id, model_alteration, model_alteration.input_field_attribute_lookup, self.config.model_alt_hydraulic_sde_path)

    def append_model_alterations(self, model):
        # type: (Model) -> None
        for model_alteration in model.model_alterations:
            self.append_model_alteration(model.id, model_alteration)

    def append_project_type(self, model_id, project_type):
        # type: (int, ProjectType) -> None
        self.append_object_to_db(model_id, project_type, project_type.input_field_attribute_lookup,
                                 self.config.project_type_sde_path)

    def append_project_types(self, model):
        # type: (Model) -> None
        for project_type in model.project_types:
            self.append_project_type(model.id, project_type)

    def append_model_network(self, model):
        input_gdb = model.model_path + "\\" + "EmgaatsModel.gdb"

        input_table = input_gdb + "\\" + "nodes"
        output_table_name = "in_memory_table_nodes"
        output_table = self.db_data_io.workspace + "\\" + output_table_name
        id_field = "model_catalog_node_id"
        object_type = NodeGeometry
        self.copy_geometry_to_memory(input_table, output_table_name, self.db_data_io, model, id_field, object_type)
        self.db_data_io.append_table_to_db(output_table, self.config.geometry_nodes_sde_path)

        input_table_links = input_gdb + "\\" + "links"
        output_table_name_links = "in_memory_table_links"
        output_table_links = self.db_data_io.workspace + "\\" + output_table_name_links
        id_field = "model_catalog_link_id"
        object_type = LinkGeometry
        self.copy_geometry_to_memory(input_table_links, output_table_name_links, self.db_data_io, model, id_field,
                                     object_type)
        self.db_data_io.append_table_to_db(output_table_links, self.config.geometry_links_sde_path)

        input_table_areas = input_gdb + "\\" + "areas"
        output_table_name_areas = "in_memory_table_areas"
        output_table_areas = self.db_data_io.workspace + "\\" + output_table_name_areas
        id_field = "model_catalog_area_id"
        object_type = AreaGeometry
        self.copy_geometry_to_memory(input_table_areas, output_table_name_areas, self.db_data_io, model, id_field,
                                     object_type)
        self.db_data_io.append_table_to_db(output_table_areas, self.config.geometry_areas_sde_path)

        arcpy.Delete_management(output_table)
        arcpy.Delete_management(output_table_links)
        arcpy.Delete_management(output_table_areas)

    def append_storage_table(self, model):
        input_gdb = model.model_path + "\\" + "EmgaatsModel.gdb"
        input_table = input_gdb + "\\" + "Storages"
        output_table_name = "in_memory_table_storage"
        output_table = self.db_data_io.workspace + "\\" + output_table_name
        id_field = "model_catalog_storage_id"
        object_type = Storage
        self.copy_geometry_to_memory(input_table, output_table_name, self.db_data_io, model, id_field, object_type)
        self.db_data_io.append_table_to_db(output_table, self.config.storage_sde_path)

        arcpy.Delete_management(output_table)

    def append_director_table(self, model):
        input_gdb = model.model_path + "\\" + "EmgaatsModel.gdb"
        input_table = input_gdb + "\\" + "Directors"
        output_table_name = "in_memory_table_director"
        output_table = self.db_data_io.workspace + "\\" + output_table_name
        id_field = "model_catalog_director_id"
        object_type = Director
        self.copy_geometry_to_memory(input_table, output_table_name, self.db_data_io, model, id_field, object_type)
        self.db_data_io.append_table_to_db(output_table, self.config.director_sde_path)

        arcpy.Delete_management(output_table)

    def copy_geometry_to_memory(self, input_table, output_table_name, db_data_io, model, id_field, object_type):
        db_data_io.copy_to_memory(input_table, output_table_name)
        output_table = db_data_io.workspace + "\\" + output_table_name
        db_data_io.add_ids(output_table, id_field, object_type)
        db_data_io.add_parent_id(output_table, "MODEL_ID", model.id)

    def set_registered_model_to_read_only(self, model):
        # "https://stackoverflow.com/questions/28492685/change-file-to-read-only-mode-in-python"

        if model.valid_emgaats_model_structure() == True:
            model_path = model.model_path
            for root, directories, filenames in os.walk(model_path):
                for filename in filenames:
                    filepath = os.path.join(root, filename)
                    os.chmod(filepath, S_IREAD | S_IRGRP | S_IROTH)
        else:
            raise InvalidModelPathException

    def write_model_registration_file(self, model):
        # https://stackoverflow.com/questions/12309269/how-do-i-write-json-data-to-a-file

        # check that a registration file does not already exist - in different function?
        # TODO Model Status - done in model_catalog_db_data_io.add_model?
        model_registration_data = {"id": model.id,
                                   "create_date": model.create_date.strftime("%d-%b-%Y (%H:%M:%S.%f)"),
                                   "model_purpose_id": model.model_purpose_id,
                                   "model_purpose": self.config.model_purpose[model.model_purpose_id]}

        file_path = model.model_path
        file_name = "model_registration.json"
        model_registration_file = os.path.join(file_path, file_name)
        try:
            with open(model_registration_file, 'w') as outfile:
                json.dump(model_registration_data, outfile)
        except:
            traceback.print_exc()
            raise Exception
        #TODO figure out how to make this testable

    def delete_model_registration_file(self, model_path):
        file_name = "model_registration.json"
        model_registration_file = os.path.join(model_path, file_name)
        if os.path.isfile(model_registration_file):
            os.remove(model_registration_file)
        else:
            raise InvalidModelRegistrationFileException

    #TODO: split this function to take a model registration path and be more "generalic"?
    def read_model_id_from_model_registration_file(self, model):
        registration_file = os.path.join(model.parent_model_path, "model_registration.json")
        with open(registration_file) as json_file:
            data = json.load(json_file)
            return data["id"]

    def read_model_purpose_from_model_registration_file(self, model):
        valid_model_purpose_values = self.config.model_purpose_id.keys()
        registration_file = os.path.join(model.parent_model_path, "model_registration.json")
        with open(registration_file) as json_file:
            data = json.load(json_file)
            if data["model_purpose"] in valid_model_purpose_values:
                return data["model_purpose"]
            else:
                raise InvalidModelPurposeException(None)

    def read_root_from_config_file(self, model):
        tree = ET.parse(model.config_file_path)
        root = tree.getroot()
        return root

    def read_extraction_date_from_emgaats_config_file(self, model):
        root = self.read_root_from_config_file(model)
        extract_date = root.find('ExtractionDateTime').text
        return extract_date

# TODO: create reads for deploy date and run date (note to change run date to results extracted date - verify)
# TODO: finish the below functions

    def read_deploy_date_and_results_extracted_date_from_emgaats_config_file(self, model):
        root = self.read_root_from_config_file(model)
        #deploy_date = root[#].text  # fragile - indexing could change
        #return deploy_date
        pass
    #get list of emgaats data for all simulations in the folder
    #will return the list
    #awaiting changes from Arnel

    def read_run_date_from_emgaats_config_file(self, model):
        root = self.read_root_from_config_file(model)
        #run_date = root[#].text  # fragile - indexing could change
        #return run_date
        pass
    #similar to above 2 functions

    def set_model_to_read_write(self, model):
        # "https://stackoverflow.com/questions/28492685/change-file-to-read-only-mode-in-python"

        model_path = model.model_path
        for root, directories, filenames in os.walk(model_path):
            for filename in filenames:
                filepath = os.path.join(root, filename)
                os.chmod(filepath, S_IWRITE | S_IWGRP | S_IWOTH )

    def set_model_copy_to_read_write(self, model_path):
        # "https://stackoverflow.com/questions/28492685/change-file-to-read-only-mode-in-python"

        for root, directories, filenames in os.walk(model_path):
            for filename in filenames:
                filepath = os.path.join(root, filename)
                os.chmod(filepath, S_IWRITE | S_IWGRP | S_IWOTH )

    def check_model_is_read_only(self, model):
        model_path = model.model_path
        for root, directories, filenames in os.walk(model_path):
            for filename in filenames:
                filepath = os.path.join(root, filename)
                if os.access(filepath, os.W_OK):
                    return False

        return True






