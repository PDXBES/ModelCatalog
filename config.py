import os
import arcpy

class Config:
    def __init__(self):
        self.storm = {0: ("user_def", "U"), 1: ("25yr6h", "D"), 2: ("10yr6h", "D")}
        self.dev_scenario = {0: "EX", 1: "50", 2: "BO"}
        self.storm_id = dict(zip(self.storm.values(), self.storm.keys()))
        self.dev_scenario_id = dict(zip(self.dev_scenario.values(), self.dev_scenario.keys()))
        executable_path = os.path.dirname(os.path.realpath(__file__))
        self.dummy_model_calibration_file_path = executable_path + "\\" + "DummyFiles" + "\\" + "model_calibration_file.xlsx"
        self.dummy_model_alteration_file_path = executable_path + "\\" + "DummyFiles" + "\\" + "model_alteration_file.xlsx"

        sde_connections = r"\\besfile1\ccsp\03_WP2_Planning_Support_Tools\03_RRAD\Model_Catalog\Dev\connection_files"

        model_catalog_test_sde = r"BESDBTEST1.MODELCATALOG.sde"
        self.model_catalog_sde_path = os.path.join(sde_connections, model_catalog_test_sde)
        self.current_id_table_sde_path = self.model_catalog_sde_path + r"\MODEL_CATALOG.GIS.VAT_MaxVal"
        self.model_tracking_sde_path = self.model_catalog_sde_path + r"\MODEL_CATALOG.GIS.ModelTracking"
        self.simulation_sde_path = self.model_catalog_sde_path + r"\MODEL_CATALOG.GIS.Simulation"

        self.engine_type = self.retrieve_engine_type_domain_as_dict()
        self.engine_type_id = dict(zip(self.engine_type.values(), self.engine_type.keys()))

        self.model_alteration = self.retrieve_model_alterations_domain_as_dict()
        self.model_alteration_id = dict(zip(self.model_alteration.values(), self.model_alteration.keys()))

        self.model_purpose = self.retrieve_model_purpose_domain_as_dict()
        self.model_purpose_id = dict(zip(self.model_purpose.values(), self.model_purpose.keys()))

        self.model_status = self.retrieve_model_status_domain_as_dict()
        self.model_status_id = dict(zip(self.model_status.values(), self.model_status.keys()))

        self.proj_phase = self.retrieve_proj_phase_domain_as_dict()
        self.proj_phase_id = dict(zip(self.proj_phase.values(), self.proj_phase.keys()))

        self.proj_type = self.retrieve_proj_type_domain_as_dict()
        self.proj_type_id = dict(zip(self.proj_type.values(), self.proj_type.keys()))


        RRAD_test_sde = r"BESDBTEST1.RRAD_write.sde"
        self.RRAD_sde_path = os.path.join(sde_connections, RRAD_test_sde)

        self.area_results_sde_path = self.RRAD_sde_path + r"\RRAD.GIS.AreaResults"
        self.link_results_sde_path = self.RRAD_sde_path + r"\RRAD.GIS.LinkResults"
        self.node_results_sde_path = self.RRAD_sde_path + r"\RRAD.GIS.NodeResults"
        self.flooding_results_sde_path = self.RRAD_sde_path + r"\RRAD.GIS.NodeFloodingResults"


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

    #TODO - make this one 1-M
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

