from unittest import TestCase
import mock
from businessclasses.mapping_link import MappingLink
from testbusinessclasses.mock_config import MockConfig
from businessclasses.mapping_snapshot_exception import MaxFlowIsNoneException
from businessclasses.mapping_snapshot_exception import DesignFlowIsNoneException
import datetime

class TestMappingLink(TestCase):

    def setUp(self):
        mock_config = MockConfig()
        self.config = mock_config.config
        self.mapping_link = MappingLink(self.config)

    def test_hydraulically_deficient_max_flow_cfs_divided_by_design_flow_cfs_greater_than_or_equal_to_threshold_returns_true(self):
        threshold = 1.2
        self.mapping_link.design_flow_cfs = 1
        self.mapping_link.max_flow_cfs = self.mapping_link.design_flow_cfs * threshold
        hydraulically_deficient_bool = self.mapping_link.hydraulically_deficient
        self.assertTrue(hydraulically_deficient_bool)

    def test_hydraulically_deficient_max_flow_cfs_divided_by_design_flow_cfs_less_than_threshold_returns_false(self):
        threshold = 1.2
        self.mapping_link.design_flow_cfs = 1
        self.mapping_link.max_flow_cfs = self.mapping_link.design_flow_cfs / threshold
        hydraulically_deficient_bool = self.mapping_link.hydraulically_deficient
        self.assertFalse(hydraulically_deficient_bool)

    def test_hydraulically_deficient_max_flow_cfs_divided_by_design_flow_cfs_design_flow_cfs_is_zero_returns_false(self):
        threshold = 1.2
        self.mapping_link.design_flow_cfs = 0
        self.mapping_link.max_flow_cfs = self.mapping_link.design_flow_cfs * threshold
        hydraulically_deficient_bool = self.mapping_link.hydraulically_deficient
        self.assertFalse(hydraulically_deficient_bool)

    def test_hydraulically_deficient_max_flow_cfs_is_none_raises_MaxFlowIsNoneException(self):
        self.mapping_link.design_flow_cfs = 0
        self.mapping_link.max_flow_cfs = None
        with self.assertRaises(MaxFlowIsNoneException):
            hydraulically_deficient_bool = self.mapping_link.hydraulically_deficient

    def test_hydraulically_deficient_design_flow_cfs_is_none_raises_DesignFlowIsNoneException(self):
        self.mapping_link.design_flow_cfs = None
        self.mapping_link.max_flow_cfs = 1
        with self.assertRaises(DesignFlowIsNoneException):
            hydraulically_deficient_bool = self.mapping_link.hydraulically_deficient

    def test_last_inspection_year_has_valid_last_inspection_date_returns_correct_year(self):
        self.mapping_link.last_inspection_date = datetime.datetime(2015, 1, 1)
        insp_year = self.mapping_link.last_inspection_year
        self.assertEqual(insp_year, 2015)

    def test_last_inspection_year_has_invalid_last_inspection_date_returns_None(self):
        self.mapping_link.last_inspection_date = None
        insp_year = self.mapping_link.last_inspection_year
        self.assertEqual(insp_year, None)

    def test_flow_ratio_link_has_valid_design_and_max_flow_returns_correct_ratio(self):
        self.mapping_link.max_flow_cfs = 1
        self.mapping_link.design_flow_cfs = 2
        flow_ratio = self.mapping_link.flow_ratio
        self.assertAlmostEqual(flow_ratio, 0.5)

    def test_last_inspection_year_has_invalid_last_inspection_date_returns_None(self):
        self.mapping_link.max_flow_cfs = 1
        self.mapping_link.design_flow_cfs = None
        flow_ratio = self.mapping_link.flow_ratio
        self.assertEqual(flow_ratio, None)