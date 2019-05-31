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

        self.workspace = "in_memory"

    def copy_rehab_results_from_nbcr_data_to_memory(self, output_table_name):
        input_table = self.config.rehab_nbcr_data_sde_path
        in_memory_table = self.rrad_db_data_io.workspace + "\\" + output_table_name
        fields = RehabResult.nbcr_data_field_attribute_lookup().keys()
        active_segments_sql = "hservstat not in ( 'ABAN' , 'TBAB' , 'DNE' )"
        whole_pipe_sql = "cutno = 0 and compkey is not Null"
        where_clause = active_segments_sql + " and " + whole_pipe_sql
        arcpy.MakeQueryTable_management(input_table, in_memory_table, "", "", fields, where_clause)

    def copy_rehab_results_from_rehab_branches_to_memory(self, output_table_name):
        input_table = self.config.rehab_branches_sde_path
        in_memory_table = self.rrad_db_data_io.workspace + "\\" + output_table_name
        fields = RehabResult.rehab_branches_field_attribute_lookup().keys()
        arcpy.MakeQueryTable_management(input_table, in_memory_table, "", "", fields, "")

    def copy_rehab_results_from_tv_ratings_to_memory(self, output_table_name):
        input_table = self.config.tv_ratings_sde_path
        in_memory_table = self.rrad_db_data_io.workspace + "\\" + output_table_name
        fields = RehabResult.tv_ratings_field_attribute_lookup().keys()
        arcpy.MakeQueryTable_management(input_table, in_memory_table, "", "", fields, "")

    def copy_rehab_results_to_memory(self, rehab_results_table_name, rehab):
        rehab_results_from_rehab_branches_table_name = "rehab_results_from_rehab_branches"
        rehab_results_from_tv_ratings_table_name = "rehab_results_from_tv_ratings"
        fields_rehab_branches = ["BPW"]
        fields_tv_ratings = ["ROOT_RATING"]
        output_table = self.rrad_db_data_io.workspace + "\\" + rehab_results_table_name
        rehab_results_from_rehab_branches_table = self.rrad_db_data_io.workspace + "\\" + rehab_results_from_rehab_branches_table_name
        rehab_results_from_tv_ratings_table = self.rrad_db_data_io.workspace + "\\" + rehab_results_from_tv_ratings_table_name
        self.copy_rehab_results_from_nbcr_data_to_memory(rehab_results_table_name)
        self.copy_rehab_results_from_rehab_branches_to_memory(rehab_results_from_rehab_branches_table_name)
        self.copy_rehab_results_from_tv_ratings_to_memory(rehab_results_from_tv_ratings_table_name)
        arcpy.JoinField_management(output_table, "compkey", rehab_results_from_rehab_branches_table, "compkey", fields_rehab_branches)
        arcpy.JoinField_management(output_table, "GLOBALID", rehab_results_from_tv_ratings_table, "GLOBALID", fields_tv_ratings)
        self.rrad_db_data_io.add_parent_id(rehab_results_table_name, "rehab_id", rehab.id)

    def append_rehab_results(self, rehab):
        self.rrad_db_data_io.append_objects_to_db(rehab.rehab_results, RehabResult.input_field_attribute_lookup(),
                                 self.config.rehab_results_sde_path,
                                 self.config.rehab_results_sde_path)



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

        rehab.rehab_results = self.create_rehab_results(rehab_id)

        rehab.calculate_apw()
        rehab.calculate_capital_cost()

        self.write_rehab_results_to_table(rehab)
        self.delete_fields_except_compkey_from_feature()
        self.join_output_pipe_table_and_geometry()
        self.append_whole_pipes_to_rehab_results()

        return rehab.id
