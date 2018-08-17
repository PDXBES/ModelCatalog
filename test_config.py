from unittest import TestCase
import mock
from config import Config
import arcpy


class TestConfig(TestCase):
    def setUp(self):
        self.config = Config()

    def test_storm_dict_return_correct_value_for_storm(self):
        storm_name, storm_type = self.config.storm[0]
        self.assertEquals(storm_name, "user_def")
        self.assertEquals(storm_type, "U")

    def test_dev_scenario_dict_return_correct_value(self):
        dev_scenario = self.config.dev_scenario
        self.assertEquals(dev_scenario[0], "EX")

    def test_standard_simulation_names(self):
        standard_simulation_names = ['D25yr6h', 'D25yr6h-50', 'D25yr6h-BO', 'D10yr6h', 'D10yr6h-50', 'D10yr6h-BO']
        output_simulation_names = self.config.standard_simulation_names()
        self.assertEquals(output_simulation_names, standard_simulation_names)

    def test_storm_id_dict_returns_correct_id_for_storm(self):
        storm_id = self.config.storm_id[("user_def", "U")]
        self.assertEquals(storm_id, 0)

    def test_dev_scenario_dict_returns_correct_id_for_dev_scenario(self):
        dev_scenario_id = self.config.dev_scenario_id["EX"]
        self.assertEquals(dev_scenario_id, 0)
        
    @mock.patch("arcpy.da.ListDomains")
    def test_retrieve_domain_as_dict_calls_list_of_domains(self, mock_list_of_domains):
        self.config.retrieve_domain_as_dict("Engine_Type")
        self.assertTrue(mock_list_of_domains.called)

    @mock.patch("arcpy.da.ListDomains")
    def test_retrieve_domain_as_dict_calls_list_of_domains_with_correct_arguments(self, mock_list_of_domains):
        self.config.retrieve_domain_as_dict("Engine_Type")
        mock_list_of_domains.assert_called_with(self.config.model_catalog_sde_path)

    @mock.patch("arcpy.da.ListDomains")
    def test_retrieve_domain_as_dict_returns_correct_dict(self, mock_list_of_domains):
        mock_domain1 = mock.MagicMock(arcpy.da.Domain)
        mock_domain1.name = "Engine_Type"
        mock_domain1.codedValues = {1: "EMGAATS"}
        mock_domain2 = mock.MagicMock(arcpy.da.Domain)
        mock_domain2.name = "Storm_Type"
        mock_list_of_domains.return_value = [mock_domain1, mock_domain2]
        domain_dict_of_scenarios = self.config.retrieve_domain_as_dict("Engine_Type")
        self.assertEquals(domain_dict_of_scenarios, {1: "EMGAATS"})

    @mock.patch("config.Config.retrieve_domain_as_dict")
    def test_retrieve_engine_type_domain_as_dict_called_with_correct_domain_name(self,
                                                                                 mock_retrieve_domain_as_dict):
        self.config.retrieve_engine_type_domain_as_dict()
        mock_retrieve_domain_as_dict.assert_called_with("Engine_Type")

    @mock.patch("config.Config.retrieve_domain_as_dict")
    def test_retrieve_model_alterations_domain_as_dict_called_with_correct_domain_name(self,
                                                                                       mock_retrieve_domain_as_dict):
        self.config.retrieve_model_alterations_domain_as_dict()
        mock_retrieve_domain_as_dict.assert_called_with("Model_Alterations")

    @mock.patch("config.Config.retrieve_domain_as_dict")
    def test_retrieve_model_purpose_domain_as_dict_called_with_correct_domain_name(self,
                                                                                   mock_retrieve_domain_as_dict):
        self.config.retrieve_model_purpose_domain_as_dict()
        mock_retrieve_domain_as_dict.assert_called_with("Model_Purpose")

    @mock.patch("config.Config.retrieve_domain_as_dict")
    def test_retrieve_model_status_domain_as_dict_called_with_correct_domain_name(self,
                                                                                       mock_retrieve_domain_as_dict):
        self.config.retrieve_model_status_domain_as_dict()
        mock_retrieve_domain_as_dict.assert_called_with("Model_Status")

    @mock.patch("config.Config.retrieve_domain_as_dict")
    def test_retrieve_proj_phase_domain_as_dict_called_with_correct_domain_name(self,
                                                                                       mock_retrieve_domain_as_dict):
        self.config.retrieve_proj_phase_domain_as_dict()
        mock_retrieve_domain_as_dict.assert_called_with("Proj_Phase")

    @mock.patch("config.Config.retrieve_domain_as_dict")
    def test_retrieve_proj_type_domain_as_dict_called_with_correct_domain_name(self,
                                                                                       mock_retrieve_domain_as_dict):
        self.config.retrieve_proj_type_domain_as_dict()
        mock_retrieve_domain_as_dict.assert_called_with("Proj_Type")