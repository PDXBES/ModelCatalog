# Overview info
# UI input objects are added to 'parameters' object (getParameterInfo function)
# values are extracted to individual variables by referencing 'paramaters' indices
# variable values are applied to feature class fields by referencing Update Cursor row indices
#
# Big Question - how to manage domains? - currently UI domains are hard coded in the script...
# but in theory we could grab those values from lookup tables - this could determine whether...
# we use ID fields or fields with the actual values

# ----------------------------------------------------------------------------------------------------------------------

import arcpy
from model_catalog import ModelCatalog
from model import Model
from model_catalog_data_io import ModelCatalogDataIO
from simulation_data_io import SimulationDataIO
from model_data_io import ModelDataIO
import getpass
import datetime
from config import Config



class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Model Catalog tools"
        self.alias = ""

        # List of tool classes associated with this toolbox
        self.tools = [EMGAATS_Model_Registration]


class EMGAATS_Model_Registration(object):
    def __init__(self):
        self.label = "EMGAATS Model Registration"
        self.description = "Tool for registering EMGAATS derived models"
        self.config = Config()
        self.model_catalog = ModelCatalog(self.config)
        self.model = Model(self.config)
        self.modelcatalogdataio = ModelCatalogDataIO(self.config)

        self.dummy_model_calibration_file_path = self.config.dummy_model_calibration_file_path
        self.dummy_model_alteration_file_path = self.config.dummy_model_alteration_file_path


#        self.canRunInBackground = True

    def getParameterInfo(self):
        """Define parameter definitions"""

        project_no = arcpy.Parameter(
            displayName="Project Number",
            name="project_number",
            datatype="GPString",
            parameterType="Required",
            direction="Input")

        model_dir = arcpy.Parameter(
            displayName="Model Directory",
            name="model_directory",
            datatype="DEWorkspace",
            parameterType="Required",
            direction="Input")

        model_dir.filter.list = ["File System", "Local Database"]  # review

        project_type = arcpy.Parameter(
            displayName="Project Type",
            name="project_type",
            datatype="GPString",
            parameterType="Required",
            direction="Input",
            multiValue=True)

        project_type.filter.type = "ValueList"
        project_type.filter.list = self.config.proj_type.values()

        project_phase = arcpy.Parameter(
            displayName="Project Phase",
            name="project_phase",
            datatype="GPString",
            parameterType="Required",
            direction="Input")

        project_phase.filter.type = "ValueList"
        project_phase.filter.list = self.config.proj_phase.values()

        model_purpose = arcpy.Parameter(
            displayName="Model Purpose",
            name="model_purpose",
            datatype="GPString",
            parameterType="Required",
            direction="Input")

        model_purpose.filter.type = "ValueList"
        model_purpose.filter.list = self.config.model_purpose.values()

        model_status = arcpy.Parameter(
            displayName="Model Status",
            name="model_status",
            datatype="GPString",
            parameterType="Required",
            direction="Input")

        model_status.filter.type = "ValueList"
        model_status.filter.list = ["Working", "Final"]

        model_calibration_file = arcpy.Parameter(
            displayName="Model Calibration File",
            name="model_calibration_file",
            datatype="DEFile",
            parameterType="Required",
            direction="Input")
        model_calibration_file.enabled = False
        model_calibration_file.value = self.dummy_model_calibration_file_path
        model_calibration_file.filter.list = ['xls', 'xlsx', 'docx', 'doc', 'txt']

        model_alterations = arcpy.Parameter(
            displayName="Model Alterations",
            name="model_alterations",
            datatype="GPValueTable",
            parameterType="Optional",
            direction="Input",
            multiValue=True)
        model_alterations.columns = [['String', 'Alteration Type']]
        model_alterations.filters[0].list = self.config.model_alteration.values()

        model_alteration_file = arcpy.Parameter(
            displayName="Model Alterations File",
            name="model_alteration_file",
            datatype="DEFile",
            parameterType="Required",
            direction="Input")
        model_alteration_file.enabled = False
        model_alteration_file.value = self.dummy_model_alteration_file_path
        model_alteration_file.filter.list = ['xls', 'xlsx', 'docx', 'doc', 'txt']

        params = [project_no, model_dir, project_type, project_phase, model_purpose,
                  model_calibration_file, model_status, model_alterations, model_alteration_file]
        return params

    def isLicensed(self):
        return True # tool can be executed

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""

        # Enables calibration file field if an alteration is added
        if parameters[4].valueAsText == "Calibration":
            if parameters[5].enabled == False:
                parameters[5].enabled = True
                parameters[5].value = ""
        else:
            parameters[5].enabled = False
            parameters[5].value = self.dummy_model_calibration_file_path

        # Checks that alteration added is not a duplicate
        if parameters[7].values is not None:
           number_of_values = len(parameters[7].values)
           if number_of_values > 1 and parameters[7].values[-1] in parameters[7].values[0:number_of_values-1]:
                parameters[7].values = parameters[7].values[0:number_of_values-1]

        # Enables alteration file field if an alteration is added
        if parameters[7].altered and parameters[7].valueAsText is not None:
            if parameters[8].enabled == False:
                parameters[8].enabled = True
                parameters[8].value = ""
        else:
            parameters[8].enabled = False
            parameters[8].value = self.dummy_model_alteration_file_path


    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):

        model_id = self.modelcatalogdataio.retrieve_current_model_id()
        self.model.model_id = model_id
        self.model.parent_model_id = 0
        self.model.model_request_id = 0
        self.model.project_phase_id = self.config.proj_phase_id[parameters[3].valueAsText]
        self.model.engine_type_id = 1
        self.model.create_date = datetime.datetime.today()
        self.model.deploy_date = None #TODO NEEDS TO BE EXTRACTED FROM CONFIG FILE
        self.model.run_date = None #TODO NEEDS TO BE EXTRACTED FROM CONFIG FILE
        self.model.extract_date = None #TODO NEEDS TO BE EXTRACTED FROM CONFIG FILE
        self.model.created_by = getpass.getuser()
        self.model.model_path = parameters[1].valueAsText
        self.model.project_type_id = self.config.proj_type_id[parameters[2].valueAsText]
        self.model.model_purpose_id = self.config.model_purpose_id[parameters[4].valueAsText]
        self.model.model_calibration_file = parameters[5].valueAsText
        self.model.model_status_id = self.config.model_status_id[parameters[6].valueAsText]
        if parameters[7].valueAsText == None:
            self.model.model_alterations_id = 1
        else:
            self.model.model_alterations_id = self.config.model_alteration_id[parameters[7].valueAsText]
        self.model.model_alteration_file = parameters[8].valueAsText
        self.model.project_num = parameters[0].valueAsText
        self.model.valid

        self.model_catalog.add_model(self.model)
        EMGAATS_Model_Registration_function(self.model_catalog, self.config)
        return


