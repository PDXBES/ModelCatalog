import os
import arcpy
from model_catalog_exception import InvalidDevScenarioInRequiredSimulationsTable
from model_catalog_exception import InvalidStormNameOrStormTypeInRequiredSimulationsTable
from model_catalog_exception import InvalidProjectPhase
from model_catalog_exception import InvalidModelPurposeException

try:
    from typing import Dict
    from typing import List
except:
    pass

#TODO: This config is too big to fail, look to break this up logically into smaller configs/utilities
class Config:
    def __init__(self, test_flag):
        init_options = {"PROD": 0, "TEST": 1}

        self.emgaats_design_storms_with_D = ["02yr6h", "05yr6h", "10yr6h", "25yr6h", "50yr6h", "100yr6h", "02yr",
                                             "100yr24hrSCS1A", "05yr", "10yr", "WQ", "25yr", "50yr", "100yr"]

        self.emgaats_design_storms_without_D = ["WQ", "25yr", "50yr", "npdx10s", "100yr", "Dry", "Avg", "AvgSum",
                                                "AvgWin", "SE3s", "SE10s", "npdx3s", "npdx5w"]

        #self.emgaats_historic_storms = ["4S6", "20151031", "20151207"]

        self.test_flag = test_flag

        executable_path = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..'))

        self.dummy_model_calibration_file_path = executable_path + "\\" + "DummyFiles" + "\\" + "model_calibration_file.xlsx"
        self.dummy_model_alteration_file_path = executable_path + "\\" + "DummyFiles" + "\\" + "model_alteration_file.xlsx"

        self.dummy_parent_model_path = executable_path + "\\" + "DummyFiles" + "\\"

        sde_connections = r"\\besfile1\CCSP\03_WP2_Planning_Support_Tools\03_RRAD\CCSP_Data_Management_ToolBox\connection_files"
        #sde_connections = r"\\besfile1\CCSP\03_WP2_Planning_Support_Tools\03_RRAD\CCSP_Data_Management_ToolBox\connection_files_GIS_login"
##
        server = None

        if init_options[test_flag] == 1:
            server = "BESDBTEST1"
        elif init_options[test_flag] == 0:
            server = "BESDBPROD1"

        model_catalog_sde = server + ".MODELCATALOG.sde"
        EMGAATS_sde = server + ".EMGAATS.sde"
        ASM_WORK_sde = server + ".ASM_WORK.sde"
        GISDB1 = "GISDB1.EGH_PUBLIC.sde"

        self.egh_public = os.path.join(sde_connections, GISDB1)
        self.tv_ratings_sde_path = self.egh_public + r"\EGH_Public.ARCMAP_ADMIN.Collection_TVRatings_BES_pdx"

        self.model_catalog_sde_path = os.path.join(sde_connections, model_catalog_sde)

        self.model_catalog_current_id_table_sde_path = self.model_catalog_sde_path + r"\MODEL_CATALOG.GIS.Current_ID"
        self.model_tracking_sde_path = self.model_catalog_sde_path + r"\MODEL_CATALOG.GIS.ModelTracking"
        self.simulation_sde_path = self.model_catalog_sde_path + r"\MODEL_CATALOG.GIS.Simulation"
        self.required_simulations_sde_path = self.model_catalog_sde_path + r"\MODEL_CATALOG.GIS.Required_Simulations"
        self.model_alt_bc_sde_path = self.model_catalog_sde_path + r"\MODEL_CATALOG.GIS.Model_Alt_BC"
        self.model_alt_hydraulic_sde_path = self.model_catalog_sde_path + r"\MODEL_CATALOG.GIS.Model_Alt_Hydraulic"
        self.model_alt_hydrologic_sde_path = self.model_catalog_sde_path + r"\MODEL_CATALOG.GIS.Model_Alt_Hydrologic"
        self.results_area_sde_path = self.model_catalog_sde_path + r"\MODEL_CATALOG.GIS.AreaResults"
        self.results_link_sde_path = self.model_catalog_sde_path + r"\MODEL_CATALOG.GIS.LinkResults"
        self.results_node_sde_path = self.model_catalog_sde_path + r"\MODEL_CATALOG.GIS.NodeResults"
        self.results_node_flooding_sde_path = self.model_catalog_sde_path + r"\MODEL_CATALOG.GIS.NodeFloodingResults"
        self.geometry_areas_sde_path = self.model_catalog_sde_path + r"\MODEL_CATALOG.GIS.Areas"
        self.geometry_links_sde_path = self.model_catalog_sde_path + r"\MODEL_CATALOG.GIS.Links"
        self.geometry_nodes_sde_path = self.model_catalog_sde_path + r"\MODEL_CATALOG.GIS.Nodes"

        self.project_type_sde_path = self.model_catalog_sde_path + r"\MODEL_CATALOG.GIS.Project_Type"
##

        self.EMGAATS_sde_path = os.path.join(sde_connections, EMGAATS_sde)

        self.storms_sde_path = self.EMGAATS_sde_path + r"\EMGAATS.GIS.STORMS"
        self.storm_types_sde_path = self.EMGAATS_sde_path + r"\EMGAATS.GIS.STORMTYPES"
        self.dev_scenarios_sde_path = self.EMGAATS_sde_path + r"\EMGAATS.GIS.DEVSCENARIOS"
