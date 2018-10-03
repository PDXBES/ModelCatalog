import arcpy
from model_catalog import ModelCatalog
from model import Model
from model_catalog_data_io import ModelCatalogDataIO
from model_data_io import ModelDataIO
from simulation_data_io import SimulationDataIO
from model_data_io import ModelDataIO
import getpass
import datetime
from config import Config

def EMGAATS_Model_Registration_function(model_catalog, config):
    # type: (ModelCatalog, Config) -> None
    modelcatalogdataio = ModelCatalogDataIO(config)
    modeldataio = ModelDataIO(config)
    simulationdataio = SimulationDataIO(config)
    model = model_catalog.models[0]
    arcpy.AddMessage("Adding Model...")
    modelcatalogdataio.add_model(model)
    arcpy.AddMessage("Model Added")
    arcpy.AddMessage("Adding Simulations...")
    model.simulations = modeldataio.read_simulations(model)
    modeldataio.add_simulations(model, modelcatalogdataio)
    arcpy.AddMessage("Simulations Added")
    if config.model_status[model.model_status_id] == "Working":
        arcpy.AddMessage("Model Status has been set to 'Working'")
        arcpy.AddMessage("No results will be added to the RRAD")
    else:
        arcpy.AddMessage("Writing results to RRAD")
        for simulation in model.simulations:
            arcpy.AddMessage("Adding results for simulation: " + simulation.sim_desc)
            arcpy.AddMessage("  Adding Area results:")
            simulationdataio.copy_area_results(simulation, model)
            arcpy.AddMessage("  Adding node results:")
            simulationdataio.copy_node_results(simulation, model)
            #TODO: Flooding results not loaded during testing
            try:
                arcpy.AddMessage("  Adding node flooding results:")
                simulationdataio.copy_node_flooding_results(simulation, model)
            except:
                arcpy.AddWarning("This results.gdb does not have a node flooding feature class.")
                arcpy.AddWarning("The results should be processed with a newer version of EMGAATS.")
            arcpy.AddMessage("  Adding link results:")
            simulationdataio.copy_link_results(simulation, model)
            arcpy.AddMessage("Results written to RRAD")

config = Config()
model = Model(config)
modeldataio = ModelDataIO(config)
model_catalog = ModelCatalog(config)
modelcatalogdataio = ModelCatalogDataIO(config)
model_id = modelcatalogdataio.retrieve_current_model_id()
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
model.model_path = r"C:\temp\Base_Calib"
model.project_type_id = 1
model.model_purpose_id = 1
model.model_calibration_file = "C:\Temp\Cal"
model.model_status_id = 1
model.model_alteration_file = "C:\Temp\BC"
model.project_num = "E10TEST"
model.valid = True
modeldataio.create_model_geometry(model)

model.create_date = datetime.datetime.today()
model_catalog.add_model(model)
EMGAATS_Model_Registration_function(model_catalog, config)