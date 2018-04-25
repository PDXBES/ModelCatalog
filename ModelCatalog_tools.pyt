import arcpy

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
            parameterType="Optional",
            direction="Input")
        model_calibration_file.filter.list = ['xls', 'xlsx', 'docx', 'doc', 'txt']

        model_alterations = arcpy.Parameter(
            displayName="Model Alterations",
            name="model_alterations",
            datatype="GPString",
            parameterType="Required",
            direction="Input",
            multiValue=True)

        model_alterations.filter.type = "ValueList"
        model_alterations.filter.list = ["Boundary Conditions", "Regression Equations", "Roughness"]

        model_alteration_file = arcpy.Parameter(
            displayName="Model Alterations File",
            name="model_alteration_file",
            datatype="DEFile",
            parameterType="Optional",
            direction="Input")
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

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        EMGAATS_Model_Registration_function(parameters, True)
        return


# class Tool2(object):
#     def __init__(self):
#         self.label = "2) ToolAAA"
#         self.description = "Checkboxes and Updating Parameter based on another parameter changing"
#
# #        self.canRunInBackground = True
#
#     def getParameterInfo(self):
#         """Define parameter definitions"""
#         param0 = arcpy.Parameter(
#             displayName="Input Text File",
#             name="in_text_file",
#             datatype="DEFile",
#             parameterType="Required",
#             direction="Input")
#         param0.filter.list = ['txt']
#
#         param3 = arcpy.Parameter(
#              displayName="Workspace",
#              name="in_workspace",
#              datatype="DEWorkspace",
#              parameterType="Required",
#              direction="Input")
#         param3.filter.list = ["File System", "Local Database"]
#
#         param5 = arcpy.Parameter(
#             displayName="Output File",
#             name="out_OutputFile",
#             datatype="DEFile",
#             parameterType="Required",
#             direction="Output")
#
#         param6 = arcpy.Parameter(
#             displayName="List of Integers",
#             name="in_List",
#             datatype="GPLong",
#             parameterType="Required",
#             direction="Input")
#         param6.value = 15
#         param6.filter.type = "ValueList"
#         param6.filter.list = [5, 10, 15, 30, 60]
#
#         param7 = arcpy.Parameter(
#             displayName="Checkbox1",
#             name="in_box1",
#             datatype="GPBoolean",
#             parameterType="Required",
#             direction="Input")
#         param7.value = True
#
#         param8 = arcpy.Parameter(
#             displayName="Checkbox2",
#             name="in_box2",
#             datatype="GPBoolean",
#             parameterType="Required",
#             direction="Input")
#         param8.value = False
#
#         param10 = arcpy.Parameter(
#              displayName="Cell Assignment",
#              name="cell_assignment",
#              datatype="GPString",
#              parameterType="Required",
#              direction="Input")
#
#         param10.value = "Maximum Area"
#         param10.filter.type = "ValueList"
#         param10.filter.list = ["Cell Center", "Maximum Area", "Maximum Combined Area"]
#
#         params = [param0, param3, param5, param6, param7, param8, param10]
#         return params
#
#     def isLicensed(self):
#         try:
#             if arcpy.CheckExtension("Spatial") != "Available":
#                 raise Exception
#         except Exception:
#             return False  # tool cannot be executed
#
#         return True  # tool can be executed
#
#     def updateParameters(self, parameters):
#         """Modify the values and properties of parameters before internal
#         validation is performed.  This method is called whenever a parameter
#         has been changed."""
#         if parameters[1].altered:
#             parameters[2].value = parameters[1].valueAsText + "\\testOut.txt"
#
#     def updateMessages(self, parameters):
#         """Modify the messages created by internal validation for each tool
#         parameter.  This method is called after internal validation."""
#         return
#
#     def execute(self, parameters, messages):
#         tool2_function(parameters)
#         return
#
#
# class Tool3(object):
#     def __init__(self):
#         self.label = "3) Tool"
#         self.description = "GPValueTable"
#
# #        self.canRunInBackground = True
#
#     def getParameterInfo(self):
#         """Define parameter definitions"""
#
#         param10 = arcpy.Parameter(
#             displayName='GPValue Table',
#             name='gp_ValueTable_optional',
#             datatype='GPValueTable',
#             parameterType='Optional',
#             direction='Input')
#
#         param10.columns = [['DEFile', 'TField'], ['String', 'NAME'], ['String', 'UNITS']]
#         param10.filters[1].type = 'ValueList'
#         param10.filters[0].list = ["txt"]
#         param10.filters[1].list = ["Thing1", "Thing2"]
#         param10.filters[2].list = ["Units1", "Units2"]
#
#         params = [param10]
#         return params
#
#     def isLicensed(self):
#         # try:
#         #     if arcpy.CheckExtension("Spatial") != "Available":
#         #         raise Exception
#         # except Exception:
#         #     return False  # tool cannot be executed
#
#         return True  # tool can be executed
#
#     def updateParameters(self, parameters):
#         """Modify the values and properties of parameters before internal
#         validation is performed.  This method is called whenever a parameter
#         has been changed."""
#
#     def updateMessages(self, parameters):
#         """Modify the messages created by internal validation for each tool
#         parameter.  This method is called after internal validation."""
#         return
#
#     def execute(self, parameters, messages):
#         tool3_function(parameters)
#         return


def EMGAATS_Model_Registration_function(parameters, gui):
    if gui:
        # read input data from toolboox gui
        input_filename = parameters[0].valueAsText
        output_filename = parameters[1].valueAsText
    else:
        input_filename = parameters[0]
        output_filename = parameters[1]
    arcpy.AddMessage(input_filename)
    arcpy.AddMessage(output_filename)


# def tool2_function(parameters):
#     # read input data from toolboox gui
#     input_filename = parameters[0].valueAsText
#     workspace = parameters[1].valueAsText
#     output_filename = parameters[2].valueAsText
#     number_from_list = parameters[3].valueAsText
#     checkbox1 = parameters[4].valueAsText
#     checkbox2 = parameters[5].valueAsText
#     string_from_list = parameters[6].valueAsText
#     arcpy.AddMessage(input_filename)
#     arcpy.AddMessage(workspace)
#     arcpy.AddMessage(output_filename)
#     arcpy.AddMessage(number_from_list)
#     arcpy.AddMessage(checkbox1)
#     arcpy.AddMessage(checkbox2)
#     arcpy.AddMessage(string_from_list)


# def tool3_function(parameters):
#     arcpy.AddMessage(parameters[0].valueAsText)


def main():
    import os
    gui = False
    path = os.path.dirname(os.path.realpath(__file__))
    parameters = []
    input_filename = path + "\\" + "text.txt"
    output_filename = path + "\\" + "out.xls"
    parameters.append(input_filename)
    parameters.append(output_filename)
    EMGAATS_Model_Registration_function(parameters, gui)


if __name__ == '__main__':
    main()
