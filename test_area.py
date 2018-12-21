from unittest import TestCase
import mock
from mock_config import MockConfig
from area import Area
from simulation import Simulation

class TestArea(TestCase):

    def setUp(self):
        mock_config = MockConfig()

        self.mock_simulation = mock.MagicMock(Simulation)
        self.mock_simulation.storm_id = 1
        self.area = Area(mock_config.config)
        self.area.first_floor_elev_ft = 8
        self.area.san_crown_elev_ft = -1
        self.area.maxHGL = .1
        self.area.has_basement = "Y"
        self.area.area_type = "BLDG"



    def test_ffe_above_crown_ffe_greater_than_or_equal_to_8_feet_from_crown_returns_true(self):
        self.area.first_floor_elev_ft = 8
        self.area.san_crown_elev_ft = 0
        self.assertTrue(self.area.ffe_above_crown())

    def test_ffe_above_crown_ffe_less_than_8_feet_from_crown_returns_false(self):
        self.area.first_floor_elev_ft = 7
        self.area.san_crown_elev_ft = 0
        self.assertFalse(self.area.ffe_above_crown())

    def test_ffe_above_crown_invalid_elevations_throws_exception(self):
        self.area.first_floor_elev_ft = None
        self.area.san_crown_elev_ft = 0
        with self.assertRaises(Exception):
            self.area.ffe_above_crown()

    def test_max_hgl_above_basement_elev_less_than_basement_depth_returns_true(self):
        self.area.maxHGL = 7
        self.area.first_floor_elev_ft = 8
        self.assertTrue(self.area.max_hgl_above_basement_elev())

    def test_max_hgl_above_basement_elev_greater_than_or_equal_to_basement_depth_returns_false(self):
        self.area.maxHGL = 0
        self.area.first_floor_elev_ft = 8
        self.assertFalse(self.area.max_hgl_above_basement_elev())

    def test_max_hgl_above_basement_elev_greater_than_or_equal_to_basement_depth_returns_false(self):
        self.area.maxHGL = 0
        self.area.first_floor_elev_ft = None
        with self.assertRaises(Exception):
            self.area.max_hgl_above_basement_elev()

    def test_basement_exists_if_Y_returns_true(self):
        self.area.has_basement = "Y"
        self.assertTrue(self.area.basement_exists())

    def test_basement_exists_if_U_returns_true(self):
        self.area.has_basement = "U"
        self.assertTrue(self.area.basement_exists())

    def test_basement_exists_if_N_returns_false(self):
        self.area.has_basement = "N"
        self.assertFalse(self.area.basement_exists())

    def test_basement_exists_if_not_Y_or_U_or_N_raises_exception(self):
        self.area.has_basement = "7"
        with self.assertRaises(Exception):
            self.area.basement_exists()

    def test_basement_flooding_ffe_above_crown_and_max_hgl_above_basement_and_basement_exists_and_is_building_returns_true(self):
        self.assertTrue(self.area.basement_flooding())


    def test_basement_flooding_ffe_below_crown_and_max_hgl_above_basement_and_basement_exists_and_is_building_returns_true(self):
        self.area.first_floor_elev_ft = 7
        self.area.san_crown_elev_ft = 0
        self.assertFalse(self.area.basement_flooding())

    def test_basement_flooding_ffe_above_crown_and_max_hgl_below_basement_and_basement_exists_and_is_building_returns_true(self):
        self.area.maxHGL = 0
        self.assertFalse(self.area.basement_flooding())

    def test_basement_flooding_ffe_above_crown_and_max_hgl_above_basement_and_basement__does_not_exist_and_is_building_returns_true(self):
        self.area.has_basement = "N"
        self.assertFalse(self.area.basement_flooding())

    def test_basement_flooding_ffe_above_crown_and_max_hgl_above_basement_and_basement_exists_and_is_not_building_returns_true(self):
        self.area.area_type = "STRT"
        self.assertFalse(self.area.basement_flooding())

    def test_calculate_bsbr_no_basement_flooding_is_0(self):
        self.area.has_basement = "N"
        self.area.calculate_bsbr(self.mock_simulation)
        self.assertEqual(self.area.bsbr, 0)

    def test_calculate_bsbr_basement_flooding_25_year_storm_is_correct(self):
        self.storm_bsbr_lookup = {"2yr6h": 91535, "5yr6h": 36614, "25yr6h": 7323}
        self.area.storm_bsbr_lookup = self.storm_bsbr_lookup
        self.area.calculate_bsbr(self.mock_simulation)
        self.assertAlmostEqual(self.area.bsbr, 7323)

    def test_calculate_bsbr_basement_flooding_5_year_storm_is_correct(self):
        self.storm_bsbr_lookup = {"2yr6h": 91535, "10yr6h": 36614, "25yr6h": 7323}
        self.area.storm_bsbr_lookup = self.storm_bsbr_lookup
        self.mock_simulation.storm_id = 2
        self.area.calculate_bsbr(self.mock_simulation)
        self.assertAlmostEqual(self.area.bsbr, 36614)

    def test_calculate_bsbr_unknown_storm_throws_Exception(self):
        self.storm_bsbr_lookup = {"2yr6h": 91535, "10yr6h": 36614, "25yr6h": 7323}
        self.area.storm_bsbr_lookup = self.storm_bsbr_lookup
        self.mock_simulation.storm_id = 10
        with self.assertRaises(Exception):
            self.area.calculate_bsbr(self.mock_simulation)

    #TODO: add other tests for other values and exceptions