def EMGAATS_Model_Registration_function(model_catalog, config):
    modelcatalogdataio = ModelCatalogDataIO(config)
    modeldataio = ModelDataIO(config)
    simulationdataio = SimulationDataIO(config)
    field_names = [
        "Model_ID",
        "Parent_Model_ID",
        "Model_Request_ID",
        "Project_Phase_ID",
        "Engine_Type_ID",
        "Create_Date",
        "Created_by",
        "Deploy_Date",
        "Extract_Date",
        "Run_Date",
        "Model_Path",
        "Project_Type_ID",
        "Model_Purpose_ID",
        "Model_Calibration_file",
        "Model_Status_ID",
        "Model_Alterations_ID",
        "Model_Alteration_file",
        "Project_Num"]
    model = model_catalog.models[0]
    arcpy.AddMessage("Adding Model...")
    modelcatalogdataio.add_model(model, field_names)
    arcpy.AddMessage("Model Added")
    arcpy.AddMessage("Adding Simulations...")
    model.simulations = modeldataio.read_simulations(model)
    modeldataio.add_simulations(model, modelcatalogdataio)
    arcpy.AddMessage("Simulations Added")
    arcpy.AddMessage("Writing results to RRAD")
    for simulation in model.simulations:
        arcpy.AddMessage("Adding results for simulation: " + simulation.sim_desc)
        simulationdataio.copy_area_results(simulation, model)
        simulationdataio.copy_node_results(simulation, model)
        #TODO: Flooding results not loaded during testing
        #simulationdataio.copy_node_flooding_results(simulation, model)
        simulationdataio.copy_link_results(simulation, model)
    arcpy.AddMessage("Results written to RRAD")

def main():  # runs the whole thing; takes manual input if gui = False
    config = Config()
    model = Model(config)
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
    model.model_path = "C:\Temp\C2_Rehab"
    model.project_type_id = 1
    model.model_purpose_id = 1
    model.model_calibration_file = "C:\Temp\Cal"
    model.model_status_id = 2
    model.model_alterations_id = 1
    model.model_alteration_file = "C:\Temp\BC"
    model.project_num = "E10TEST"
    model.valid = True

    model.create_date = datetime.datetime.today()
    model_catalog.add_model(model)
    EMGAATS_Model_Registration_function(model_catalog, config)


#if __name__ == '__main__':
#    main()
