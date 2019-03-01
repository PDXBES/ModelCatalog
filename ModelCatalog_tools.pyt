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
        self.tools = [EMGAATS_Model_Registration, TemporaryMonitorQaQc, SlrtQaQc]

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
        self.dummy_parent_model_path = self.config.dummy_parent_model_path
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

        parent_model_dir = arcpy.Parameter(
            displayName="Parent Model Directory",
            name="parent_model_directory",
            datatype="DEWorkspace",
            parameterType="Required",
            direction="Input")

        parent_model_dir.filter.list = ["File System", "Local Database"]
        parent_model_dir.enabled = False
        parent_model_dir.value = self.dummy_parent_model_path


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


        params = [project_no, model_dir, parent_model_dir, project_type, project_phase, project_cip_number,
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

        if parameters[4].valueAsText in ("Pre Design", "Design 30", "Design 60", "Design 90"):
            if parameters[5].value == u"None":
                parameters[5].value = None
            parameters[5].enabled = True
            parameters[5].filter.list = self.config.unique_cip_numbers
            if parameters[5].value != None or parameters[5].value == u"None":
                parameters[0].value = "ARID"
                analysis_request_ids = ""
                for analysis_request_id in self.config.get_cip_analysis_requests(parameters[5].valueAsText):
                    analysis_request_ids += " " + analysis_request_id
                analysis_request_ids.strip()
                parameters[0].value = analysis_request_ids
            else:
                parameters[0].value = ""
        else:
            parameters[5].enabled = False
            parameters[5].filter.list = [u"None"]
            parameters[5].value = u"None"

        # Enables calibration file field if calibration file
        if parameters[6].valueAsText == "Calibration":
            if parameters[7].enabled == False:
                parameters[7].enabled = True
                parameters[7].value = ""
            if parameters[2].enabled == True:
                parameters[2].enabled = False
                parameters[2].value = self.dummy_parent_model_path
        else:
            parameters[7].enabled = False
            parameters[7].value = self.dummy_model_calibration_file_path
            if parameters[6].altered:
                parameters[2].enabled = True
                parameters[2].value = ""


        # # Checks that alteration added is not a duplicate
        if parameters[9].values is not None:
            number_of_values = len(parameters[9].values)
            if number_of_values > 1 and parameters[9].values[-1] in parameters[9].values[0:number_of_values-1]:
                parameters[9].values = parameters[9].values[0:number_of_values-1]

        if parameters[10].values is not None:
            number_of_values = len(parameters[10].values)
            if number_of_values > 1 and parameters[10].values[-1] in parameters[10].values[0:number_of_values-1]:
                parameters[10].values = parameters[10].values[0:number_of_values-1]

        if parameters[11].values is not None:
            number_of_values = len(parameters[11].values)
            if number_of_values > 1 and parameters[11].values[-1] in parameters[11].values[0:number_of_values-1]:
                parameters[11].values = parameters[11].values[0:number_of_values-1]

        values_altered= False
        alterations_present = False
        # Enables alteration file field if an alteration is added
        if (parameters[9].altered or parameters[10].altered or parameters[11].altered):
            values_altered = True
        if (parameters[9].valueAsText is not None) or (parameters[10].valueAsText is not None) or (parameters[11].valueAsText is not None):
            alterations_present = True
        if values_altered and alterations_present:
            if parameters[12].enabled == False:
                parameters[12].enabled = True
                parameters[12].value = ""
        else:
            parameters[12].enabled = False
            parameters[12].value = self.dummy_model_alteration_file_path

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        arcpy.AddMessage("Execute")

        try:
            self.model = Model.initialize_with_current_id(self.config, self.model_dataio)
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
            self.model.run_date = None  # TODO NEEDS TO BE EXTRACTED FROM CONFIG FILE (change to results extracted date)
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

class TemporaryMonitorQaQc(object):
    def __init__(self):
        self.label = "Temporary Monitor Data Quality"
        self.description = "Tool for recording temporary data quality to database"
        self.config = config.Config()
        self.model_catalog = ModelCatalog(self.config)
        self.modelcatalogdataio = ModelCatalogDbDataIo(self.config)
        self.model_dataio = ModelDataIo(self.config, self.modelcatalogdataio)
        self.model_id = ""
        # Need to create list of model objects from model catalog

    def getParameterInfo(self):
        model_id = arcpy.Parameter(
            displayName="Model ID",
            name="model_id",
            datatype="GPString",
            parameterType="Required",
            direction="Input")

        model_id.filter.type = "ValueList"
        model_id.filter.list = [1, 2, 3] #TODO Need to get list of final calibration models, purpose, paths

        monitor_location_id = arcpy.Parameter(
            displayName="Location_ID",
            name="monitor_location_id",
            datatype="GPString",
            parameterType="Required",
            direction="Input")
        monitor_location_id.filter.list = [1, 2, 3] #TODO Need to get list of temporary monitors

        simulations_qa_qc = arcpy.Parameter(
            displayName='Observed Data Quality',
            name='qaqc_table',
            datatype='GPValueTable',
            parameterType='Required',
            direction='Input')

        simulations_qa_qc.columns = [['String', 'Simulation'], ['String', 'Depth QC'], ['String', 'Flow QC']]
        simulations_qa_qc.filters[1].type = 'ValueList'
        simulations_qa_qc.filters[1].list = ["Good", "Fair", "Poor", "NA"]
        simulations_qa_qc.filters[2].list = ["Good", "Fair", "Poor", "NA"]

        calculated_data_quality = arcpy.Parameter(
            displayName="Calculated Data Quality (Automatically Calculated)",
            name="calculated_data_quality",
            datatype="GPString",
            parameterType="Required",
            direction="Input")
        calculated_data_quality.filter.list = ["Good", "Fair", "Poor"]
        calculated_data_quality.value = "Good" #TODO this will need to calculated in the updateParameters
        calculated_data_quality.enabled = False

        override_data_quality = arcpy.Parameter(
            displayName="Manual Data Quality",
            name="override_data_quality",
            datatype="GPString",
            parameterType="Required",
            direction="Input")
        override_data_quality.filter.list = ["Good", "Fair", "Poor"]

        params = [model_id, monitor_location_id, simulations_qa_qc, calculated_data_quality, override_data_quality]
        return params

    def isLicensed(self):
        return True

    def updateParameters(self, parameters):
        model_id_parameter = parameters[0]
        data_review_parameter = parameters[2]
        if model_id_parameter.altered:
            simulation_values, simulations = data_review_combo_box_get_simulations(model_id_parameter)
            data_review_combo_box_set_simulation_list(data_review_parameter, model_id_parameter)
            data_review_combo_box_logic(data_review_parameter, model_id_parameter, simulation_values, simulations)
        else:
            data_review_parameter.values = None

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        pass

class SlrtQaQc(object):
    def __init__(self):
        self.label = "SLRT Data Quality"
        self.description = "Tool for recording SLRT data quality to database"
        self.config = config.Config()
        self.model_catalog = ModelCatalog(self.config)
        self.modelcatalogdataio = ModelCatalogDbDataIo(self.config)
        self.model_dataio = ModelDataIo(self.config, self.modelcatalogdataio)
        # Need to create list of model objects from model catalog

    def getParameterInfo(self):
        model_id = arcpy.Parameter(
            displayName="Model ID",
            name="model_id",
            datatype="GPString",
            parameterType="Required",
            direction="Input")

        model_id.filter.type = "ValueList"
        model_id.filter.list = [1, 2, 3] #TODO Need to get list of final calibration models, purpose, paths

        station_id = arcpy.Parameter(
            displayName="Station ID",
            name="station_id",
            datatype="GPString",
            parameterType="Required",
            direction="Input")
        station_id.filter.list = [1, 2, 3] #TODO Need to get list of station ids

        h2_id = arcpy.Parameter(
            displayName="H2 ID",
            name="h2_id",
            datatype="GPString",
            parameterType="Required",
            direction="Input")
        h2_id.filter.list = [1, 2, 3] #TODO Need to get list of h2 id for station

        location_qualifier = arcpy.Parameter(
            displayName="Location Qualifier",
            name="location_qualifier",
            datatype="GPString",
            parameterType="Required",
            direction="Input")
        location_qualifier.filter.list = [1, 2, 3] #TODO Need to get list of location qualifiers for h2 id

        simulations_qa_qc = arcpy.Parameter(
            displayName='Observed Data Quality',
            name='qaqc_table',
            datatype='GPValueTable',
            parameterType='Required',
            direction='Input')

        simulations_qa_qc.columns = [['String', 'Simulation'], ['String', 'Depth QC'], ['String', 'Flow QC']]
        simulations_qa_qc.filters[1].type = 'ValueList'
        simulations_qa_qc.filters[1].list = ["Good", "Fair", "Poor", "NA"]
        simulations_qa_qc.filters[2].list = ["Good", "Fair", "Poor", "NA"]

        calculated_data_quality = arcpy.Parameter(
            displayName="Calculated Data Quality (Automatically Calculated)",
            name="calculated_data_quality",
            datatype="GPString",
            parameterType="Required",
            direction="Input")
        calculated_data_quality.filter.list = ["Good", "Fair", "Poor"]
        calculated_data_quality.value = "Good" #TODO this will need to calculated in the updateParameters
        calculated_data_quality.enabled = False

        override_data_quality = arcpy.Parameter(
            displayName="Data Quality Override",
            name="override_data_quality",
            datatype="GPString",
            parameterType="Required",
            direction="Input")
        override_data_quality.filter.list = ["Good", "Fair", "Poor"]

        params = [model_id, station_id, h2_id, location_qualifier, simulations_qa_qc, calculated_data_quality,
                  override_data_quality]
        return params

    def isLicensed(self):
        return True

    def updateParameters(self, parameters):
        model_id_parameter = parameters[0]
        data_review_parameter = parameters[4]
        if model_id_parameter.altered:
            simulation_values, simulations = data_review_combo_box_get_simulations(model_id_parameter)
            data_review_combo_box_set_simulation_list(data_review_parameter, model_id_parameter)
            data_review_combo_box_logic(data_review_parameter, model_id_parameter, simulation_values, simulations)
        else:
            data_review_parameter.values = None

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""

        return

    def execute(self, parameters, messages):
        pass

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
    if model.write_to_rrad():
        arcpy.AddMessage("Writing results to RRAD")
        for simulation in model.simulations:
            arcpy.AddMessage("Adding results for simulation: " + simulation.sim_desc)
            simulationdataio.add_simulation_results(simulation)
            arcpy.AddMessage("Results written to RRAD")

    else:
        arcpy.AddMessage("No results will be added to the RRAD")

def data_review_combo_box_logic(data_review_parameter, model_id_parameter, simulation_values, simulations):
    # Prevents user from adding or deleting simulations
    if len(simulations) > 0 and model_id_parameter.hasBeenValidated:
        if data_review_parameter.values is not None:
            replace_simulations_deleted = len(data_review_parameter.values) < len(simulations)
            remove_simulations_added = len(data_review_parameter.values) > len(simulations)
            if replace_simulations_deleted:
                data_review_combo_box_replace_deleted_simulations(data_review_parameter, simulations)
            if remove_simulations_added:
                data_review_combo_box_remove_added_simulations(data_review_parameter, simulations)
        else:
            data_review_parameter.values = simulation_values

def data_review_combo_box_set_simulation_list(data_review_parameter, model_id_parameter):
    # Gets list of simulations if there is a model id
    simulation_values, simulations = data_review_combo_box_get_simulations(model_id_parameter)
    if model_id_parameter.hasBeenValidated == False:
        # Sets list of simulations if the model id has been changed
        data_review_parameter.values = simulation_values

#TODO Needs a list of simulation descriptions based on model_id_parameter
def data_review_combo_box_get_simulations(model_id_parameter):
    simulations = ["10012019", "09012019",
                   "08012019"]  # TODO Need a list of simulation descriptions based on model_id_parameter
    simulation_values = zip(simulations, len(simulations) * [""], len(simulations) * [""])
    return simulation_values, simulations

def data_review_combo_box_remove_added_simulations(data_review_parameter, simulations):
    param = []
    for value in data_review_parameter.values:
        if value[0] in simulations:
            param.append(value)
    data_review_parameter.values = param

def data_review_combo_box_replace_deleted_simulations(data_review_parameter, simulations):
    param = []
    for simulation in simulations:
        deleted_simulation = True
        existing_simulation = None
        for value in data_review_parameter.values:
            if value[0] == simulation:
                deleted_simulation = False
                existing_simulation = value
                break
        if deleted_simulation:
            # simulation deleted by user
            param.append([simulation, "", ""])
        else:
            param.append(existing_simulation)
    data_review_parameter.values = param

