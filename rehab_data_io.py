import arcpy
try:
    from typing import List, Any
except:
    pass
from config import Config
from pipe import Pipe


class RehabDataIO():
    def __init__(self, config):
        # type: (Config) -> None
        self.config = config

        self.active_whole_pipe_layer = "nbcr_data_whole_pipes_layer"
        self.active_whole_pipe_feature_class = "nbcr_data_whole_pipes"
        self.rehab_branches_feature_class = "rehab_branches"

        self.workspace = "in_memory"
        # self.workspace = "c:\\temp\\in_memory.gdb"
        self.output_pipes_table = "output_pipes_table"
        self.output_pipes_table_path = self.workspace + "/" + self.output_pipes_table
        self.active_whole_pipe_feature_class_path = self.workspace + "/" + self.active_whole_pipe_feature_class
        self.rehab_branches_table_path = self.workspace + "/" + self.rehab_branches_feature_class
        self.nbcr_data_whole_pipe_table = "nbcr_data_whole_pipe_table"
        self.nbcr_data_whole_pipe_table_path = self.workspace + "/" + self.nbcr_data_whole_pipe_table

        self.select_active_segments_sql = "hservstat not in ( 'ABAN' , 'TBAB' , 'DNE' )"
        self.select_whole_pipe_sql = "cutno = 0 and compkey is not Null"
        self.select_active_whole_pipe_sql = self.select_active_segments_sql + " and " + self.select_whole_pipe_sql

        self.whole_pipe_fields = ["compkey", "bpw", "usnode",
                                  "dsnode", "diamwidth", "length",
                                  "material", "lateralcost", "manholecost",
                                  "asmrecommendednbcr", "asmrecommendedaction",
                                  "apwspot", "apwliner", "apwwhole", "lateralcount", "globalid"]

        self.output_pipes_table_fields = self.whole_pipe_fields + ["apw", "capitalcost", "rehab_id"]

    def _select_nbcr_data_pipes(self):

        arcpy.MakeFeatureLayer_management(self.config.rehab_nbcr_data_sde_path, self.active_whole_pipe_layer,
                                          self.select_active_whole_pipe_sql, self.workspace)

    def _create_pipe_feature_class(self):
        arcpy.CopyFeatures_management(self.active_whole_pipe_layer, self.active_whole_pipe_feature_class_path)

    def create_branches_table(self):
        arcpy.CopyRows_management(self.config.rehab_branches_sde_path,
                                  self.rehab_branches_table_path)

    def delete_nbcr_data_bpw_field(self, input_table):
        arcpy.DeleteField_management(input_table, "BPW")

    def add_bpw_from_branches(self):
        arcpy.JoinField_management(self.nbcr_data_whole_pipe_table_path,
                                   "compkey",
                                   self.rehab_branches_table_path,
                                   "compkey",
                                   "BPW")

    def convert_nbcr_data_to_table(self):
        self._select_nbcr_data_pipes()
        self._create_pipe_feature_class()
        arcpy.TableToTable_conversion(self.config.rehab_nbcr_data_sde_path,
                                      self.workspace,
                                      self.nbcr_data_whole_pipe_table,
                                      self.select_active_whole_pipe_sql)
        self.delete_nbcr_data_bpw_field(self.nbcr_data_whole_pipe_table_path)
        self.create_branches_table()
        self.add_bpw_from_branches()

    def create_pipes(self, rehab_id):
        pipes = []
        cursor = arcpy.da.SearchCursor(self.nbcr_data_whole_pipe_table_path, self.whole_pipe_fields)
        for row in cursor:
            pipe = Pipe()
            pipe.rehab_id = rehab_id
            pipe.compkey = row[0]
            pipe.bpw = row[1]
            pipe.usnode = row[2]
            pipe.dsnode = row[3]
            pipe.diamwidth = row[4]
            pipe.length = row[5]
            pipe.material = row[6]
            pipe.lateralcost = row[7]
            pipe.manholecost = row[8]
            pipe.asmrecommendednbcr = row[9]
            pipe.asmrecommendedaction = row[10]
            pipe.apwspot = row[11]
            pipe.apwliner = row[12]
            pipe.apwwhole = row[13]
            pipe.lateralcount = row[14]
            pipe.globalid = row[15]
            pipes.append(pipe)
        return pipes

    def write_pipes_to_table(self, rehab):
        arcpy.CreateTable_management(self.workspace, self.output_pipes_table, self.config.rehab_results_sde_path)
        cursor = arcpy.da.InsertCursor(self.output_pipes_table_path, self.output_pipes_table_fields)
        for pipe in rehab.pipes:
            if pipe.valid():
                row = []
                row.append(pipe.compkey)
                row.append(pipe.bpw)
                row.append(pipe.usnode)
                row.append(pipe.dsnode)
                row.append(pipe.diamwidth)
                row.append(pipe.length)
                row.append(pipe.material)
                row.append(pipe.lateralcost)
                row.append(pipe.manholecost)
                row.append(pipe.asmrecommendednbcr)
                row.append(pipe.asmrecommendedaction)
                row.append(pipe.apwspot)
                row.append(pipe.apwliner)
                row.append(pipe.apwwhole)
                row.append(pipe.lateralcount)
                row.append(pipe.globalid)
                row.append(pipe.apw)
                row.append(pipe.capitalcost)
                row.append(pipe.rehab_id)
                cursor.insertRow(row)

    def delete_fields(self, feature_class, fields_to_keep):
        uppercase_fields_to_keep = [field.upper() for field in fields_to_keep]
        fields = arcpy.ListFields(feature_class)
        for field in fields:
            if field.name.upper() in uppercase_fields_to_keep or field.type == 'Geometry' or field.type == 'OID':
                arcpy.AddMessage("Keeping field: " + field.name)
                arcpy.AddMessage("Field Type: " + field.type)
            else:
                arcpy.AddMessage("Deleting field: " + field.name)
                arcpy.AddMessage("Field Type: " + field.type)
                arcpy.DeleteField_management(feature_class, field.name)
                arcpy.AddMessage("Deleting field: " + field.name)

    def delete_fields_1(self, feature_class):
        #TODO Tests for this or work out what field that is being deleted in the delete_fields function that is needed to append to SDE
        fields_to_delete = self.whole_pipe_fields
        uppercase_fields_to_delete = [field.upper() for field in fields_to_delete]
        fields = arcpy.ListFields(feature_class)
        for field in fields:
            if field.name.upper() in uppercase_fields_to_delete and field.name.upper() != 'COMPKEY':
                arcpy.AddMessage("Deleting field: " + field.name)
                arcpy.AddMessage("Field Type: " + field.type)
                arcpy.DeleteField_management(feature_class, field.name)
                arcpy.AddMessage("Deleting field: " + field.name)
            else:
                arcpy.AddMessage("Keeping field: " + field.name)
                arcpy.AddMessage("Field Type: " + field.type)

    def delete_fields_except_compkey_from_feature(self):
        self.delete_fields_1(self.active_whole_pipe_feature_class_path)
        #self.delete_fields(self.active_whole_pipe_feature_class_path, ["compkey", "geom_Length"])

    def join_output_pipe_table_and_geometry(self):
       arcpy.JoinField_management(self.active_whole_pipe_feature_class_path,
                                  "compkey",
                                  self.output_pipes_table_path,
                                  "compkey")

    def append_whole_pipes_to_rehab_results(self):
        try:
            edit = arcpy.da.Editor(self.config.RRAD_sde_path)

            edit.startEditing(False, True)

            edit.startOperation()
            print("starting append")
            arcpy.Append_management(self.active_whole_pipe_feature_class_path, self.config.rehab_results_sde_path, "NO_TEST")
            #raise arcpy.ExecuteError()
            print("Append Complete")
            edit.stopOperation()

            edit.stopEditing(True)

        except:
            print("Exception Raised, stopping edits")
            edit.undoOperation()
            edit.abortOperation()
            edit.stopEditing(False)