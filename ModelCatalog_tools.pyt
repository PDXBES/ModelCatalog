# Overview info
# UI input objects are added to 'parameters' object (getParameterInfo function)
# values are extracted to individual variables by referencing 'paramaters' indices
# variable values are applied to feature class fields by referencing Update Cursor row indices
#
# Big Question - how to manage domains? - currently UI domains are hard coded in the script...
# but in theory we could grab those values from lookup tables - this could determine whether...
# we use ID fields or fields with the actual values

# ----------------------------------------------------------------------------------------------------------------------

import arcpy, os
from model_catalog import ModelCatalog
from model import Model
from data_io import DataIO
import getpass, datetime


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
        path = os.path.dirname(os.path.realpath(__file__))
        self.dummy_model_calibration_file_path = path + "\\" + "DummyFiles" + "\\" + "model_calibration_file.xlsx"
        self.dummy_model_alteration_file_path = path + "\\" + "DummyFiles" + "\\" + "model_alteration_file.xlsx"
        self.model_catalog = ModelCatalog()
        self.model = Model()
        self.dataio = DataIO()


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
        project_type.filter.list = ["Combined", "Sanitary", "Storm", "Other"]

        project_phase = arcpy.Parameter(
            displayName="Project Phase",
            name="project_phase",
            datatype="GPString",
            parameterType="Required",
            direction="Input")

        project_phase.filter.type = "ValueList"
        project_phase.filter.list = ["Planning", "Pre design", "Design 30", "Design 60", "Design 90"]

        model_purpose = arcpy.Parameter(
            displayName="Model Purpose",
            name="model_purpose",
            datatype="GPString",
            parameterType="Required",
            direction="Input")

        model_purpose.filter.type = "ValueList"
        model_purpose.filter.list = ["Calibration", "Characterization", "Alternative", "Recommended Plan"]

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
        model_alterations.filters[0].list = ["Boundary Conditions", "Regression Equations", "Roughness"]

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

        model_id = self.dataio.retrieve_next_model_id(self.dataio.ValueTable,["Object_Type", "Current_ID"])
        self.model.model_id = model_id
        self.model.parent_model_id = 0
        self.model.model_request_id = 0
        self.model.project_phase_id = parameters[3].valueAsText
        self.model.engine_type_id = 1
        self.model.create_date = datetime.datetime.today()
        self.model.deploy_date = None #TODO NEEDS TO BE EXTRACTED FROM CONFIG FILE
        self.model.run_date = None #TODO NEEDS TO BE EXTRACTED FROM CONFIG FILE
        self.model.extract_date = None #TODO NEEDS TO BE EXTRACTED FROM CONFIG FILE
        self.model.created_by = getpass.getuser() #TODO NEEDS TO CHANGE DATABASE FIELD TO NOT AUTOPOPULATE
        self.model.model_path = parameters[1].valueAsText
        self.model.project_type_id = parameters[2].valueAsText
        self.model.model_purpose_id = parameters[4].valueAsText
        self.model.model_calibration_file = parameters[5].valueAsText
        self.model.model_status_id = parameters[6].valueAsText
        self.model.model_alterations_id = parameters[7].valueAsText
        self.model.model_alteration_file = parameters[8].valueAsText
        self.model.project_num = parameters[0].valueAsText
        self.model.valid

        self.model_catalog.add_model(self.model)
        EMGAATS_Model_Registration_function(self.model_catalog)
        return


def EMGAATS_Model_Registration_function(model_catalog):
    dataio = DataIO()
    # TODO Ask Dan about IDs being attached to domains
    field_names = [
        "Model_ID",
        "Parent_Model_ID",
        "Model_Request_ID",
        "Project_Phase_ID",
        "Engine_Type_ID",
        "Create_Date",
        "Created_by",
        "Deploy_Date",
        "Run_Date",
        "Model_Path",
        "Project_Type_ID",
        "Model_Purpose_ID",
        "Model_Calibration_file",
        "Model_Status_ID",
        "Model_Alterations_ID",
        "Model_Alteration_file",
        "Project_Num"]
    
    dataio.add_model(model_catalog.models[0],dataio.ModelTracking,field_names)

