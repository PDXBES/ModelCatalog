import os
import arcpy
try:
    from typing import Dict
    from typing import List
except:
    pass

class Config:
    def __init__(self):
        executable_path = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..'))

        self.dummy_model_calibration_file_path = executable_path + "\\" + "DummyFiles" + "\\" + "model_calibration_file.xlsx"
        self.dummy_model_alteration_file_path = executable_path + "\\" + "DummyFiles" + "\\" + "model_alteration_file.xlsx"

        sde_connections = r"\\besfile1\CCSP\03_WP2_Planning_Support_Tools\03_RRAD\CCSP_Data_Management_ToolBox\connection_files"

        model_catalog_test_sde = r"BESDBTEST1.MODELCATALOG.sde"
        self.model_catalog_sde_path = os.path.join(sde_connections, model_catalog_test_sde)
        self.model_catalog_current_id_table_sde_path = self.model_catalog_sde_path + r"\MODEL_CATALOG.GIS.Current_ID"
        self.model_tracking_sde_path = self.model_catalog_sde_path + r"\MODEL_CATALOG.GIS.ModelTracking"
        self.simulation_sde_path = self.model_catalog_sde_path + r"\MODEL_CATALOG.GIS.Simulation"

        self.model_alt_bc_sde_path = self.model_catalog_sde_path + r"\MODEL_CATALOG.GIS.Model_Alt_BC"
        self.model_alt_hydraulic_sde_path = self.model_catalog_sde_path + r"\MODEL_CATALOG.GIS.Model_Alt_Hydraulic"
        self.model_alt_hydrologic_sde_path = self.model_catalog_sde_path + r"\MODEL_CATALOG.GIS.Model_Alt_Hydrologic"

        self.project_type_sde_path = self.model_catalog_sde_path + r"\MODEL_CATALOG.GIS.Project_Type"

        rehab_test_sde = r"BESDBTEST1.REHAB.sde"
        self.rehab_test_sde_path = os.path.join(sde_connections, rehab_test_sde)
        self.rehab_nbcr_data_sde_path = self.rehab_test_sde_path + r"\REHAB.GIS.nBCR_Data"
        self.rehab_branches_sde_path = self.rehab_test_sde_path + r"\REHAB.GIS.REHAB_Branches"

        RRAD_test_sde = r"BESDBTEST1.RRAD_write.sde"
        self.RRAD_sde_path = os.path.join(sde_connections, RRAD_test_sde)

        self.rehab_tracking_sde_path = self.RRAD_sde_path + r"\RRAD.GIS.Rehab_Tracking"
        self.area_results_sde_path = self.RRAD_sde_path + r"\RRAD.GIS.AreaResults"
        self.link_results_sde_path = self.RRAD_sde_path + r"\RRAD.GIS.LinkResults"
        self.node_results_sde_path = self.RRAD_sde_path + r"\RRAD.GIS.NodeResults"
        self.flooding_results_sde_path = self.RRAD_sde_path + r"\RRAD.GIS.NodeFloodingResults"
        self.rehab_results_sde_path = self.RRAD_sde_path + r"\RRAD.GIS.Rehab_Results"
        self.rrad_current_id_table_sde_path = self.RRAD_sde_path + r"\RRAD.GIS.Current_ID"

        self.bsbr_results_sde_path = self.RRAD_sde_path + r"\RRAD.GIS.BSBR_results"

        EMGAATS_test_sde = r"BESDBTEST1.EMGAATS.sde"
        self.EMGAATS_sde_path = os.path.join(sde_connections, EMGAATS_test_sde)

        self.storms_sde_path = self.EMGAATS_sde_path + r"\EMGAATS.GIS.STORMS"
        self.storm_types_sde_path = self.EMGAATS_sde_path + r"\EMGAATS.GIS.STORMTYPES"
        self.dev_scenarios_sde_path = self.EMGAATS_sde_path + r"\EMGAATS.GIS.DEVSCENARIOS"

        ASM_WORK_test_sde = r"BESDBTEST1.ASM_WORK.sde"
        self.ASM_WORK_sde_path = os.path.join(sde_connections, ASM_WORK_test_sde)

        self.analysis_requests_sde_path = self.ASM_WORK_sde_path + r"\ASM_Work.GIS.Analysis_Requests"

        self.storm = self.retrieve_storm_dict()  # {0: ("user_def", "U"), 1: ("25yr6h", "D"), 2: ("10yr6h", "D")}
        self.storm_id = self.reverse_dict(self.storm)

        self.dev_scenario = self.retrieve_dev_scenario_dict()  # {0: "EX", 1: "50", 2: "BO"}
        self.dev_scenario_id = self.reverse_dict(self.dev_scenario)

        self.engine_type = self.retrieve_engine_type_domain_as_dict()
        self.engine_type_id = self.reverse_dict(self.engine_type)

        self.model_alt_bc = self.retrieve_model_alt_bc_domain_as_dict()
        self.model_alt_bc_id = self.reverse_dict(self.model_alt_bc)

        self.model_alt_hydraulic = self.retrieve_model_alt_hydraulic_domain_as_dict()
        self.model_alt_hydraulic_id = self.reverse_dict(self.model_alt_hydraulic)

        self.model_alt_hydrologic = self.retrieve_model_alt_hydrologic_domain_as_dict()
        self.model_alt_hydrologic_id = self.reverse_dict(self.model_alt_hydrologic)

        self.model_purpose = self.retrieve_model_purpose_domain_as_dict()
        self.model_purpose_id = self.reverse_dict(self.model_purpose)

        self.model_status = self.retrieve_model_status_domain_as_dict()
        self.model_status_id = self.reverse_dict(self.model_status)

        self.proj_phase = self.retrieve_proj_phase_domain_as_dict()
        self.proj_phase_id = self.reverse_dict(self.proj_phase)

        self.proj_type = self.retrieve_proj_type_domain_as_dict()
        self.proj_type_id = self.reverse_dict(self.proj_type)

        self.cip_analysis_requests = self.retrieve_cip_analysis_request_dict()
        self.unique_cip_numbers = self.get_unique_cip_numbers()
        #TODO - move piece to remove unicode empty string to separate function

    def get_unique_cip_numbers(self):
        unique_cip_numbers = []
        unique_cip_numbers_w_empty_unicode_string = self.get_unique_values_case_insensitive(self.cip_analysis_requests)
        for cip_number in unique_cip_numbers_w_empty_unicode_string:
            if cip_number != u'':
                unique_cip_numbers.append(cip_number)

        return sorted(unique_cip_numbers, reverse = True)

    def standard_simulation_names(self):
        standard_simulation_names = []
        for storm in self.storm.values():
            if storm != ("user_def", "U"):
                for scenario in self.dev_scenario.values():
                    simulation_name = ""
                    type_and_storm_name = storm[1] + storm[0]
                    if scenario == "EX":
                        simulation_name = type_and_storm_name
                    else:
                        simulation_name = type_and_storm_name + "-" + scenario
                    standard_simulation_names.append(simulation_name)
        return standard_simulation_names

    def retrieve_domain_as_dict(self, domain_name):
        list_of_domains = arcpy.da.ListDomains(self.model_catalog_sde_path)
        dict_of_scenarios = None
        for domain in list_of_domains:
            if domain.name == domain_name:
                dict_of_scenarios = domain.codedValues
                break
        return dict_of_scenarios

    def retrieve_engine_type_domain_as_dict(self):
        return self.retrieve_domain_as_dict("Engine_Type")

    def retrieve_model_alt_bc_domain_as_dict(self):
        return self.retrieve_domain_as_dict("Model_Alt_BC")

    def retrieve_model_alt_hydraulic_domain_as_dict(self):
        return self.retrieve_domain_as_dict("Model_Alt_Hydraulic")

    def retrieve_model_alt_hydrologic_domain_as_dict(self):
        return self.retrieve_domain_as_dict("Model_Alt_Hydrologic")

    def retrieve_model_purpose_domain_as_dict(self):
        return self.retrieve_domain_as_dict("Model_Purpose")

    def retrieve_model_status_domain_as_dict(self):
        return self.retrieve_domain_as_dict("Model_Status")

    def retrieve_proj_phase_domain_as_dict(self):
        return self.retrieve_domain_as_dict("Proj_Phase")

    def retrieve_proj_type_domain_as_dict(self):
        return self.retrieve_domain_as_dict("Proj_Type")

    def retrieve_storm_dict(self):
        storm_id = "storm_id"
        storm_fields = ["storm_name", "storm_type"]
        storm_dict = self.retrieve_dict_from_db(storm_id, storm_fields, self.storms_sde_path)
        return storm_dict

    def retrieve_dev_scenario_dict(self):
        dev_scenario_id = "dev_scenario_id"
        dev_scenario_fields = ["dev_scenario"]
        dev_scenario_dict = self.retrieve_dict_from_db(dev_scenario_id, dev_scenario_fields, self.dev_scenarios_sde_path)
        return dev_scenario_dict

    def retrieve_cip_analysis_request_dict(self):
        ar_id = "AR_ID"
        cip_fields = ["ProjectNumber"]
        list_of_keys_and_values = []
        analysis_request_dict = self.retrieve_dict_from_db(ar_id, cip_fields, self.analysis_requests_sde_path)
        for key, value in analysis_request_dict.iteritems():
            if value != None:
                list_of_keys_and_values.append((key, value))

        cip_analysis_request_dict = dict(list_of_keys_and_values)
        return cip_analysis_request_dict

    def get_keys_based_on_value(self, input_dict, input_value):
        keys = []
        for key, value in input_dict.iteritems():
            if value == input_value:
                keys.append(key)
        return keys

    def get_unique_values(self, input_dict):
        # type:(Dict) -> List
        values = input_dict.values()
        output_list = list(set(values))
        return output_list

    def get_unique_values_case_insensitive(self, input_dict):
        # type:(Dict) -> List
        unique_value_list = self.get_unique_values(input_dict)
        uppercase_value_list = [value.upper() for value in unique_value_list]
        unique_uppercase_value_list = list(set(uppercase_value_list))
        return unique_uppercase_value_list

    def get_keys_based_on_value_case_insensitive(self, input_dict, input_value):
        keys = []
        for key, value in input_dict.iteritems():
            if input_value.upper() == value.upper():
                keys.append(key)
        return keys

    def get_cip_analysis_requests(self, cip_number):
        cip_analysis_requests = self.get_keys_based_on_value_case_insensitive(self.cip_analysis_requests, cip_number)

        return cip_analysis_requests

    def retrieve_dict_from_db(self, key_field, value_fields, db_table):
        # type: (str, List[str], str) -> Dict
        fields = [key_field] + value_fields
        values = []
        db_dict_keys = []
        cursor = arcpy.da.SearchCursor(db_table, fields)
        for row in cursor:
            db_dict_keys.append(row[0])
            if len(value_fields) > 1:
                values.append(row[1:len(row)])
            else:
                values.append(row[1])
        db_dict = dict(zip(db_dict_keys, values))
        del cursor
        return db_dict


    def reverse_dict(self, dictionary):
        # type: (Dict) -> Dict
        reverse_dictionary = dict(zip(dictionary.values(), dictionary.keys()))
        return reverse_dictionary