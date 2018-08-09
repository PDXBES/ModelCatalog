import os


class Config:
    def __init__(self):
        self.storm = {0: ("user_def", "U"), 1: ("25yr6h", "D"), 2: ("10yr6h", "D")}
        self.dev_scenario = {0: "EX", 1: "50", 2: "BO"}
        executable_path = os.path.dirname(os.path.realpath(__file__))
        self.dummy_model_calibration_file_path = executable_path + "\\" + "DummyFiles" + "\\" + "model_calibration_file.xlsx"
        self.dummy_model_alteration_file_path = executable_path + "\\" + "DummyFiles" + "\\" + "model_alteration_file.xlsx"

        sde_connections = r"\\besfile1\ccsp\03_WP2_Planning_Support_Tools\03_RRAD\Model_Catalog\Dev\connection_files"

        model_catalog_test_sde = r"BESDBTEST1.MODELCATALOG.sde"
        self.model_catalog_sde_path = os.path.join(sde_connections, model_catalog_test_sde)
        self.next_id_table_sde_path = self.model_catalog_sde_path + r"\MODEL_CATALOG.GIS.VAT_MaxVal"
        self.model_tracking_sde_path = self.model_catalog_sde_path + r"\MODEL_CATALOG.GIS.ModelTracking"

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


