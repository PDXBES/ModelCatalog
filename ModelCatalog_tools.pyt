import arcpy
from businessclasses.model_catalog import ModelCatalog
from businessclasses.model import Model
from dataio.model_catalog_db_data_io import ModelCatalogDbDataIo
from dataio.simulation_data_io import SimulationDataIo
from dataio.model_data_io import ModelDataIo
from dataio.db_data_io import DbDataIo
import getpass
import datetime
import traceback
import sys
from dataio import utility
from businessclasses import config
from businessclasses.model_catalog_exception import InvalidModelException
from businessclasses.model_catalog_exception import InvalidModelRegistrationFileException
from businessclasses.model_catalog_exception import InvalidParentModelPurposeException
from ui.model_copy import ModelCopy
reload(arcpy)
reload(config)
reload(utility)
# reload(ModelCatalog)
# reload(Model)
# reload(ModelCatalogDbDataIo)
# reload(ModelDataIo)
# reload(SimulationDataIO)

test_flag = "TEST"

# config = config.Config(test_flag)
# model_catalog = ModelCatalog(config)
# model_catalog_db_data_io = ModelCatalogDbDataIo(config)
# model_copy = ModelCopy(config,
#                        model_catalog,
#                        model_catalog_db_data_io)
# model_copy.create_registered_model_dictionary()

class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Model Catalog tools"
        self.alias = "Model Catalog Tools"

        # List of tool classes associated with this toolbox
        self.tools = [EMGAATS_Model_Registration, Copy_Registered_Model, Export_Model_Catalog_Data]

