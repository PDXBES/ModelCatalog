from unittest import TestCase
from pipe import Pipe
import mock


class TestPipe(TestCase):
    def setUp(self):
        self.pipe = Pipe()

    def test_calculate_apw_recommended_action_is_spot(self):
        self.pipe.asmrecommendedaction = "SP"
        self.pipe.apwspot = 1.11
        self.pipe.calculate_apw()
        self.assertAlmostEquals(self.pipe.apw, 1.11, 2)

    def test_calculate_apw_recommended_action_is_cipp(self):
        self.pipe.asmrecommendedaction = "CIPP"
        self.pipe.apwliner = 2.22
        self.pipe.calculate_apw()
        self.assertAlmostEquals(self.pipe.apw, 2.22, 2)

    def test_calculate_apw_recommended_action_is_oc(self):
        self.pipe.asmrecommendedaction = "OC"
        self.pipe.apwwhole = 3.33
        self.pipe.calculate_apw()
        self.assertAlmostEquals(self.pipe.apw, 3.33, 2)

    def test_calculate_apw_recommended_is_not_case_sensitive(self):
        self.pipe.asmrecommendedaction = "oc"
        self.pipe.apwwhole = 3.33
        self.pipe.calculate_apw()
        self.assertAlmostEquals(self.pipe.apw, 3.33, 2)

    def test_calculate_capital_cost_calculates_correctly(self):
        self.pipe.asmrecommendednbcr = 1.11
        self.pipe.apw = 2.22
        self.pipe.bpw = 3.33
        self.pipe.calculate_capital_cost()
        self.assertAlmostEquals(self.pipe.capitalcost, 1, 2)

    def test_is_greater_than_zero_if_input_value_is_not_a_positive_number_return_false(self):
        self.pipe.apw = - 0.1
        self.assertEquals(self.pipe._is_greater_than_zero(self.pipe.apw), False)

    def test_is_greater_than_zero_if_input_value_is_a_positive_number_return_true(self):
        self.pipe.apw = 0.1
        self.assertEquals(self.pipe._is_greater_than_zero(self.pipe.apw), True)

    def test_is_greater_than_zero_if_input_value_is_not_a_number_return_false(self):
        self.pipe.apw = "nan"
        self.assertEquals(self.pipe._is_greater_than_zero(self.pipe.apw), False)

    def test_valid_if_apw_bpw_or_capital_cost_are_not_positive_number_returns_false(self):
        self.pipe.apw = -0.01
        self.pipe.bpw = 0.1
        self.pipe.capitalcost = 0.1
        self.assertEquals(self.pipe.valid(), False)
        self.pipe.apw = 0.01
        self.pipe.bpw = -0.1
        self.pipe.capitalcost = 0.1
        self.assertEquals(self.pipe.valid(), False)
        self.pipe.apw = 0.01
        self.pipe.bpw = 0.1
        self.pipe.capitalcost = -0.1
        self.assertEquals(self.pipe.valid(), False)

    def test_valid_if_apw_bpw_and_capital_cost_are_positive_numbers_returns_true(self):
        self.pipe.apw = 0.01
        self.pipe.bpw = 0.1
        self.pipe.capitalcost = 0.1
        self.pipe.asmrecommendedaction = "oc"
        self.pipe.asmrecommendednbcr = 1.11
        self.pipe.apwwhole = 3.33
        self.assertEquals(self.pipe.valid(), True)


    def test_calculate_capital_cost_if_apw_not_greater_than_zero_capital_cost_is_none(self):
        self.pipe.apw = 0
        self.pipe.bpw = 1
        self.pipe.asmrecommendednbcr = 2
        self.pipe.calculate_capital_cost()
        self.assertEquals(self.pipe.capitalcost, None)

    def test_calculate_capital_cost_if_apw_and_asmrecommendednbcr_is_greater_than_zero_capital_cost_is_calculated(self):
        self.pipe.apw = .1
        self.pipe.bpw = 1
        self.pipe.asmrecommendednbcr = 2
        self.pipe.calculate_capital_cost()
        self.assertAlmostEquals(self.pipe.capitalcost, .45)

    def test_calculate_capital_cost_if_asmrecommendednbcr_not_greater_than_zero_capital_cost_is_none(self):
        self.pipe.apw = 2
        self.pipe.bpw = 1
        self.pipe.asmrecommendednbcr = 0
        self.pipe.calculate_capital_cost()
        self.assertEquals(self.pipe.capitalcost, None)

