import mock
from config import Config

class MockConfig():
    def __init__(self):
        self.config = mock.MagicMock(Config)
        self.config.model_catalog_sde_path = "model_catalog_sde_path"
        self.config.model_catalog_current_id_table_sde_path = "model_catalog_current_id_table_sde_path"
        self.config.model_tracking_sde_path = "model_tracking_sde_path"
        self.config.simulation_sde_path = "simulation_sde_path"
        self.config.rehab_nbcr_data_sde_path = "rehab_nbcr_data_sde_path"
        self.config.rehab_branches_sde_path = "rehab_branches_sde_path"
        self.config.rrad_current_id_table_sde_path = "rrad_current_id_table_sde_path"

        self.config.RRAD_sde_path = "RRAD_sde_path"
        self.config.area_results_sde_path = "area_results_sde_path"
        self.config.link_results_sde_path = "link_results_sde_path"
        self.config.node_results_sde_path = "node_results_sde_path"
        self.config.flooding_results_sde_path = "flooding_results_sde_path"
        self.config.rehab_results_sde_path = "rehab_results_sde_path"
        self.config.rehab_tracking_sde_path = "rehab_tracking_sde_path"

        self.config.EMGAATS_sde_path = "EMGAATS_sde_path"
        self.config.storms_sde_path = "storms_sde_path"
        self.config.storm_types_sde_path = "storm_types_sde_path"
        self.config.dev_scenarios_sde_path = "dev_scenarios_sde_path"

        self.config.storm = {0: ("user_def", "U"), 1: ("25yr6h", "D"), 2: ("10yr6h", "D")}
        self.config.storm_id = {("user_def", "U"): 0, ("25yr6h", "D"): 1, ("10yr6h", "D"): 2}

        self.config.dev_scenario = {0: "EX", 1: "50", 2: "BO"}
        self.config.dev_scenario_id = {"EX": 0, "50": 1, "BO": 2}

        self.config.standard_simulation_names.return_value = ['D25yr6h', 'D25yr6h-50', 'D25yr6h-BO', 'D10yr6h', 'D10yr6h-50', 'D10yr6h-BO']

        # self.config.engine_type =
        # self.config.engine_type_id =
        #
        self.config.model_alteration = {0: "zero", 1: "one", 2: "two"}
        self.config.model_alteration_id = {"zero": 0, "one": 1, "two": 2}
        #
        # self.config.model_purpose =
        # self.config.model_purpose_id =
        #
        # self.config.model_status =
        # self.config.model_status_id =
        #
        # self.config.proj_phase =
        # self.config.proj_phase_id =
        #
        # self.config.proj_type =
        # self.config.proj_type_id =

