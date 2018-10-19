import os
import arcpy
try:
    from typing import Dict
except:
    pass

class Config:
    def __init__(self):
        executable_path = os.path.dirname(os.path.realpath(__file__))
        self.dummy_model_calibration_file_path = executable_path + "\\" + "DummyFiles" + "\\" + "model_calibration_file.xlsx"
        self.dummy_model_alteration_file_path = executable_path + "\\" + "DummyFiles" + "\\" + "model_alteration_file.xlsx"

        sde_connections = r"\\besfile1\CCSP\03_WP2_Planning_Support_Tools\03_RRAD\CCSP_Data_Management_ToolBox\connection_files"

        model_catalog_test_sde = r"BESDBTEST1.MODELCATALOG.sde"
        self.model_catalog_sde_path = os.path.join(sde_connections, model_catalog_test_sde)
        self.model_catalog_current_id_table_sde_path = self.model_catalog_sde_path + r"\MODEL_CATALOG.GIS.Current_ID"
        self.model_tracking_sde_path = self.model_catalog_sde_path + r"\MODEL_CATALOG.GIS.ModelTracking"
        self.simulation_sde_path = self.model_catalog_sde_path + r"\MODEL_CATALOG.GIS.Simulation"
        self.model_alterations_sde_path = self.model_catalog_sde_path + r"\MODEL_CATALOG.GIS.Model_Alterations"
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

        EMGAATS_test_sde = r"BESDBTEST1.EMGAATS.sde"
        self.EMGAATS_sde_path = os.path.join(sde_connections, EMGAATS_test_sde)

        self.storms_sde_path = self.EMGAATS_sde_path + r"\EMGAATS.GIS.STORMS"
        self.storm_types_sde_path = self.EMGAATS_sde_path + r"\EMGAATS.GIS.STORMTYPES"
        self.dev_scenarios_sde_path = self.EMGAATS_sde_path + r"\EMGAATS.GIS.DEVSCENARIOS"

        self.storm = self.retrieve_storm_dict()  # {0: ("user_def", "U"), 1: ("25yr6h", "D"), 2: ("10yr6h", "D")}
        self.storm_id = self.reverse_dict(self.storm)

        self.dev_scenario = self.retrieve_dev_scenario_dict()  # {0: "EX", 1: "50", 2: "BO"}
        self.dev_scenario_id = self.reverse_dict(self.dev_scenario)

        self.engine_type = self.retrieve_engine_type_domain_as_dict()
        self.engine_type_id = self.reverse_dict(self.engine_type)

        self.model_alteration = self.retrieve_model_alterations_domain_as_dict()
        self.model_alteration_id = self.reverse_dict(self.model_alteration)


        self.model_purpose = self.retrieve_model_purpose_domain_as_dict()
        self.model_purpose_id = self.reverse_dict(self.model_purpose)

        self.model_status = self.retrieve_model_status_domain_as_dict()
        self.model_status_id = self.reverse_dict(self.model_status)

        self.proj_phase = self.retrieve_proj_phase_domain_as_dict()
        self.proj_phase_id = self.reverse_dict(self.proj_phase)

        self.proj_type = self.retrieve_proj_type_domain_as_dict()
        self.proj_type_id = self.reverse_dict(self.proj_type)

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

    def retrieve_domain_as_dict(self,domain_name):
        list_of_domains = arcpy.da.ListDomains(self.model_catalog_sde_path)
        dict_of_scenarios = None
        for domain in list_of_domains:
            if domain.name == domain_name:
                dict_of_scenarios = domain.codedValues
                break
        return dict_of_scenarios

    def retrieve_engine_type_domain_as_dict(self):
        return self.retrieve_domain_as_dict("Engine_Type")

    def retrieve_model_alterations_domain_as_dict(self):
        return self.retrieve_domain_as_dict("Model_Alterations")


    def retrieve_model_purpose_domain_as_dict(self):
        return self.retrieve_domain_as_dict("Model_Purpose")

    def retrieve_model_status_domain_as_dict(self):
        return self.retrieve_domain_as_dict("Model_Status")


    def retrieve_proj_phase_domain_as_dict(self):
        return self.retrieve_domain_as_dict("Proj_Phase")


    def retrieve_proj_type_domain_as_dict(self):
        return self.retrieve_domain_as_dict("Proj_Type")

    def retrieve_storm_dict(self):
        storm_field_names = ["storm_id", "storm_name", "storm_type"]
        storm_IDs = []
        storm_types = []
        storm_names = []
        cursor = arcpy.da.SearchCursor(self.storms_sde_path, storm_field_names)
        for row in cursor:
            storm_IDs.append(row[0])
            storm_names.append(row[1])
            storm_types.append(row[2])
        storm_name_and_type = zip(storm_names, storm_types)
        storm_dict = dict(zip(storm_IDs, storm_name_and_type))
        del cursor
        return storm_dict

    def retrieve_dev_scenario_dict(self):
        dev_scenario_field_names = ["dev_scenario_id", "dev_scenario"]
        dev_scenario_IDs = []
        dev_scenario = []
        cursor = arcpy.da.SearchCursor(self.dev_scenarios_sde_path, dev_scenario_field_names)
        for row in cursor:
            dev_scenario_IDs.append(row[0])
            dev_scenario.append(row[1])

        dev_scenario_dict = dict(zip(dev_scenario_IDs, dev_scenario))
        del cursor
        return dev_scenario_dict


    def reverse_dict(self, dictionary):
        # type: (Dict) -> Dict
        reverse_dictionary = dict(zip(dictionary.values(), dictionary.keys()))
        return reverse_dictionary