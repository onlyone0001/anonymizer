from unittest import TestCase

from src.analyze.analyzer_result import AnalyzerResult
from src.analyze.regex import RegEx
from src.analyze.base_detector import BaseDetector

class TestBaseDetector(TestCase):

    def setUp(self):

        class TestClass(BaseDetector):
            def get_pattern(self):
                return RegEx().one_of("STFG").any_digit().num_occurrences(7).range("A", "Z").build()

            def get_name(self):
                return "NRIC"

        self.test_class = TestClass()

    def test_execute_calls_match_and_validate(self):
        results = self.test_class.execute("First President of Singapore NRIC was S0000001I")
        self.assertEqual(len(results), 1)
        self.assertEqual(AnalyzerResult("S0000001I", "NRIC", 38, 47), results[0])

    def test_execute_returns_all_matches_when_more_than_one(self):
        results = self.test_class.execute("First President of Singapore NRIC was S0000001I and the second president's was T0000001R")
        self.assertEqual(len(results), 2)
        self.assertCountEqual([AnalyzerResult("S0000001I", "NRIC", 38, 47),AnalyzerResult("T0000001R", "NRIC", 79, 88)], results)

    def test_execute_returns_empty_list_when_no_matches(self):
        results = self.test_class.execute("First President of Singapore NRIC was ABC and the second president's was DEF")
        self.assertEqual(len(results), 0)