def EMGAATS_Model_Registration_functionOld(parameters):
    # read input data from proxy

    arcpy.env.overwriteOutput = True

    # -- sde connection to modelcatalog --
    # connections = r"\\besfile1\ccsp\03_WP2_Planning_Support_Tools\03_RRAD\Model_Catalog\Dev\connection_files"
    # MODELCATALOG_sde = r"BESDBTEST1.MODELCATALOG.sde"
    # MODEL_CATALOG = os.path.join(connections, MODELCATALOG_sde)
    # ModelTracking = MODEL_CATALOG + r"\MODEL_CATALOG.GIS.ModelTracking"

    tracking = r"\\besfile1\ccsp\03_WP2_Planning_Support_Tools\03_RRAD\Model_Catalog\ModelCatalog_TEST.gdb\ModelTracking"

    project_number = parameters[0].valueAsText
    directory = parameters[1].valueAsText
    param_projType = parameters[2].valueAsText
    param_projPhase = parameters[3].valueAsText
    param_modelPurpose = parameters[4].valueAsText
    param_calibration_file = parameters[5].valueAsText
    param_modelStatus = parameters[6].valueAsText
    #alterations = parameters[7].values
    alterationsAsText = parameters[7].valueAsText
    #alterationValue = parameters[7].value
    param_alterationFile = parameters[8].valueAsText

    # arcpy.AddMessage(input_filename)
    # print input_filename
    # arcpy.AddMessage(project_number)
    # print project_number

    # get feature class from model
    print "Identifying model feature class"
    areas_base = os.path.join(directory, r"EmgaatsModel.gdb\Areas_base")

    # create convex hull of areas_base - buffers took way too long for larger model runs
    print "Creating bounding polygon around model area"
    areas_hull = arcpy.MinimumBoundingGeometry_management(areas_base, r"in_memory\areas_hull", "CONVEX_HULL", "ALL")
    # areas_hull = arcpy.MinimumBoundingGeometry_management(areas_base, r"C:\temp\working.gdb\areas_hull", "CONVEX_HULL", "ALL")

    # get list of field names
    fields = arcpy.ListFields(areas_hull)
    field_names = []
    for field in fields:
        field_names.append(field.name)

    # create field if it does not exist
    my_field = "Model_ID"
    if my_field not in field_names:
        arcpy.AddField_management(areas_hull, my_field, "LONG")

    # get max count of Model_ID from tracking - FOR THIS TO WORK MUST HAVE INITIAL RECORD WITH MODELID == 0
    maxlist = []
    with arcpy.da.SearchCursor(tracking, [my_field]) as cursor:
        for row in cursor:
            maxlist.append(row[0])
                
    newMax = max(maxlist) + 1

    # update Model ID field + 1
    print "Fill Model ID with value + 1"
    with arcpy.da.UpdateCursor(areas_hull, my_field) as cursor:
        for row in cursor:
            row[0] = newMax
            cursor.updateRow(row)

    # append result (which should have a single record) to model tracking feature class, using model tracking results
    print "Appending bounding polygon to Model Tracking"
    arcpy.Append_management(areas_hull, tracking, "NO_TEST")

    # apply values returned from form inputs to tracking fc
    # BEWARE - FIELDS HERE WILL NEED TO CHANGE IF SCHEMA CHANGES BUT ORDER DOES NOT MATTER
    # EG ONCE WE POINT TO REAL DATA ON TEST1 FIELD NAMES CHANGE SLIGHTLY
    edit_fields = ["Model_ID", "Parent_Model_ID", "Model_Request_ID", "Project_Phase", "Engine_Type", "Create_Date",
                   "Deploy_Date", "Run_Date", "Extract_Date", "Created_by", "Model_Path", "Project_Type",
                   "Model_Purpose", "Model_Calibration_file", "Model_Status", "Model_Alterations",
                   "Model_Alteration_file", "Project_Number"]

    print "Applying input values to record"
    #  NOTE - IT DOES NOT MATTER WHAT ORDER THE PARAMETERS INDEXING IS IN SINCE YOU ASSIGN THEM TO A...
    #  NON NUMBERED/ ORDERED VARIABLE ABOVE
    with arcpy.da.UpdateCursor(tracking, edit_fields) as cursor:
        for row in cursor:
            if row[0] == newMax:  # if row has the current model ID
                # row[1] = # ParentModel_ID - not currently filled
                # row[2] = # calculate from model tracking db (does not currently exist)
                row[3] = param_projPhase  # - what do to about ID field?
                # row[4] = # Engine_Type - not currently filled - what to do about ID field?
                # row[5] = # Create_Date - automatic: Editor Tracking enabled for feature class
                # row[6] = # Deploy Date - not currently filled
                # row[7] = # Run Date - not currently filled
                # row[8] = # Extract Date - not currently filled
                # row[9] = # Created by - automatic: Editor Tracking enabled for feature class
                row[10] = directory
                row[11] = param_projType
                row[12] = param_modelPurpose
                row[13] = param_calibration_file
                row[14] = param_modelStatus
                row[15] = alterationsAsText
                row[16] = param_alterationFile
                row[17] = project_number
            cursor.updateRow(row)

def main():  # runs the whole thing; takes manual input if gui = False
    model = Model()
    model_catalog = ModelCatalog()
    dataio = DataIO()
    model_id = dataio.retrieve_next_model_id(dataio.ValueTable, ["Object_Type", "Current_ID"])
    model.model_id = model_id
    model.parent_model_id = 555
    model.model_request_id = 777
    model.project_phase_id = 1
    model.engine_type_id = 1
    model.create_date = None
    model.deploy_date = None  # TODO NEEDS TO BE EXTRACTED FROM CONFIG FILE
    model.run_date = None  # TODO NEEDS TO BE EXTRACTED FROM CONFIG FILE
    model.extract_date = None  # TODO NEEDS TO BE EXTRACTED FROM CONFIG FILE
    model.created_by = getpass.getuser()  # TODO NEEDS TO CHANGE DATABASE FIELD TO NOT AUTOPOPULATE
    model.model_path = "C:\Temp"
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
    EMGAATS_Model_Registration_function(model_catalog)


if __name__ == '__main__':
    main()
