import arcpy
from businessclasses.model_catalog import ModelCatalog
from businessclasses.model import Model
from dataio.model_catalog_db_data_io import ModelCatalogDbDataIo
from dataio.simulation_data_io import SimulationDataIO
from dataio.model_data_io import ModelDataIo
import getpass
import datetime
from businessclasses import config
from businessclasses.model_catalog_exception import InvalidModelException
reload(arcpy)
reload(config)
# reload(ModelCatalog)
# reload(Model)
# reload(ModelCatalogDbDataIo)
# reload(ModelDataIo)
# reload(SimulationDataIO)

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
        self.config = config.Config()
        self.model_catalog = ModelCatalog(self.config)
        self.modelcatalogdataio = ModelCatalogDbDataIo(self.config)
        self.model_dataio = ModelDataIo(self.config, self.modelcatalogdataio)

        self.dummy_model_calibration_file_path = self.config.dummy_model_calibration_file_path
        self.dummy_model_alteration_file_path = self.config.dummy_model_alteration_file_path
        arcpy.AddMessage("Init")

#        self.canRunInBackground = True

    def getParameterInfo(self):
        """Define parameter definitions"""
        arcpy.AddMessage("Get parameter info")
        project_no = arcpy.Parameter(
            displayName="Model Analysis Tracking Number",
            name="project_number",
            datatype="GPString",
            parameterType="Required",
            direction="Input")
        project_no.value = " "
        project_no.enabled = False

        model_dir = arcpy.Parameter(
            displayName="Model Directory",
            name="model_directory",
            datatype="DEWorkspace",
            parameterType="Required",
            direction="Input")

        model_dir.filter.list = ["File System", "Local Database"]

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

        project_cip_number = arcpy.Parameter(
            displayName="CIP Number",
            name="cip_number",
            datatype="GPString",
            parameterType="Required",
            direction="Input")

        project_cip_number.enabled = False
        project_cip_number.filter.type = "ValueList"
        cip_numbers = self.config.unique_cip_numbers
        cip_numbers.append(u"None")
        project_cip_number.filter.list = cip_numbers
        project_cip_number.value = u"None"

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

        model_alterations_boundary_conditions = arcpy.Parameter(
            displayName="Model Alterations Boundary Conditions",
            name="model_alterations_boundary_conditions",
            datatype="GPValueTable",
            parameterType="Optional",
            direction="Input",
            multiValue=True)
        model_alterations_boundary_conditions.columns = [['String', 'Alteration Type']]
        model_alterations_boundary_conditions.filters[0].list = self.config.model_alt_bc.values()

        model_alterations_hydrologic = arcpy.Parameter(
            displayName="Model Alterations Hydrologic Parameters",
            name="model_alterations_hydrologic",
            datatype="GPValueTable",
            parameterType="Optional",
            direction="Input",
            multiValue=True)
        model_alterations_hydrologic.columns = [['String', 'Alteration Type']]
        model_alterations_hydrologic.filters[0].list = self.config.model_alt_hydrologic.values()

        model_alterations_hydraulic = arcpy.Parameter(
            displayName="Model Alterations Hydraulic Parameters",
            name="model_alterations_hydraulic",
            datatype="GPValueTable",
            parameterType="Optional",
            direction="Input",
            multiValue=True)
        model_alterations_hydraulic.columns = [['String', 'Alteration Type']]
        model_alterations_hydraulic.filters[0].list = self.config.model_alt_hydraulic.values()

        model_alteration_file = arcpy.Parameter(
            displayName="Model Alterations File",
            name="model_alteration_file",
            datatype="DEFile",
            parameterType="Required",
            direction="Input")
        model_alteration_file.enabled = False
        model_alteration_file.value = self.dummy_model_alteration_file_path
        model_alteration_file.filter.list = ['xls', 'xlsx', 'docx', 'doc', 'txt']


        params = [project_no, model_dir, project_type, project_phase, project_cip_number,
                  model_purpose, model_calibration_file, model_status, model_alterations_boundary_conditions,
                  model_alterations_hydrologic, model_alterations_hydraulic, model_alteration_file]
        return params

    def isLicensed(self):
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        arcpy.AddMessage("Update Parameters")

        if parameters[3].valueAsText in ("Pre Design", "Design 30", "Design 60", "Design 90"):
            if parameters[4].value == u"None":
                parameters[4].value = None
            parameters[4].enabled = True
            parameters[4].filter.list = self.config.unique_cip_numbers
            if parameters[4].value != None or parameters[4].value == u"None":
                parameters[0].value = "ARID"
                analysis_request_ids = ""
                for analysis_request_id in self.config.get_cip_analysis_requests(parameters[4].valueAsText):
                    analysis_request_ids += " " + analysis_request_id
                analysis_request_ids.strip()
                parameters[0].value = analysis_request_ids
            else:
                parameters[0].value = ""
        else:
            parameters[4].enabled = False
            parameters[4].filter.list = [u"None"]
            parameters[4].value = u"None"

        # Enables calibration file field if calibration file
        if parameters[5].valueAsText == "Calibration":
            if parameters[6].enabled == False:
                parameters[6].enabled = True
                parameters[6].value = ""
        else:
            parameters[6].enabled = False
            parameters[6].value = self.dummy_model_calibration_file_path

        # # Checks that alteration added is not a duplicate
        if parameters[8].values is not None:
            number_of_values = len(parameters[8].values)
            if number_of_values > 1 and parameters[8].values[-1] in parameters[8].values[0:number_of_values-1]:
                parameters[8].values = parameters[8].values[0:number_of_values-1]

        if parameters[9].values is not None:
            number_of_values = len(parameters[9].values)
            if number_of_values > 1 and parameters[9].values[-1] in parameters[9].values[0:number_of_values-1]:
                parameters[9].values = parameters[9].values[0:number_of_values-1]

        if parameters[10].values is not None:
            number_of_values = len(parameters[10].values)
            if number_of_values > 1 and parameters[10].values[-1] in parameters[10].values[0:number_of_values-1]:
                parameters[10].values = parameters[10].values[0:number_of_values-1]

        values_altered= False
        alterations_present = False
        # Enables alteration file field if an alteration is added
        if (parameters[8].altered or parameters[9].altered or parameters[10].altered):
            values_altered = True
        if (parameters[8].valueAsText is not None) or (parameters[9].valueAsText is not None) or (parameters[10].valueAsText is not None):
            alterations_present = True
        if values_altered and alterations_present:
            if parameters[11].enabled == False:
                parameters[11].enabled = True
                parameters[11].value = ""
        else:
            parameters[11].enabled = False
            parameters[11].value = self.dummy_model_alteration_file_path


    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        arcpy.AddMessage("Execute")

        try:
            self.model = Model.initialize_with_current_id(self.config, self.model_dataio)
            #model_id = self.modelcatalogdataio.retrieve_current_model_id()
            #self.model.id = model_id
            self.model.parent_model_id = 0
            if parameters[4] == u"None":
                pass
            else:
                analysis_request_ids = ""
                for analysis_request_id in self.config.get_cip_analysis_requests(parameters[4].valueAsText):
                    analysis_request_ids += " " + analysis_request_id
                analysis_request_ids.strip()
                arcpy.AddMessage(analysis_request_ids)
                self.model.model_request_id = analysis_request_ids
            self.model.project_phase_id = self.config.proj_phase_id[parameters[3].valueAsText]
            self.model.engine_type_id = 1  # not currently in use
            self.model.create_date = datetime.datetime.today()
            self.model.deploy_date = None  # TODO NEEDS TO BE EXTRACTED FROM CONFIG FILE
            self.model.run_date = None  # TODO NEEDS TO BE EXTRACTED FROM CONFIG FILE
            self.model.extract_date = None  # TODO NEEDS TO BE EXTRACTED FROM CONFIG FILE
            self.model.created_by = getpass.getuser()
            self.model.model_path = parameters[1].valueAsText
            self.model.create_project_types(parameters[2].values)
            self.model.create_model_alterations_bc(parameters[8].values)
            self.model.create_model_alterations_hydrologic(parameters[9].values)
            self.model.create_model_alterations_hydraulic(parameters[10].values)
            self.model.model_purpose_id = self.config.model_purpose_id[parameters[5].valueAsText]
            self.model.model_calibration_file = parameters[6].valueAsText
            self.model.model_status_id = self.config.model_status_id[parameters[7].valueAsText]
            self.model.model_alteration_file = parameters[11].valueAsText
            self.model.project_num = parameters[0].valueAsText
            self.model_dataio.create_model_geometry(self.model)
            self.model.create_simulations()
            self.model_catalog.add_model(self.model)

            EMGAATS_Model_Registration_function(self.model_catalog, self.config)
        except InvalidModelException:
            self.model.model_valid_diagnostic()
            arcpy.AddError("Model is not valid")

