import os
from model_catalog import ModelCatalog
from model import Model
from model_catalog_data_io import ModelCatalogDataIO
from model_data_io import ModelDataIO
import getpass
import datetime
from config import Config

# This allows a file without a .py extension to be imported (ESRI pyt file)
executable_path = os.path.dirname(os.path.realpath(__file__))
from imp import load_source
model_catalog_tools = load_source("ModelCatalog_tools", executable_path + "\\ModelCatalog_tools.pyt")

########################################################################################################################
print "#####Testing working status model registration.#####"
print "\n\n"
config = Config()
model = Model(config)
model_dataio = ModelDataIO(config)
model_catalog = ModelCatalog(config)
model_catalog_dataio = ModelCatalogDataIO(config)
model_id = model_catalog_dataio.retrieve_current_model_id()
model.model_id = model_id
model.parent_model_id = 555
model.model_request_id = 777
model.project_phase_id = 1
model.engine_type_id = 1
model.create_date = None
model.deploy_date = None  # TODO NEEDS TO BE EXTRACTED FROM CONFIG FILE
model.run_date = None  # TODO NEEDS TO BE EXTRACTED FROM CONFIG FILE
model.extract_date = None  # TODO NEEDS TO BE EXTRACTED FROM CONFIG FILE
model.created_by = getpass.getuser()
model.model_path = r"\\BESFIle1\CCSP\03_WP2_Planning_Support_Tools\03_RRAD\Model_Catalog\Test_Cases\Carolina_Trunk\Base_Calib"
# TODO: need 1-M for project types, write code to add project types
# TODO: need 1-M for model alterations, write code to add model alterations
model.project_type_id = 1
model.model_purpose_id = config.model_purpose_id["Calibration"]
model.model_calibration_file = "C:\Temp\Cal"
model.model_status_id = config.model_status_id["Working"]
model.model_alteration_file = "C:\Temp\BC"
model.project_num = "E10TEST"
model.valid
model_dataio.create_model_geometry(model)
model.create_date = datetime.datetime.today()

model_catalog.add_model(model)
model_catalog_tools.EMGAATS_Model_Registration_function(model_catalog, config)
print "\n\n"

########################################################################################################################
print "#####Testing final status model registration.#####"
print "\n\n"
model_catalog = ModelCatalog(config)
model_id = model_catalog_dataio.retrieve_current_model_id()
model.model_status_id = config.model_status_id["Final"]
model.valid
model_dataio.create_model_geometry(model)
model.create_date = datetime.datetime.today()

model_catalog.add_model(model)
model_catalog_tools.EMGAATS_Model_Registration_function(model_catalog, config)
print "\n\n"

########################################################################################################################
print "#####Testing invalid model registration.#####"
print "\n\n"
try:
    model_catalog = ModelCatalog(config)
    model_id = model_catalog_dataio.retrieve_current_model_id()
    model.valid
    model_dataio.create_model_geometry(model)
    model.create_date = datetime.datetime.today()
    model.model_path = r"Invalid_path"
    model_catalog.add_model(model)
    model_catalog_tools.EMGAATS_Model_Registration_function(model_catalog, config)
except:
    print("Current Model Path does not point to a valid EMGAATS model")