import unittest
from factor import Factor
from ve_algorithm import VElimination

class testVElimination(unittest.TestCase):
    def setUp(self):
        self.f_a = Factor(['A'], [0.6, 0.4])
        self.f_b = Factor(['A', 'B'], [0.8, 0.2, 0.1, 0.9])
        self.f_c = Factor(['B', 'C'], [0.7, 0.3, 0.5, 0.5])

        self.f_tampering = Factor(['Ta'], [0.02, 0.98])
        self.f_fire = Factor(['Fi'], [0.01, 0.99])
        self.f_smoke = Factor(['Fi', 'Sm'], [0.9, 0.1, 0.01, 0.99])
        self.f_alarm = Factor(['Fi', 'Ta', 'Al'], [0.5, 0.5, 0.99, 0.01, 0.85, 0.15, 0.0001, 0.9999])
        self.f_leaving = Factor(['Al', 'Le'], [0.88, 0.12, 0.001, 0.999])
        self.f_report = Factor(['Le', 'Re'], [0.75, 0.25, 0.01, 0.99])

    def testNoObservations(self):
        ve = VElimination(variables=['A', 'B', 'C'], factors=[self.f_a, self.f_b, self.f_c], query='A', obs={})
        self.assertDictAlmostEqual(ve.execute(),
                                   {False: 0.4, True: 0.6})

        ve = VElimination(variables=['A', 'B', 'C'], factors=[self.f_a, self.f_b, self.f_c], query='C', obs={})
        self.assertDictAlmostEqual(ve.execute(),
                                   {False: 0.396, True: 0.604})

    def testWithObservations(self):
        ve = VElimination(variables=['A', 'B', 'C'],
                          factors=[self.f_a, self.f_b, self.f_c],
                          query='A', obs={'C': True})
        self.assertDictAlmostEqual(ve.execute(),
                                   {False: 0.34437086092715236, True: 0.6556291390728476})

        ve = VElimination(variables=['A', 'B', 'C'],
                          factors=[self.f_a, self.f_b, self.f_c],
                          query='B',
                          obs={'A': True, 'C': False})
        self.assertDictAlmostEqual(ve.execute(),
                                   {False: 0.2941176470588236, True: 0.7058823529411765})

    def testMultipleDependencies(self):
        ve = VElimination(variables=['Al', 'Fi', 'Le', 'Re', 'Sm', 'Ta'],
                          factors=[self.f_tampering, self.f_fire, self.f_smoke,
                                   self.f_alarm, self.f_leaving, self.f_report],
                          query='Ta',
                          obs={'Re': True, 'Sm': False})
        self.assertDictAlmostEqual(ve.execute(),
                                   {False: 0.49920299092147685, True: 0.5007970090785231})

    def assertDictAlmostEqual(self, dict1, dict2, places=0):
        """
        Rounds the numbers of two lists to *places* decimal places to see
        if the lists are almost equal.
        :param dict1: list of numbers
        :param dict2: list of numbers
        :param places: number of decimal places to consider
        :return: True, if all numbers in the lists are equal to *places* decimal places. Else False.
        """
        self.assertEqual(len(dict1), len(dict2))
        for a, b in zip(iter(dict1.values()), iter(dict2.values())):
            self.assertAlmostEqual(a, b, places)