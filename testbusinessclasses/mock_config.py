import mock
from businessclasses.config import Config

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
        self.config.project_type_sde_path = "project_type_sde_path"
        self.config.required_simulations_sde_path = "required_simulations_sde_path"


        self.config.RRAD_sde_path = "RRAD_sde_path"
        self.config.area_results_sde_path = "area_results_sde_path"
        self.config.link_results_sde_path = "link_results_sde_path"
        self.config.node_results_sde_path = "node_results_sde_path"
        self.config.node_flooding_results_sde_path = "node_flooding_results_sde_path"
        self.config.rehab_results_sde_path = "rehab_results_sde_path"
        self.config.rehab_tracking_sde_path = "rehab_tracking_sde_path"
        self.config.directors_sde_path = "directors_sde_path"

        self.config.model_alt_bc_sde_path = "model_alt_bc_sde_path"
        self.config.model_alt_hydrologic_sde_path = "model_alt_hydrologic_sde_path"
        self.config.model_alt_hydraulic_sde_path = "model_alt_hydraulic_sde_path"

        self.config.RRAD_MAPPING_sde_path = "RRAD_MAPPING_sde_path"
        self.config.areas_sde_path = "areas_sde_path"
        self.config.current_id_sde_path = "current_id_sde_path"
        self.config.links_sde_path = "links_sde_path"
        self.config.nodes_sde_path = "nodes_sde_path"
        self.config.snapshot_tracking_sde_path = "snapshot_tracking_sde_path"

        self.config.EMGAATS_sde_path = "EMGAATS_sde_path"
        self.config.storms_sde_path = "storms_sde_path"
        self.config.storm_types_sde_path = "storm_types_sde_path"
        self.config.dev_scenarios_sde_path = "dev_scenarios_sde_path"


        self.config.storm = {0: ("User-defined", "U"), 1: ("25yr6h", "D"), 2: ("10yr6h", "D")}
        self.config.storm_id = {("User-defined", "U"): 0, ("25yr6h", "D"): 1, ("10yr6h", "D"): 2}

        self.config.dev_scenario = {0: "EX", 1: "50", 2: "BO"}
        self.config.dev_scenario_id = {"EX": 0, "50": 1, "BO": 2}

        self.config.standard_simulation_names.return_value = ['D25yr6h', 'D25yr6h-50', 'D25yr6h-BO', 'D10yr6h', 'D10yr6h-50', 'D10yr6h-BO']

        # self.config.engine_type =
        # self.config.engine_type_id =
        #
        self.config.model_alt_bc = {0: "zero_bc", 1: "one_bc", 2: "two_bc"}
        self.config.model_alt_bc_id = {"zero_bc": 0, "one_bc": 1, "two_bc": 2}

        self.config.model_alt_hydrologic = {0: "zero_hydrologic", 1: "one_hydrologic", 2: "two_hydrologic"}
        self.config.model_alt_hydrologic_id = {"zero_hydrologic": 0, "one_hydrologic": 1, "two_hydrologic": 2}

        self.config.model_alt_hydraulic = {0: "zero_hydraulic", 1: "one_hydraulic", 2: "two_hydraulic"}
        self.config.model_alt_hydraulic_id = {"zero_hydraulic": 0, "one_hydraulic": 1, "two_hydraulic": 2}

        self.config.ccsp_characterization_storm_and_dev_scenario_ids = [(1, 0), (2, 1)]
        self.config.ccsp_alternative_storm_and_dev_scenario_ids = [(3, 4), (2, 1)]
        self.config.ccsp_recommended_plan_storm_and_dev_scenario_ids = [(5, 0), (2, 1)]

        self.config.model_purpose = {0: "Characterization", 1: "Alternative", 2: "Recommended Plan", 3: "Calibration"}
        self.config.model_purpose_id = {"Characterization": 0, "Alternative": 1, "Recommended Plan": 2, "Calibration": 3}

        self.config.model_status = {0: "Working", 1: "Final"}
        self.config.model_status_id = {"Working": 0, "Final": 1}

        self.config.proj_phase = {0: "Planning", 1: "Pre Design", 2: "Design 30", 3: "Design 60", 4: "Design 90"}
        self.config.proj_phase_id = {"Planning": 0, "Pre Design": 1, "Design 30": 2, "Design 60": 3, "Design 90": 4}

         #self.config.proj_type =
        # self.config.proj_type_id =

