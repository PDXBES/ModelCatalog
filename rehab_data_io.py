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

        self.workspace = "c:\\temp\\in_memory.gdb"
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
        arcpy.Copy_management(self.config.rehab_branches_sde_path,
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
        arcpy.Append_management(self.active_whole_pipe_feature_class_path,
                                self.config.rehab_results_sde_path,
                                "NO_TEST")


#TODO: try copy rows to use in_memory