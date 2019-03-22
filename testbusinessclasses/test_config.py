from unittest import TestCase
import mock
import arcpy
import os
from mock_config import MockConfig
from businessclasses.config import Config
from businessclasses.model_catalog_exception import InvalidStormNameOrStormTypeInRequiredSimulationsTable
from businessclasses.model_catalog_exception import InvalidDevScenarioInRequiredSimulationsTable
from businessclasses.model_catalog_exception import InvalidModelPurpose
from businessclasses.model_catalog_exception import InvalidProjectPhase

class TestConfig(TestCase):
    def setUp(self):
        mock_config = MockConfig()
        self.config_mock = mock_config.config
        self.config_real = Config("TEST")
        self.mock_search_cursor = mock.MagicMock(arcpy.da.SearchCursor)
        self.mock_search_cursor.__iter__.return_value = iter([(1, "02yr6h", "D"), (2, "05yr6h", "D")])

        self.mock_search_cursor_for_required_simulation_list = mock.MagicMock(arcpy.da.SearchCursor)
        self.mock_search_cursor_for_required_simulation_list.__iter__.return_value = iter([("02yr6h", "D", "EX", 0), ("05yr6h", "D", "50", 1)])

        self.mock_dev_scenario_search_cursor = mock.MagicMock(arcpy.da.SearchCursor)
        self.mock_dev_scenario_search_cursor.__iter__.return_value = iter([(1, "EX"), (2, "50")])

        self.patch_list_of_domains = mock.patch("arcpy.da.ListDomains")
        self.mock_list_of_domains = self.patch_list_of_domains.start()

        self.patch_search_cursor = mock.patch("arcpy.da.SearchCursor")
        self.mock_search_cursor_instance = self.patch_search_cursor.start()
        self.mock_search_cursor_instance.return_value = self.mock_search_cursor

        self.key_field = "key_field"
        self.value_fields = ["field1", "field2"]
        self.db_table = "db_table_path"

    def tearDown(self):
        self.mock_search_cursor_instance = self.patch_search_cursor.stop()
        self.mock_list_of_domains = self.patch_list_of_domains.stop()

    def test_standard_simulation_names(self):
        standard_simulation_names = ['D25yr6h', 'D25yr6h-50', 'D25yr6h-BO', 'D10yr6h', 'D10yr6h-50', 'D10yr6h-BO']
        output_simulation_names = self.config_mock.standard_simulation_names()
        self.assertEquals(output_simulation_names, standard_simulation_names)

    def test_reverse_dict_returns_reverse_dict(self):
        test_dictionary = {0: "one", 1: "two", 2: "three"}
        reverse_dictionary = {"one": 0, "two": 1, "three": 2}
        test_reverse = self.config_real.reverse_dict(test_dictionary)
        self.assertEquals(test_reverse, reverse_dictionary)

    def test_retrieve_domain_as_dict_calls_list_of_domains_with_correct_arguments(self):
        self.config_real.retrieve_domain_as_dict("Engine_Type")
        self.mock_list_of_domains.assert_called_with(self.config_real.model_catalog_sde_path)

    def test_retrieve_domain_as_dict_returns_correct_dict(self):
        mock_domain1 = mock.MagicMock(arcpy.da.Domain)
        mock_domain1.name = "Engine_Type"
        mock_domain1.codedValues = {1: "EMGAATS"}
        mock_domain2 = mock.MagicMock(arcpy.da.Domain)
        mock_domain2.name = "Storm_Type"
        self.mock_list_of_domains.return_value = [mock_domain1, mock_domain2]
        domain_dict_of_scenarios = self.config_real.retrieve_domain_as_dict("Engine_Type")
        self.assertEquals(domain_dict_of_scenarios, {1: "EMGAATS"})

    def test_retrieve_engine_type_domain_as_dict_called_with_correct_domain_name(self):
        with mock.patch.object(self.config_real, "retrieve_domain_as_dict") as mock_retrieve_domain_as_dict:
            self.config_real.retrieve_engine_type_domain_as_dict()
            mock_retrieve_domain_as_dict.assert_called_with("Engine_Type")

    def test_retrieve_model_alt_bc_domain_as_dict_called_with_correct_domain_name(self):
        with mock.patch.object(self.config_real, "retrieve_domain_as_dict") as mock_retrieve_domain_as_dict:
            self.config_real.retrieve_model_alt_bc_domain_as_dict()
            mock_retrieve_domain_as_dict.assert_called_with("Model_Alt_BC")

    def test_retrieve_model_alt_hydraulic_domain_as_dict_called_with_correct_domain_name(self):
        with mock.patch.object(self.config_real, "retrieve_domain_as_dict") as mock_retrieve_domain_as_dict:
            self.config_real.retrieve_model_alt_hydraulic_domain_as_dict()
            mock_retrieve_domain_as_dict.assert_called_with("Model_Alt_Hydraulic")

    def test_retrieve_model_alt_hydrologic_domain_as_dict_called_with_correct_domain_name(self):
        with mock.patch.object(self.config_real, "retrieve_domain_as_dict") as mock_retrieve_domain_as_dict:
            self.config_real.retrieve_model_alt_hydrologic_domain_as_dict()
            mock_retrieve_domain_as_dict.assert_called_with("Model_Alt_Hydrologic")

    def test_retrieve_model_purpose_domain_as_dict_called_with_correct_domain_name(self):
        with mock.patch.object(self.config_real, "retrieve_domain_as_dict") as mock_retrieve_domain_as_dict:
            self.config_real.retrieve_model_purpose_domain_as_dict()
            mock_retrieve_domain_as_dict.assert_called_with("Model_Purpose")

    def test_retrieve_model_status_domain_as_dict_called_with_correct_domain_name(self):
        with mock.patch.object(self.config_real, "retrieve_domain_as_dict") as mock_retrieve_domain_as_dict:
            self.config_real.retrieve_model_status_domain_as_dict()
            mock_retrieve_domain_as_dict.assert_called_with("Model_Status")

    def test_retrieve_proj_phase_domain_as_dict_called_with_correct_domain_name(self):
        with mock.patch.object(self.config_real, "retrieve_domain_as_dict") as mock_retrieve_domain_as_dict:
            self.config_real.retrieve_proj_phase_domain_as_dict()
            mock_retrieve_domain_as_dict.assert_called_with("Proj_Phase")

    def test_retrieve_proj_type_domain_as_dict_called_with_correct_domain_name(self):
        with mock.patch.object(self.config_real, "retrieve_domain_as_dict") as mock_retrieve_domain_as_dict:
            self.config_real.retrieve_proj_type_domain_as_dict()
            mock_retrieve_domain_as_dict.assert_called_with("Proj_Type")

    def test_retrieve_dict_from_db_calls_search_cursor_with_correct_arguments(self):
        self.config_real.retrieve_dict_from_db(self.key_field, self.value_fields, self.db_table)
        self.mock_search_cursor_instance.assert_called_with("db_table_path", ["key_field", "field1", "field2"])

    def test_retrieve_dict_from_db_has_multiple_fields_returns_correct_dictionary(self):
        return_dict = {1: ("02yr6h", "D"), 2: ("05yr6h", "D")}
        storm_dict = self.config_real.retrieve_dict_from_db(self.key_field, self.value_fields, self.db_table)
        self.assertEqual(storm_dict, return_dict)

    def test_retrieve_dict_from_db_has_one_field_returns_correct_dictionary(self):
        return_dict = {1: "EX", 2: "50"}
        self.value_fields = ["field1"]
        self.mock_search_cursor_instance.return_value = self.mock_dev_scenario_search_cursor
        storm_dict = self.config_real.retrieve_dict_from_db(self.key_field, self.value_fields, self.db_table)
        self.assertEqual(storm_dict, return_dict)

    def test_retrieve_storm_dict_calls_retrieve_dict_from_db_with_correct_arguments(self):
        with mock.patch.object(self.config_real, "retrieve_dict_from_db") as mock_retrieve_dict_from_db:
            self.config_real.retrieve_storm_dict()
            mock_retrieve_dict_from_db.assert_called_with("storm_id", ["storm_name", "storm_type"],self.config_real.storms_sde_path)

    def test_retrieve_storm_dict_returns_correct_value(self):
        with mock.patch.object(self.config_real, "retrieve_dict_from_db") as mock_retrieve_dict_from_db:
            mock_retrieve_dict_from_db.return_value = "return value"
            return_value = self.config_real.retrieve_storm_dict()
            self.assertEqual(return_value, "return value")

    def test_retrieve_dev_scenario_dict_calls_retrieve_dict_from_db_with_correct_arguments(self):
        with mock.patch.object(self.config_real, "retrieve_dict_from_db") as mock_retrieve_dict_from_db:
            self.config_real.retrieve_dev_scenario_dict()
            mock_retrieve_dict_from_db.assert_called_with("dev_scenario_id", ["dev_scenario"], self.config_real.dev_scenarios_sde_path)

    def test_retrieve_dev_scenario_dict_returns_correct_value(self):
        with mock.patch.object(self.config_real, "retrieve_dict_from_db") as mock_retrieve_dict_from_db:
            mock_retrieve_dict_from_db.return_value = "return value"
            return_value = self.config_real.retrieve_dev_scenario_dict()
            self.assertEqual(return_value, "return value")

    def test_retrieve_cip_analysis_request_dict_is_called_with_correct_arguments(self):
        with mock.patch.object(self.config_real, "retrieve_dict_from_db") as mock_retrieve_dict_from_db:
            self.config_real.retrieve_cip_analysis_request_dict()
            mock_retrieve_dict_from_db.assert_called_with("AR_ID", ["ProjectNumber"], self.config_real.analysis_requests_sde_path)

    def test_retrieve_cip_analysis_request_dict_returns_correct_value(self):
        with mock.patch.object(self.config_real, "retrieve_dict_from_db") as mock_retrieve_dict_from_db:
            mock_retrieve_dict_from_db.return_value = {"key1": "value", "key2": None}
            return_value = self.config_real.retrieve_cip_analysis_request_dict()
            self.assertEqual(return_value, {"key1": "value"})

    def test_get_unique_values_returns_unique_values(self):
        input_dict = {"key1": "value", "key2": "value", "key3": "value1"}
        unique_values = self.config_real.get_unique_values(input_dict)
        self.assertItemsEqual(unique_values, ["value", "value1"])

    def test_get_unique_values_case_insensitive_returns_unique_values_regardless_of_case(self):
        input_dict = {"key1": "value", "key2": "Value", "key3": "value1"}
        unique_values = self.config_real.get_unique_values_case_insensitive(input_dict)
        self.assertItemsEqual(unique_values, ["VALUE", "VALUE1"])

    def test_get_keys_based_on_value_returns_correct_keys(self):
        test_dict = {"Key1": "value", "Key2": "value", "Key3": "bad_value"}
        test_value = "value"
        check_keys = self.config_real.get_keys_based_on_value(test_dict, test_value)
        self.assertItemsEqual(check_keys, ["Key1", "Key2"])

    def test_get_keys_based_on_value_case_insensitive_returns_correct_keys_regardless_of_value_case(self):
        test_dict = {"Key1": "value", "Key2": "VALUE", "Key3": "bad_value"}
        test_value = "value"
        return_keys = self.config_real.get_keys_based_on_value_case_insensitive(test_dict, test_value)
        self.assertItemsEqual(return_keys, ["Key1", "Key2"])

    def test_get_cip_analysis_requests_returns_correct_cip_requests(self):
        self.config_real.cip_analysis_requests = {"Key1": "e1000", "Key2": "E1000", "Key3": "bad_value"}
        cip_number = "E1000"
        cip_analysis_requests = self.config_real.get_cip_analysis_requests(cip_number)
        self.assertItemsEqual(cip_analysis_requests, ["Key1", "Key2"])

    def test_get_unique_cip_numbers_returns_cip_numbers_without_empty_unicode_string(self):
        input_dict = {"key1": "value1", "key2": "Value", "key3": "value","key4": u''}
        self.config_real.cip_analysis_requests = input_dict
        unique_values = self.config_real.get_unique_cip_numbers()
        self.assertItemsEqual(unique_values, ["VALUE", "VALUE1"])
        self.assertEqual(unique_values[0], "VALUE1")
        self.assertEqual(unique_values[1], "VALUE")

    def test_retrieve_required_storm_and_dev_scenario_ids_with_purpose_characterization_calls_search_cursor_with_correct_arguments(self):
        model_purpose = "Characterization"
        model_project_phase = "Planning"
        self.mock_search_cursor_instance.return_value = self.mock_search_cursor_for_required_simulation_list
        self.config_real.retrieve_required_storm_and_dev_scenario_ids(model_purpose, model_project_phase)
        self.mock_search_cursor_instance.assert_called_with(self.config_real.required_simulations_sde_path, ["storm_name", "storm_type", "dev_scenario", "ccsp_characterization"])

    def test_retrieve_required_storm_and_dev_scenario_ids_with_purpose_characterization_returns_correct_list_of_required_simulations(self):
        model_purpose = "Characterization"
        model_project_phase = "Planning"
        self.mock_search_cursor_instance.return_value = self.mock_search_cursor_for_required_simulation_list
        required_simulations = self.config_real.retrieve_required_storm_and_dev_scenario_ids(model_purpose, model_project_phase)
        self.assertEqual(required_simulations, [(2, 2)])

    def test_retrieve_required_storm_and_dev_scenario_ids_throws_exception_when_storm_name_not_in_storm_id_dict(self):
        model_purpose = "Characterization"
        model_project_phase = "Planning"
        self.mock_search_cursor_for_required_simulation_list.__iter__.return_value = iter([("02yr6h", "D", "EX", 0), ("incorrect_storm_name", "D", "50", 1)])
        self.mock_search_cursor_instance.return_value = self.mock_search_cursor_for_required_simulation_list
        with self.assertRaises(InvalidStormNameOrStormTypeInRequiredSimulationsTable):
            self.config_real.retrieve_required_storm_and_dev_scenario_ids(model_purpose, model_project_phase)

    def test_retrieve_required_storm_and_dev_scenario_ids_throws_exception_when_dev_scenario_not_in_dev_scenario_dict(self):
        model_purpose = "Characterization"
        model_project_phase = "Planning"
        self.mock_search_cursor_for_required_simulation_list.__iter__.return_value = iter([("02yr6h", "D", "EX", 0), ("05yr6h", "D", "incorrect_dev_scenario", 1)])
        self.mock_search_cursor_instance.return_value = self.mock_search_cursor_for_required_simulation_list
        with self.assertRaises(InvalidDevScenarioInRequiredSimulationsTable):
            self.config_real.retrieve_required_storm_and_dev_scenario_ids(model_purpose, model_project_phase)

    def test_retrieve_required_storm_and_dev_scenario_ids_throws_exception_with_invalid_project_phase(self):
        model_purpose = "Characterization"
        model_project_phase = "invalid_project_phase"
        self.mock_search_cursor_for_required_simulation_list.__iter__.return_value = iter(
            [("02yr6h", "D", "EX", 0), ("05yr6h", "D", "incorrect_dev_scenario", 1)])
        self.mock_search_cursor_instance.return_value = self.mock_search_cursor_for_required_simulation_list
        with self.assertRaises(InvalidProjectPhase):
            self.config_real.retrieve_required_storm_and_dev_scenario_ids(model_purpose, model_project_phase)

    def test_retrieve_required_storm_and_dev_scenario_ids_throws_exception_with_invalid_model_purpose(self):
        model_purpose = "Invalid_model_purpose"
        model_project_phase = "Planning"
        self.mock_search_cursor_for_required_simulation_list.__iter__.return_value = iter(
            [("02yr6h", "D", "EX", 0), ("05yr6h", "D", "incorrect_dev_scenario", 1)])
        self.mock_search_cursor_instance.return_value = self.mock_search_cursor_for_required_simulation_list
        with self.assertRaises(InvalidModelPurpose):
            self.config_real.retrieve_required_storm_and_dev_scenario_ids(model_purpose, model_project_phase)

    def test_config_init_with_test_flag_as_true_sde_path_to_test_server(self):
        test_bool = "TEST"
        config = Config(test_bool)
        sde_connections = r"\\besfile1\CCSP\03_WP2_Planning_Support_Tools\03_RRAD\CCSP_Data_Management_ToolBox\connection_files"

        model_catalog_test_sde = r"BESDBTEST1.MODELCATALOG.sde"
        rehab_test_sde = r"BESDBTEST1.REHAB.sde"
        RRAD_test_sde = r"BESDBTEST1.RRAD_write.sde"
        EMGAATS_test_sde = r"BESDBTEST1.EMGAATS.sde"
        ASM_WORK_test_sde = r"BESDBTEST1.ASM_WORK.sde"

        model_catalog_test_sde_path = os.path.join(sde_connections, model_catalog_test_sde)
        rehab_test_sde_path = os.path.join(sde_connections, rehab_test_sde)
        RRAD_test_sde_path = os.path.join(sde_connections, RRAD_test_sde)
        EMGAATS_test_sde_path = os.path.join(sde_connections, EMGAATS_test_sde)
        ASM_WORK_test_sde_path = os.path.join(sde_connections, ASM_WORK_test_sde)

        self.assertEquals(config.model_catalog_sde_path, model_catalog_test_sde_path)
        self.assertEquals(config.rehab_sde_path, rehab_test_sde_path)
        self.assertEquals(config.RRAD_sde_path, RRAD_test_sde_path)
        self.assertEquals(config.EMGAATS_sde_path, EMGAATS_test_sde_path)
        self.assertEquals(config.ASM_WORK_sde_path, ASM_WORK_test_sde_path)