def EMGAATS_Model_Registration_function(model_catalog, config):
    # type: (ModelCatalog, Config) -> None
    modelcatalogdataio = ModelCatalogDbDataIo(config)
    modeldataio = ModelDataIo(config, modelcatalogdataio)
    simulationdataio = SimulationDataIO(config, modelcatalogdataio)
    model = model_catalog.models[0]
    try:
        arcpy.AddMessage("Adding Model...")
        modelcatalogdataio.add_model(model, modeldataio)
        arcpy.AddMessage("Model Added")
    except:
        arcpy.ExecuteError

    if config.model_status[model.model_status_id] == "Working":
        arcpy.AddMessage("Model Status has been set to 'Working'")
        arcpy.AddMessage("No results will be added to the RRAD")
    else:
        arcpy.AddMessage("Writing results to RRAD")
        for simulation in model.simulations:
            arcpy.AddMessage("Adding results for simulation: " + simulation.sim_desc)
            arcpy.AddMessage("  Adding Area results:")
            #simulationdataio.copy_area_results(simulation)
            simulation.create_areas(simulationdataio)
            arcpy.AddMessage("  Adding node results:")
            simulationdataio.copy_node_results(simulation)
            #TODO: Flooding results not loaded during testing
            try:
                arcpy.AddMessage("  Adding node flooding results:")
                simulationdataio.copy_node_flooding_results(simulation)
            except:
                arcpy.AddWarning("This results.gdb does not have a node flooding feature class.")
                arcpy.AddWarning("The results should be processed with a newer version of EMGAATS.")
            arcpy.AddMessage("  Adding link results:")
            simulationdataio.copy_link_results(simulation)
            arcpy.AddMessage("Results written to RRAD")