##

        self.ASM_WORK_sde_path = os.path.join(sde_connections, ASM_WORK_sde)

        self.analysis_requests_sde_path = self.ASM_WORK_sde_path + r"\ASM_Work.GIS.Analysis_Requests"

        self.storm = self.retrieve_storm_dict()  # eg - {0: ("user_def", "U"), 1: ("25yr6h", "D"), 2: ("10yr6h", "D")}
        self.storm_id = self.reverse_dict(self.storm)

        self.dev_scenario = self.retrieve_dev_scenario_dict()  # eg - {0: "EX", 1: "50", 2: "BO"}
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

        self.ccsp_characterization_storm_and_dev_scenario_ids = self.retrieve_required_storm_and_dev_scenario_ids("Characterization", "Planning")
        self.ccsp_alternative_storm_and_dev_scenario_ids = self.retrieve_required_storm_and_dev_scenario_ids("Alternative", "Planning")
        self.ccsp_recommended_plan_storm_and_dev_scenario_ids = self.retrieve_required_storm_and_dev_scenario_ids("Recommended Plan", "Planning")

    #TODO - move piece to remove unicode empty string to separate function
    def get_unique_cip_numbers(self):
        unique_cip_numbers = []
        unique_cip_numbers_w_empty_unicode_string = self.get_unique_values_case_insensitive(self.cip_analysis_requests)
        for cip_number in unique_cip_numbers_w_empty_unicode_string:
            if cip_number != u'':
                unique_cip_numbers.append(cip_number)

        return sorted(unique_cip_numbers, reverse = True)

    def standard_simulation_names(self):
        # TODO add unit test for this logic related to design storms with D
        standard_simulation_names = []
        for storm in self.storm.values():
            if storm[1] == "D":
                for scenario in self.dev_scenario.values():
                    simulation_name = ""
                    if storm[0] in self.emgaats_design_storms_with_D:
                        type_and_storm_name = storm[1] + storm[0]
                    else:
                        type_and_storm_name = storm[0]
                    if scenario == "EX":
                        simulation_name = type_and_storm_name
                    else:
                        simulation_name = type_and_storm_name + "-" + scenario
                    standard_simulation_names.append(simulation_name)
            elif storm[1] == "H":
                for scenario in self.dev_scenario.values():
                    simulation_name = ""
                    type_and_storm_name = storm[0]
                    if scenario == "EX":
                        simulation_name = type_and_storm_name
                    else:
                        simulation_name = type_and_storm_name + "-" + scenario
                    standard_simulation_names.append(simulation_name)
        return standard_simulation_names

#TODO: give retrieve domain as dict a sde path and refactor to use in mapping snapshot
    def retrieve_domain_as_dict(self, domain_name, sde_path):
        list_of_domains = arcpy.da.ListDomains(sde_path)
        dict_of_scenarios = None
        for domain in list_of_domains:
            if domain.name == domain_name:
                dict_of_scenarios = domain.codedValues
                break
        return dict_of_scenarios

    def retrieve_engine_type_domain_as_dict(self):
        return self.retrieve_domain_as_dict("Engine_Type", self.model_catalog_sde_path)

    def retrieve_model_alt_bc_domain_as_dict(self):
        return self.retrieve_domain_as_dict("Model_Alt_BC", self.model_catalog_sde_path)

    def retrieve_model_alt_hydraulic_domain_as_dict(self):
        return self.retrieve_domain_as_dict("Model_Alt_Hydraulic", self.model_catalog_sde_path)

    def retrieve_model_alt_hydrologic_domain_as_dict(self):
        return self.retrieve_domain_as_dict("Model_Alt_Hydrologic", self.model_catalog_sde_path)

    def retrieve_model_purpose_domain_as_dict(self):
        return self.retrieve_domain_as_dict("Model_Purpose", self.model_catalog_sde_path)

    def retrieve_model_status_domain_as_dict(self):
        return self.retrieve_domain_as_dict("Model_Status", self.model_catalog_sde_path)

    def retrieve_proj_phase_domain_as_dict(self):
        return self.retrieve_domain_as_dict("Proj_Phase", self.model_catalog_sde_path)

    def retrieve_proj_type_domain_as_dict(self):
        return self.retrieve_domain_as_dict("Proj_Type", self.model_catalog_sde_path)

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

    def retrieve_required_storm_and_dev_scenario_ids(self, model_purpose, model_project_phase):
        if model_project_phase == "Planning":
            if model_purpose == "Characterization":
                model_project_phase_and_purpose_field_name = "ccsp_characterization"
            elif model_purpose == "Alternative":
                model_project_phase_and_purpose_field_name = "ccsp_alternative"
            elif model_purpose == "Recommended Plan":
                model_project_phase_and_purpose_field_name = "ccsp_recommended_plan"
            else:
                raise InvalidModelPurposeException()

        else:
            raise InvalidProjectPhase()

        cursor = arcpy.da.SearchCursor(self.required_simulations_sde_path, ["storm_name", "storm_type", "dev_scenario", model_project_phase_and_purpose_field_name])
        simulation_ids = []
        for row in cursor:
            if row[3] == 1:
                storm_name = row[0]
                storm_type = row[1]
                dev_scenario = row[2]
                try:
                    storm_id = self.storm_id[(storm_name, storm_type)]
                except:
                    raise InvalidStormNameOrStormTypeInRequiredSimulationsTable
                try:
                    dev_scenario_id = self.dev_scenario_id[dev_scenario]
                except:
                    raise InvalidDevScenarioInRequiredSimulationsTable

                simulation_ids.append((storm_id, dev_scenario_id))
        del cursor

        return simulation_ids



