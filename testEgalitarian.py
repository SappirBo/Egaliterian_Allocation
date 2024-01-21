
#!python3

"""
Author: Sappir Bohbot
Date: 21/01/2024

Task 3 from Economic algorithms course, Based on Erel Segal-Halevi Work, 
link to Course:https://github.com/erelsgl-at-ariel/algorithms-5784
link to code:https://github.com/erelsgl-at-ariel/algorithms-5784/blob/main/02-pareto-efficiency/code/3-leximin-sums.py
"""
import unittest
from egalitarianEllocation import egaliterian_allocation

eps = 0.0001

class TestSolveFunction(unittest.TestCase):
    
    def test_from_task(self):
        print("\n- - - - - - - Run: test_from_task - - - - - - -")
        valuations_from_task = [[11,11,22,33,44],
                       [11,22,44,55,66],
                       [11,33,22,11,66]]
        result = egaliterian_allocation(valuations_from_task)
        self.assertIsNotNone(result)
        self._check_resource_allocation(result)

    def test_equal_valuations(self):
        print("\n- - - - - - - Run: test_equal_valuations - - - - - - -")
        valuations_equal = [[10, 10, 10, 10, 10],
                            [10, 10, 10, 10, 10],
                            [10, 10, 10, 10, 10]]
        result = egaliterian_allocation(valuations_equal)
        self.assertIsNotNone(result)
        self._check_resource_allocation(result)

    def test_skewed_valuations(self):
        print("\n - - - - - - - Run: test_skewed_valuations - - - - - - -")
        valuations_skewed = [[90, 5, 5, 0, 0],
                             [0, 0, 90, 10, 0],
                             [10, 95, 0, 0, 95]]
        result = egaliterian_allocation(valuations_skewed)
        self.assertIsNotNone(result)
        self._check_resource_allocation(result)

    def _check_resource_allocation(self, result):
        for resource in range(5):
            sum_for_resource = 0
            for player_allocation in range(3):
                sum_for_resource += 100.0 * result[resource][player_allocation].value
            grater_equal_to_99 = sum_for_resource <= 100.0 + eps
            lesser_equal_to_100 = sum_for_resource >= 100.0 - eps 
            self.assertTrue(grater_equal_to_99)
            self.assertTrue(lesser_equal_to_100)

if __name__ == '__main__':
    unittest.main()