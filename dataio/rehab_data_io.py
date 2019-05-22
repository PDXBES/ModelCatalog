import arcpy
from businessclasses.rehab import Rehab
from dataio.object_data_io import ObjectDataIo
import datetime
try:
    from typing import List, Any
except:
    pass
from businessclasses.config import Config
from businessclasses.rehab_result import RehabResult


class RehabDataIo(ObjectDataIo):
    def __init__(self, config, rrad_db_data_io):
        # type: (Config) -> None
        self.config = config
        self.rrad_db_data_io = rrad_db_data_io
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

        self.whole_pipe_fields = ["compkey",
                                  "bpw",
                                  "usnode",
                                  "dsnode",
                                  "diamwidth",
                                  "length",
                                  "material",
                                  "lateralcost",
                                  "manholecost",
                                  "asmrecommendednbcr",
                                  "asmrecommendedaction",
                                  "apwspot",
                                  "apwliner",
                                  "apwwhole",
                                  "lateralcount",
                                  "globalid",
                                  "FailureYear",
                                  "grade_h5",
                                  "inspDate",
                                  "rrad_rehab_id"]

        self.output_pipes_table_fields = ["compkey",
                                  "bpw",
                                  "usnode",
                                  "dsnode",
                                  "diamwidth",
                                  "length",
                                  "material",
                                  "lateralcost",
                                  "manholecost",
                                  "asmrecommendednbcr",
                                  "asmrecommendedaction",
                                  "apwspot",
                                  "apwliner",
                                  "apwwhole",
                                  "lateralcount",
                                  "globalid",
                                  "FailureYear",
                                  "Integer_Condition_Grade",
                                  "Last_Inspection_Date",
                                  "apw",
                                  "capitalcost",
                                  "rehab_id",
                                  "rrad_rehab_id"]

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
        self.rrad_db_data_io.add_unique_ids(self.nbcr_data_whole_pipe_table_path, "rrad_rehab_id")

        cursor = arcpy.da.SearchCursor(self.nbcr_data_whole_pipe_table_path, self.whole_pipe_fields)
        for row in cursor:
            rehab_result = RehabResult()
            rehab_result.rehab_id = rehab_id
            rehab_result.compkey = row[0]
            rehab_result.bpw = row[1]
            rehab_result.usnode = row[2]
            rehab_result.dsnode = row[3]
            rehab_result.diamwidth = row[4]
            rehab_result.length = row[5]
            rehab_result.material = row[6]
            rehab_result.lateralcost = row[7]
            rehab_result.manholecost = row[8]
            rehab_result.asmrecommendednbcr = row[9]
            rehab_result.asmrecommendedaction = row[10]
            rehab_result.apwspot = row[11]
            rehab_result.apwliner = row[12]
            rehab_result.apwwhole = row[13]
            rehab_result.lateralcount = row[14]
            rehab_result.globalid = row[15]
            rehab_result.failure_year = row[16]
            rehab_result.integer_grade = row[17]
            rehab_result.inspection_date = row[18]
            rehab_result.id = row[19]
            pipes.append(rehab_result)
        return pipes

    def write_pipes_to_table(self, rehab):
        arcpy.CreateTable_management(self.workspace, self.output_pipes_table, self.config.rehab_results_sde_path)
        cursor = arcpy.da.InsertCursor(self.output_pipes_table_path, self.output_pipes_table_fields)
        for pipe in rehab.pipes:
            #if pipe.valid():
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
                row.append(pipe.failure_year)
                row.append(pipe.integer_grade)
                row.append(pipe.inspection_date)
                row.append(pipe.apw)
                row.append(pipe.capitalcost)
                row.append(pipe.rehab_id)
                row.append(pipe.id)
                cursor.insertRow(row)

    def delete_fields(self, feature_class, fields_to_keep):
        uppercase_fields_to_keep = [field.upper() for field in fields_to_keep]
        fields = arcpy.ListFields(feature_class)
        for field in fields:
            if not(field.name.upper() in uppercase_fields_to_keep or field.type == 'Geometry' or field.type == 'OID'):
                arcpy.DeleteField_management(feature_class, field.name)

    def delete_specified_fields(self, feature_class, fields_to_delete):
        uppercase_fields_to_delete = [field.upper() for field in fields_to_delete]
        fields = arcpy.ListFields(feature_class)
        for field in fields:
            if field.name.upper() in uppercase_fields_to_delete and field.name.upper() != 'COMPKEY':
                arcpy.DeleteField_management(feature_class, field.name)

    def delete_fields_except_compkey_from_feature(self):
        fields_to_delete = []
        for field in self.whole_pipe_fields:
            if field.upper() == "COMPKEY":
                pass
            else:
                fields_to_delete.append(field)
        self.delete_specified_fields(self.active_whole_pipe_feature_class_path, fields_to_delete)
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
            raise

    # TODO - write method using add model that uses and edit session like append above

    def create_rehab_snapshot_for_characterization_mapping_snapshot(self):
        rehab_id = self.create_rehab_snapshot("Characterization")
        return rehab_id

    def create_rehab_snapshot(self, purpose):

        rehab_id = self.rrad_db_data_io.retrieve_current_rehab_id()
        rehab = Rehab(self.config)
        rehab.id = rehab_id
        rehab.extract_date = datetime.datetime.today()
        rehab.last_inspection_date = datetime.datetime.today()
        rehab.purpose = purpose
        self.rrad_db_data_io.add_rehab(rehab)

        self.convert_nbcr_data_to_table()

        rehab.pipes = self.create_pipes(rehab_id)

        rehab.calculate_apw()
        rehab.calculate_capital_cost()

        self.write_pipes_to_table(rehab)
        self.delete_fields_except_compkey_from_feature()
        self.join_output_pipe_table_and_geometry()
        self.append_whole_pipes_to_rehab_results()

        return rehab.id
