from unittest import TestCase
import mock
import arcpy
from mock_config import MockConfig
from config import Config

class TestConfig(TestCase):
    def setUp(self):
        mock_config = MockConfig()
        self.config_mock = mock_config.config
        self.config_real = Config()
        self.mock_search_cursor = mock.MagicMock(arcpy.da.SearchCursor)
        self.mock_search_cursor.__iter__.return_value = iter([(1, "02yr6h", "D"), (2, "05yr6h", "D")])
        self.mock_dev_scenario_search_cursor = mock.MagicMock(arcpy.da.SearchCursor)
        self.mock_dev_scenario_search_cursor.__iter__.return_value = iter([(1, "EX"), (2, "50")])

    # def test_storm_dict_return_correct_value_for_storm(self):
    #     storm_name, storm_type = self.config.storm[0]
    #     self.assertEquals(storm_name, "user_def")
    #     self.assertEquals(storm_type, "U")
    #
    # def test_dev_scenario_dict_return_correct_value(self):
    #     dev_scenario = self.config.dev_scenario
    #     self.assertEquals(dev_scenario[0], "EX")
    #
    # def test_storm_id_dict_returns_correct_id_for_storm(self):
    #     storm_id = self.config.storm_id[("user_def", "U")]
    #     self.assertEquals(storm_id, 0)
    #
    # def test_dev_scenario_dict_returns_correct_id_for_dev_scenario(self):
    #     dev_scenario_id = self.config.dev_scenario_id["EX"]
    #     self.assertEquals(dev_scenario_id, 0)

    def test_standard_simulation_names(self):
        standard_simulation_names = ['D25yr6h', 'D25yr6h-50', 'D25yr6h-BO', 'D10yr6h', 'D10yr6h-50', 'D10yr6h-BO']
        output_simulation_names = self.config_mock.standard_simulation_names()
        self.assertEquals(output_simulation_names, standard_simulation_names)

    def test_reverse_dict_returns_reverse_dict(self):
        test_dictionary = {0: "one", 1: "two", 2: "three"}
        reverse_dictionary = {"one": 0, "two": 1, "three": 2}
        test_reverse = self.config_real.reverse_dict(test_dictionary)
        self.assertEquals(test_reverse, reverse_dictionary)

    @mock.patch("arcpy.da.ListDomains")
    def test_retrieve_domain_as_dict_calls_list_of_domains_with_correct_arguments(self, mock_list_of_domains):
        self.config_real.retrieve_domain_as_dict("Engine_Type")
        mock_list_of_domains.assert_called_with(self.config_real.model_catalog_sde_path)

    @mock.patch("arcpy.da.ListDomains")
    def test_retrieve_domain_as_dict_returns_correct_dict(self, mock_list_of_domains):
        mock_domain1 = mock.MagicMock(arcpy.da.Domain)
        mock_domain1.name = "Engine_Type"
        mock_domain1.codedValues = {1: "EMGAATS"}
        mock_domain2 = mock.MagicMock(arcpy.da.Domain)
        mock_domain2.name = "Storm_Type"
        mock_list_of_domains.return_value = [mock_domain1, mock_domain2]
        domain_dict_of_scenarios = self.config_real.retrieve_domain_as_dict("Engine_Type")
        self.assertEquals(domain_dict_of_scenarios, {1: "EMGAATS"})

    @mock.patch("config.Config.retrieve_domain_as_dict")
    def test_retrieve_engine_type_domain_as_dict_called_with_correct_domain_name(self,
                                                                                 mock_retrieve_domain_as_dict):
        self.config_real.retrieve_engine_type_domain_as_dict()
        mock_retrieve_domain_as_dict.assert_called_with("Engine_Type")

    @mock.patch("config.Config.retrieve_domain_as_dict")
    def test_retrieve_model_alterations_domain_as_dict_called_with_correct_domain_name(self,
                                                                                       mock_retrieve_domain_as_dict):
        self.config_real.retrieve_model_alterations_domain_as_dict()
        mock_retrieve_domain_as_dict.assert_called_with("Model_Alterations")

    @mock.patch("config.Config.retrieve_domain_as_dict")
    def test_retrieve_model_purpose_domain_as_dict_called_with_correct_domain_name(self,
                                                                                   mock_retrieve_domain_as_dict):
        self.config_real.retrieve_model_purpose_domain_as_dict()
        mock_retrieve_domain_as_dict.assert_called_with("Model_Purpose")

    @mock.patch("config.Config.retrieve_domain_as_dict")
    def test_retrieve_model_status_domain_as_dict_called_with_correct_domain_name(self,
                                                                                  mock_retrieve_domain_as_dict):
        self.config_real.retrieve_model_status_domain_as_dict()
        mock_retrieve_domain_as_dict.assert_called_with("Model_Status")

    @mock.patch("config.Config.retrieve_domain_as_dict")
    def test_retrieve_proj_phase_domain_as_dict_called_with_correct_domain_name(self,
                                                                                mock_retrieve_domain_as_dict):
        self.config_real.retrieve_proj_phase_domain_as_dict()
        mock_retrieve_domain_as_dict.assert_called_with("Proj_Phase")

    @mock.patch("config.Config.retrieve_domain_as_dict")
    def test_retrieve_proj_type_domain_as_dict_called_with_correct_domain_name(self,
                                                                               mock_retrieve_domain_as_dict):
        self.config_real.retrieve_proj_type_domain_as_dict()
        mock_retrieve_domain_as_dict.assert_called_with("Proj_Type")

    @mock.patch("arcpy.da.SearchCursor")
    def test_retrieve_storms_calls_search_cursor(self, mock_retrieve_storms):
        self.config_real.retrieve_storm_dict()
        self.assertTrue(mock_retrieve_storms.called)

    @mock.patch("arcpy.da.SearchCursor")
    def test_retrieve_storm_dict_calls_search_cursor_with_correct_arguments(self, mock_retrieve_storms):
        self.config_real.retrieve_storm_dict()
        mock_retrieve_storms.assert_called_with(self.config_real.storms_sde_path, ["storm_id", "storm_name", "storm_type"])

    @mock.patch("arcpy.da.SearchCursor")
    def test_retrieve_storm_dict_returns_correct_dictionary(self, mock_retrieve_storms):
        mock_retrieve_storms.return_value = self.mock_search_cursor
        return_dict = {1: ("02yr6h", "D"), 2: ("05yr6h", "D")}
        storm_dict = self.config_real.retrieve_storm_dict()
        self.assertEqual(storm_dict, return_dict)

    @mock.patch("arcpy.da.SearchCursor")
    def test_retrieve_storm_dict_calls_search_cursor(self, mock_retrieve_storms):
        self.config_real.retrieve_storm_dict()
        self.assertTrue(mock_retrieve_storms.called)

    @mock.patch("arcpy.da.SearchCursor")
    def test_retrieve_dev_scenario_dict_calls_search_cursor_with_correct_arguments(self, mock_retrieve_dev_scenario_dict):
        self.config_real.retrieve_dev_scenario_dict()
        mock_retrieve_dev_scenario_dict.assert_called_with(self.config_real.dev_scenarios_sde_path,
                                                           ["dev_scenario_id", "dev_scenario"])

    @mock.patch("arcpy.da.SearchCursor")
    def test_retrieve_dev_scenario_dict_returns_correct_dictionary(self, mock_retrieve_dev_scenario_dict):
        mock_retrieve_dev_scenario_dict.return_value = self.mock_dev_scenario_search_cursor
        return_dict = {1: "EX", 2: "50"}
        dev_scenario_dict = self.config_real.retrieve_dev_scenario_dict()
        self.assertEqual(dev_scenario_dict, return_dict)