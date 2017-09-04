import unittest
from factor import Factor, unionize_factors, sum_out


class TestFactor(unittest.TestCase):
    def setUp(self):
        self.f_a = Factor(['B', 'A'], [0.8, 0.2, 0.1, 0.9])
        self.f_b = Factor(['C', 'B'], [0.7, 0.3, 0.5, 0.5])
        self.f_c = Factor(['C', 'B', 'A'], [0.56, 0.4, 0.14, 0.1, 0.03, 0.05, 0.27, 0.45])

    def testUnionize(self):
        self.assertListAlmostEqual(unionize_factors('B', [self.f_a, self.f_b]).get_cpt(),
                                   [0.56, 0.4, 0.14, 0.1, 0.03, 0.05, 0.27, 0.45])

    def testSumOut(self):
        self.assertListAlmostEqual(sum_out('B', self.f_c).get_cpt(),
                                   [0.59, 0.45, 0.41, 0.55])

    def assertListAlmostEqual(self, list1, list2, places=0):
        """
        Rounds the numbers of two lists to *places* decimal places to see
        if the lists are almost equal.
        :param list1: list of numbers
        :param list2: list of numbers
        :param places: number of decimal places to consider
        :return: True, if all numbers in the lists are equal to *places* decimal places. Else False.
        """
        self.assertEqual(len(list1), len(list2))
        for a, b in zip(list1, list2):
            self.assertAlmostEqual(a, b, places)
