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
        self.active_whole_pipe_feature_class_path = self.workspace + "/" + self.active_whole_pipe_feature_class
        self.rehab_branches_table_path = self.workspace + "/" + self.rehab_branches_feature_class
        self.nbcr_data_whole_pipe_table = "nbcr_data_whole_pipe_table"
        self.nbcr_data_whole_pipe_table_path = self.workspace + "/" +self.nbcr_data_whole_pipe_table

        self.select_active_segments_sql = "hservstat not in ( 'ABAN' , 'TBAB' , 'DNE' )"
        self.select_whole_pipe_sql = "cutno = 0 and compkey is not Null"
        self.select_active_whole_pipe_sql = self.select_active_segments_sql + " and " + self.select_whole_pipe_sql

        self.whole_pipe_fields = ["compkey", "bpw", "usnode",
                                  "dsnode", "diamwidth", "length",
                                  "material", "lateralcost", "manholecost",
                                  "asmrecommendednbcr", "asmrecommendedaction",
                                  "apwspot", "apwliner", "apwwhole", "lateralcount", "globalid"]

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
        arcpy.JoinField_management(self.active_whole_pipe_feature_class_path,
                                   "compkey",
                                   self.rehab_branches_table_path,
                                   "compkey",
                                   "BPW")

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

#TODO: make unit test match what we did in append_whole_pipes_to_rehab_results and patch the edit sessions to append whole pipes