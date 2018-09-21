import arcpy
try:
    from typing import List, Any
except:
    pass
from config import Config


class RehabDataIO():
    def __init__(self, config):
        # type: (Config) -> None
        self.config = config

        self.active_whole_pipe_layer = "nbcr_data_whole_pipes_layer"
        self.active_whole_pipe_feature_class = "nbcr_data_whole_pipes"
        self.rehab_branches_feature_class = "rehab_branches"

        self.workspace = "in_memory"
        self.active_whole_pipe_feature_class_path = self.workspace + "/" + self.active_whole_pipe_feature_class
        self.rehab_branches_feature_class_path = self.workspace + "/" + self.rehab_branches_feature_class

    def select_nbcr_data_pipes(self):
        select_active_segments_sql = "hservstat not in ( 'ABAN' , 'TBAB' , 'DNE' )"
        select_whole_pipe_sql = "cutno = 0 and compkey is not Null"
        select_active_whole_pipe_sql = select_active_segments_sql + " and " + select_whole_pipe_sql

        arcpy.MakeFeatureLayer_management(self.config.rehab_nbcr_data_sde_path, self.active_whole_pipe_layer,
                                          select_active_whole_pipe_sql, self.workspace)

    def create_pipe_feature_class(self):
        arcpy.CopyFeatures_management(self.active_whole_pipe_layer, self.active_whole_pipe_feature_class_path)

    def create_branches_feature_class(self):
        arcpy.CopyRows_management(self.config.rehab_branches_sde_path,
                                      self.rehab_branches_feature_class_path)

    def delete_nbcr_data_bpw_field(self):
        arcpy.DeleteField_management(self.active_whole_pipe_feature_class_path, "BPW")

    def add_bpw_from_branches(self):
        arcpy.JoinField_management(self.active_whole_pipe_feature_class_path,
                                   "compkey",
                                   self.rehab_branches_feature_class_path,
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

#TODO: make unit test match what we did in append_whole_pipes_to_rehab_results and patch the edit sessions to append whole pipes