class EMGAATS_Model_Registration(object):
    def __init__(self):
        self.label = "EMGAATS Model Registration"
        self.description = "Tool for registering EMGAATS derived models"
        self.config = config.Config(test_flag)
        self.model_catalog = ModelCatalog(self.config)
        self.modelcatalogdataio = ModelCatalogDbDataIo(self.config)
        self.model_dataio = ModelDataIo(self.config, self.modelcatalogdataio)
        self.utility = utility.Utility(self.config)

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

        model_name = arcpy.Parameter(
            displayName="Model Name",
            name="model_name",
            datatype="GPString",
            parameterType="Required",
            direction="Input")

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

        params = [model_name, model_dir, project_type, project_phase, project_cip_number, project_no,
                  model_purpose, parent_model_dir, model_calibration_file, model_status,
                  model_alterations_boundary_conditions,
                  model_alterations_hydrologic, model_alterations_hydraulic, model_alteration_file]

        if test_flag == "TEST":
            read_write = arcpy.Parameter(
                displayName="Make model read/write before registration",
                name="read_write",
                datatype="GPBoolean",
                parameterType="Required",
                direction="Input",
            )
            read_write.value = False
            params.append(read_write)

        return params

    def isLicensed(self):
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed.
        Where we put the logic in to enable/disable fields
        """
        arcpy.AddMessage("Update Parameters")

        model_name_parameter = parameters[0]
        model_path_parameter = parameters[1]
        project_type_parameter = parameters[2]
        project_phase_parameter = parameters[3]
        cip_number_parameter = parameters[4]
        analysis_request_id_parameter = parameters[5]
        model_purpose_parameter = parameters[6]
        parent_model_dir_parameter = parameters[7]
        model_calibration_file_parameter = parameters[8]
        model_status_parameter = parameters[9]
        model_alt_bc_parameter = parameters[10]
        model_alt_hydrologic_parameter = parameters[11]
        model_alt_hydraulic_parameter = parameters[12]
        model_alteration_file_parameter = parameters[13]


        if project_phase_parameter.valueAsText in ("Pre Design", "Design 30", "Design 60", "Design 90"):
            if cip_number_parameter.value == u"None":
                cip_number_parameter.value = None
            cip_number_parameter.enabled = True
            cip_number_parameter.filter.list = self.config.unique_cip_numbers
            if cip_number_parameter.value != None or cip_number_parameter.value == u"None":
                analysis_request_id_parameter.value = "ARID"
                analysis_request_ids = ""
                for analysis_request_id in self.config.get_cip_analysis_requests(cip_number_parameter.value):
                    analysis_request_ids += " " + analysis_request_id
                analysis_request_ids.strip()
                analysis_request_id_parameter.value = analysis_request_ids
            else:
                analysis_request_id_parameter.value = " "
        else:
            cip_number_parameter.enabled = False
            cip_number_parameter.filter.list = [u"None"]
            cip_number_parameter.value = u"None"

        # Enables calibration file field if calibration file
        if model_purpose_parameter.valueAsText == "Calibration":
            if model_calibration_file_parameter.enabled == False:
                model_calibration_file_parameter.enabled = True
                model_calibration_file_parameter.value = ""
            if parent_model_dir_parameter.enabled == True:
                parent_model_dir_parameter.enabled = False
                parent_model_dir_parameter.value = self.dummy_parent_model_path
        else:
            model_calibration_file_parameter.enabled = False
            model_calibration_file_parameter.value = self.dummy_model_calibration_file_path
            if model_purpose_parameter.altered and not parent_model_dir_parameter.enabled:
                parent_model_dir_parameter.enabled = True
                parent_model_dir_parameter.value = ""

        drop_down_list_remove_value_not_in_domain(model_status_parameter)
        drop_down_list_remove_value_not_in_domain(model_purpose_parameter)
        drop_down_list_remove_value_not_in_domain(project_phase_parameter)
        drop_down_list_remove_value_not_in_domain(cip_number_parameter)

        combo_box_remove_duplicates(model_alt_bc_parameter)
        combo_box_remove_value_not_in_domain(model_alt_bc_parameter)
        combo_box_remove_duplicates(model_alt_hydrologic_parameter)
        combo_box_remove_value_not_in_domain(model_alt_hydrologic_parameter)
        combo_box_remove_duplicates(model_alt_hydraulic_parameter)
        combo_box_remove_value_not_in_domain(model_alt_hydraulic_parameter)

        values_altered = False
        alterations_present = False
        # Enables alteration file field if an alteration is added
        if (model_alt_bc_parameter.altered or model_alt_hydrologic_parameter.altered or model_alt_hydraulic_parameter.altered):
            values_altered = True
        if (model_alt_bc_parameter.valueAsText is not None) or (model_alt_hydrologic_parameter.valueAsText is not None) or (model_alt_hydraulic_parameter.valueAsText is not None):
            alterations_present = True
        if values_altered and alterations_present:
            if model_alteration_file_parameter.enabled == False:
                model_alteration_file_parameter.enabled = True
                model_alteration_file_parameter.value = ""
        else:
            model_alteration_file_parameter.enabled = False
            model_alteration_file_parameter.value = self.dummy_model_alteration_file_path

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

#should validate the parent model id before we run execute
    def execute(self, parameters, messages):
        arcpy.AddMessage("Execute")

        try:
            self.model = Model.initialize_with_current_id(self.config, self.modelcatalogdataio)
            self.model.parent_model_id = 0

            model_name_parameter = parameters[0]
            model_path_parameter = parameters[1]
            project_type_parameter = parameters[2]
            project_phase_parameter = parameters[3]
            cip_number_parameter = parameters[4]
            analysis_request_id_parameter = parameters[5]
            model_purpose_parameter = parameters[6]
            parent_model_dir_parameter = parameters[7]
            model_calibration_file_parameter = parameters[8]
            model_status_parameter = parameters[9]
            model_alt_bc_parameter = parameters[10]
            model_alt_hydrologic_parameter = parameters[11]
            model_alt_hydraulic_parameter = parameters[12]
            model_alteration_file_parameter = parameters[13]

            if cip_number_parameter == u"None":
                pass
            else:
                analysis_request_ids = ""
                for analysis_request_id in self.config.get_cip_analysis_requests(cip_number_parameter.valueAsText):
                    analysis_request_ids += " " + analysis_request_id
                analysis_request_ids.strip()
                arcpy.AddMessage(analysis_request_ids)
                self.model.model_request_id = analysis_request_ids
            self.model.project_phase_id = self.config.proj_phase_id[project_phase_parameter.valueAsText]
            self.model.engine_type_id = 1  # not currently in use
            self.model.create_date = datetime.datetime.today()
            self.model.created_by = getpass.getuser()
            self.model.model_name = model_name_parameter.valueAsText
            self.model.model_path = self.utility.check_path(model_path_parameter.valueAsText)
            self.model.deploy_date = None  # TODO NEEDS TO BE EXTRACTED FROM CONFIG FILE
            self.model.run_date = None  # TODO NEEDS TO BE EXTRACTED FROM CONFIG FILE (change to results extracted date)
            self.model.set_extract_date(self.model_dataio)
            self.model.create_project_types(project_type_parameter.values, self.modelcatalogdataio)
            self.model.create_model_alterations_bc(model_alt_bc_parameter.values, self.modelcatalogdataio)
            self.model.create_model_alterations_hydrologic(model_alt_hydrologic_parameter.values, self.modelcatalogdataio)
            self.model.create_model_alterations_hydraulic(model_alt_hydraulic_parameter.values, self.modelcatalogdataio)
            self.model.model_purpose_id = self.config.model_purpose_id[model_purpose_parameter.valueAsText]

            if self.model.model_purpose_id == self.config.model_purpose_id["Calibration"]:
                self.model.model_calibration_file = self.utility.check_path(model_calibration_file_parameter.valueAsText)
            else:
                self.model.parent_model_path = self.utility.check_path(parent_model_dir_parameter.valueAsText)
                self.model.model_calibration_file = None
            self.model.model_status_id = self.config.model_status_id[model_status_parameter.valueAsText]
            if len(self.model.model_alterations) > 0:
                self.model.model_alteration_file = self.utility.check_path(model_alteration_file_parameter.valueAsText)
            else:
                self.model.model_alteration_file = None
            self.model.project_num = analysis_request_id_parameter.valueAsText
            self.model.create_simulations(self.model_dataio)
            self.model_dataio.create_model_geometry(self.model)

            try:
                self.model.set_parent_model_id(self.model_dataio)
            except(InvalidModelRegistrationFileException):
                arcpy.AddError("Invalid Parent Model Registration File")
                raise arcpy.ExecuteError()
            except InvalidParentModelPurposeException as e:
                arcpy.AddError("Invalid Parent Model Purpose")
                arcpy.AddError(e.parent_model_purpose)
                raise arcpy.ExecuteError()

            self.model_catalog.add_model(self.model)

            if test_flag == "TEST":
                if parameters[-1].value:
                    self.model_dataio.set_model_to_read_write(self.model)

            EMGAATS_Model_Registration_function(self.model_catalog, self.config)
        except InvalidModelException:
            self.model._write_attributes_to_screen()
            self.model.model_valid_diagnostic()
            arcpy.AddError("Model is not valid")

def EMGAATS_Model_Registration_function(model_catalog, config):
    # type: (ModelCatalog, Config) -> None
    model_catalog_data_io = ModelCatalogDbDataIo(config)
    model_data_io = ModelDataIo(config, model_catalog_data_io)
    simulation_data_io = SimulationDataIo(config, model_catalog_data_io)
    model = model_catalog.models[0]
    try:
        arcpy.AddMessage("Adding Model...")
        model_catalog_data_io.add_model(model, model_data_io, simulation_data_io)
        arcpy.AddMessage("Model Added")
    except:
        arcpy.AddError("Model could not be registered")
        arcpy.ExecuteError()

########################################################################################################################

class Copy_Registered_Model(object):
    def __init__(self):
        self.label = "Copy a Registered Model"
        self.description = "Tool for making a copy of a model which was previously registered in the Model Catalog. " \
                           "The resultant copy will be unlocked and editable. " \
                           "The copy will be date stamped and created in the same directory as the original."

        self.config = config.Config(test_flag)
        self.model_catalog = ModelCatalog(self.config)
        self.db_data_io = DbDataIo(self.config)
        self.modelcatalogdataio = ModelCatalogDbDataIo(self.config)
        self.model_data_io = ModelDataIo(self.config, self.db_data_io)
        self.model_copy = ModelCopy(self.config,
                                    self.model_catalog,
                                    self.modelcatalogdataio)
        self.model_copy.create_registered_model_dictionary()

    def getParameterInfo(self):
        registered_models = arcpy.Parameter(
            displayName="Registered Models",
            name="registered_models",
            datatype="GPString",
            parameterType="Required",
            direction="Input",
            multiValue=False)
        registered_models.filter.type = "ValueList"
        registered_models.filter.list = self.model_copy.registered_model_dict.keys()

        params = [registered_models]
        return params

    def isLicensed(self):
        return True

    def updateParameters(self, parameters):
        pass

    def updateMessages(self, parameters):

        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""

        return

    def execute(self, parameters, messages):
        arcpy.AddMessage("Execute")

        # get list of models selected by user
        selected_model_description = parameters[0].value
        selected_model = self.model_copy.registered_model_dict[selected_model_description]

        # get model.model_dir and make a copy (parse model_dir to get 1 folder level up)
        try:
            arcpy.AddMessage("Copying " + str(selected_model.model_path) + " ...")
            self.model_copy.copy_model_folder(selected_model)
            arcpy.AddMessage(" - Setting copy to read/ write")
            self.model_data_io.set_model_copy_to_read_write(self.model_copy.new_copy_dir_name(selected_model))
            arcpy.AddMessage(" - Deleting model registration file")
            self.model_data_io.delete_model_registration_file(self.model_copy.new_copy_dir_name(selected_model))
            arcpy.AddMessage("Model Copied and Ready")
        except:
            arcpy.AddError(str(selected_model.model_path) + " - Model could not be copied")
            arcpy.ExecuteError()


########################################################################################################################

class Export_Model_Catalog_Data(object):
    def __init__(self):
        self.label = "Export Selected Models to Geodatabase"
        self.description = "Tool for exporting model data which was previously registered in the Model Catalog."

        self.config = config.Config(test_flag)
        self.model_catalog = ModelCatalog(self.config)
        self.db_data_io = DbDataIo(self.config)
        self.modelcatalogdataio = ModelCatalogDbDataIo(self.config)
        self.model_data_io = ModelDataIo(self.config, self.db_data_io)
        self.model_copy = ModelCopy(self.config,
                                    self.model_catalog,
                                    self.modelcatalogdataio)
        self.utility = utility.Utility(self.config)

        self.model_copy.create_non_calibration_model_dictionary()

    def getParameterInfo(self):
        registered_models = arcpy.Parameter(
            displayName="Registered Models",
            name="registered_models",
            datatype="GPString",
            parameterType="Required",
            direction="Input",
            multiValue=True)
        registered_models.filter.type = "ValueList"
        registered_models.filter.list = self.model_copy.non_calibration_model_dict.keys()

        output_dir = arcpy.Parameter(
            displayName="Output Directory",
            name="output_directory",
            datatype="DEWorkspace",
            parameterType="Required",
            direction="Input")

        output_dir.filter.list = ["File System", "Local Database"]

        params = [registered_models, output_dir]
        return params

    def isLicensed(self):
        return True

    def updateParameters(self, parameters):
        pass

    def updateMessages(self, parameters):

        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""

        return

    def execute(self, parameters, messages):
        arcpy.AddMessage("Execute")

        # get list of models selected by user
        selected_model_descriptions = parameters[0].values
        selected_models = self.model_copy.get_selected_non_calibration_models(selected_model_descriptions)

        model_id_list = []
        for model in selected_models:
            model_id_list.append(model.id)

        simulation_id_list = self.model_copy.get_sim_ids_from_model_ids(model_id_list)

        output_directory = parameters[1].value
        gdb_full_path_name = self.utility.gdb_full_path_name(output_directory)

        try:
            arcpy.AddMessage("Model Export - Process Started")
            self.modelcatalogdataio.create_output_gdb(gdb_full_path_name)

            self.modelcatalogdataio.copy_data_to_gdb(self.config.model_tracking_sde_path, "Model_ID", model_id_list, gdb_full_path_name)
            self.modelcatalogdataio.copy_data_to_gdb(self.config.geometry_areas_sde_path, "Model_ID", model_id_list, gdb_full_path_name)
            self.modelcatalogdataio.copy_data_to_gdb(self.config.geometry_links_sde_path, "Model_ID", model_id_list, gdb_full_path_name)
            self.modelcatalogdataio.copy_data_to_gdb(self.config.geometry_nodes_sde_path, "Model_ID", model_id_list, gdb_full_path_name)
            self.modelcatalogdataio.copy_data_to_gdb(self.config.storage_sde_path, "Model_ID", model_id_list, gdb_full_path_name)
            self.modelcatalogdataio.copy_data_to_gdb(self.config.project_type_sde_path, "Model_ID", model_id_list, gdb_full_path_name)
            self.modelcatalogdataio.copy_data_to_gdb(self.config.director_sde_path, "Model_ID", model_id_list, gdb_full_path_name)
            self.modelcatalogdataio.copy_data_to_gdb(self.config.simulation_sde_path, "Model_ID", model_id_list, gdb_full_path_name)
            self.modelcatalogdataio.copy_data_to_gdb(self.config.model_alt_hydrologic_sde_path, "Model_ID", simulation_id_list, gdb_full_path_name)
            self.modelcatalogdataio.copy_data_to_gdb(self.config.model_alt_hydraulic_sde_path, "Model_ID", simulation_id_list, gdb_full_path_name)
            self.modelcatalogdataio.copy_data_to_gdb(self.config.model_alt_bc_sde_path, "Model_ID", simulation_id_list, gdb_full_path_name)

            self.modelcatalogdataio.copy_data_to_gdb(self.config.results_area_sde_path, "Simulation_ID", simulation_id_list, gdb_full_path_name)
            self.modelcatalogdataio.copy_data_to_gdb(self.config.results_link_sde_path, "Simulation_ID", simulation_id_list, gdb_full_path_name)
            self.modelcatalogdataio.copy_data_to_gdb(self.config.results_node_sde_path, "Simulation_ID", simulation_id_list, gdb_full_path_name)
            self.modelcatalogdataio.copy_data_to_gdb(self.config.results_node_flooding_sde_path, "Simulation_ID", simulation_id_list, gdb_full_path_name)

            arcpy.AddMessage("Zipping File")
            self.utility.zip(gdb_full_path_name)

            arcpy.AddMessage("Model Export - Process Finished")
        except:

            if arcpy.Exists(gdb_full_path_name):
                arcpy.Delete_management(gdb_full_path_name)
            if arcpy.Exists(gdb_full_path_name + ".zip"):
                arcpy.Delete_management(gdb_full_path_name + ".zip")
            arcpy.AddError("Data could not be exported")
            arcpy.ExecuteError()


########################################################################################################################

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

def combo_box_remove_duplicates(parameter):
    if parameter.values is not None:
        number_of_values = len(parameter.values)
        if number_of_values > 1 and parameter.values[-1] in parameter.values[0:number_of_values - 1]:
            parameter.values = parameter.values[0:number_of_values - 1]

def combo_box_remove_value_not_in_domain(parameter):
    if parameter.values is not None:
        number_of_values = len(parameter.values)
        if number_of_values >= 1 and not parameter.values[-1][0] in parameter.filters[0].list:
            parameter.values = parameter.values[0:number_of_values - 1]

def drop_down_list_remove_value_not_in_domain(parameter):
    if parameter.value is not None:
        if not parameter.value in parameter.filter.list:
            parameter.value = None

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

