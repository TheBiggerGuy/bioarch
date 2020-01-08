#!/usr/bin/env python


from random import Random
import unittest


from .mouth import Mouth, Tooth


class ToothTest(unittest.TestCase):
    def test_construction(self):
        Tooth('A', '2', 'NA', '0', '1')

        for i in range(0, 5):
            with self.assertRaises(AssertionError):
                args = ['A', '2', 'NA', '0', '1']
                args[i] = None
                Tooth(*args)

        with self.assertRaises(ValueError):
            Tooth('Z', '2', 'NA', '0', '1')

        # if Tooth='NA' then calculus=eh=cavities='NA'
        for i in range(1, 4):
            with self.assertRaises(ValueError):
                args = ['NA', 'NA', 'NA', 'NA', '1']
                args[i] = '1'
                Tooth(*args)

    def test_eq(self):
        self.assertEqual(Tooth('A', '2', 'NA', '0', '1'), Tooth('A', '2', 'NA', '0', '1'))
        for i in range(0, 5):
            args = ['A', '2', 'NA', '1', '1']
            args[i] = '0'
            self.assertNotEqual(Tooth(*args), Tooth('A', '2', 'NA', '1', '1'))

    def test_to_pd_series(self):
        series = Tooth('A', '2', 'NA', '0', '1').to_pd_series()
        self.assertEqual(series.to_json(), '{"tooth":"A","tooth_val":2,"calculus":"2","calculus_val":2,"eh":"NA","eh_val":null,"cavities":"0","cavities_val":false,"abcess":"1","abcess_val":true}')
        series = Tooth('A', '2', 'NA', '0', '1').to_pd_series(prefix='tooth_0_')
        self.assertEqual(series.to_json(), '{"tooth_0_tooth":"A","tooth_0_tooth_val":2,"tooth_0_calculus":"2","tooth_0_calculus_val":2,"tooth_0_eh":"NA","tooth_0_eh_val":null,"tooth_0_cavities":"0","tooth_0_cavities_val":false,"tooth_0_abcess":"1","tooth_0_abcess_val":true}')

        for i, tooth in enumerate(('NA', '0', '1', 'A', 'B1', 'B2', 'C', 'D', 'E', 'F', 'G', 'H', 'I')):
            series = Tooth(tooth, 'NA', 'NA', 'NA', 'NA').to_pd_series()
            if i == 0:
                self.assertEqual(series['tooth_val'], None)
            else:
                self.assertEqual(series['tooth_val'], i - 1)


class MouthTest(unittest.TestCase):
    def test_construction(self):
        Mouth([Tooth.empty()] * 32)
        with self.assertRaises(ValueError):
            Mouth([Tooth.empty()] * 33)

    def test_to_pd_series(self):
        random = Random(666)
        series = Mouth([Tooth('A', '2', 'NA', '0', random.choice(('NA', '0', '1'))) for _ in range(0, 32)]).to_pd_series()

        self.assertRegex(series.to_json(), '^{"all_number_of_teeth":32,"all_tooth_0_tooth":"A",".*}$')
        self.assertRegex(series.to_json(), '.*"incisors_abcess_mean":0.6666666667,"incisors_abcess_max":true,"incisors_abcess_min":false,"incisors_abcess_count":6}$')
        series = Mouth.empty().to_pd_series(prefix='mouth_')
        self.assertTrue(series.to_json().startswith('{"mouth_all_number_of_teeth":0,"mouth_all_tooth_0_tooth":"NA","'))


def main():
    unittest.main()


if __name__ == "__main__":
    main()
