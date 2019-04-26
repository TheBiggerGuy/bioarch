#!/usr/bin/env python


import unittest


from .age import AgeCategory, EstimatedAge


class AgeCategoryTest(unittest.TestCase):
    def test_order(self):
        self.assertEqual(sorted([AgeCategory.OLD, AgeCategory.YOUNG]), [AgeCategory.YOUNG, AgeCategory.OLD])
        # None is sorted first
        self.assertEqual(sorted([AgeCategory.OLD, AgeCategory.YOUNG, None]), [None, AgeCategory.YOUNG, AgeCategory.OLD])
        # Numbers are sorted as if they where AgeCategory.value
        self.assertEqual(sorted([0, 3, AgeCategory.YOUNG]), [0, AgeCategory.YOUNG, 3])
        # Invalid numbers fail
        with self.assertRaises(ValueError):
            [AgeCategory.OLD, -1].sort()

    def test_parse(self):
        self.assertEqual(AgeCategory.parse('UNKNOWN'), AgeCategory.UNKNOWN)
        self.assertEqual(AgeCategory.parse('YOUNG'), AgeCategory.YOUNG)
        self.assertEqual(AgeCategory.parse('YOUNG_ADULT'), AgeCategory.YOUNG_ADULT)
        self.assertEqual(AgeCategory.parse('YOUNG ADULT'), AgeCategory.YOUNG_ADULT)
        self.assertEqual(AgeCategory.parse('ADULT'), AgeCategory.ADULT)
        self.assertEqual(AgeCategory.parse('MIDDLE'), AgeCategory.MIDDLE)
        self.assertEqual(AgeCategory.parse('MIDDLE_OLD'), AgeCategory.MIDDLE_OLD)
        self.assertEqual(AgeCategory.parse('MIDDLE/OLD'), AgeCategory.MIDDLE_OLD)
        self.assertEqual(AgeCategory.parse('OLD'), AgeCategory.OLD)
        self.assertEqual(AgeCategory.parse('OA'), AgeCategory.OLD)

        self.assertEqual(AgeCategory.parse('UNKNOWN'), AgeCategory.parse('unknown'))
        self.assertEqual(AgeCategory.parse(None), None)
        self.assertEqual(AgeCategory.parse(AgeCategory.UNKNOWN), AgeCategory.UNKNOWN)


class EstimatedAgeTest(unittest.TestCase):
    def test_costructor(self):
        self.assertEqual(EstimatedAge('UNKNOWN', 'UNKNOWN').category, AgeCategory.UNKNOWN)
        self.assertEqual(EstimatedAge('OLD', 'UNKNOWN').category, AgeCategory.OLD)

        with self.assertRaises(ValueError):
            EstimatedAge('NA_AN_AGE', 'UNKNOWN')

        self.assertEqual(EstimatedAge('OLD', '10-20').ranged, range(10, 20))
        self.assertEqual(EstimatedAge('OLD', '20+').ranged, range(20, 100))
        self.assertEqual(EstimatedAge('OLD', '=20').ranged, range(20, 21))
        self.assertEqual(EstimatedAge('OLD', 'UNKNOWN').ranged, None)
        self.assertEqual(EstimatedAge('OLD', '?').ranged, None)

    def test_to_pd_series(self):
        series = EstimatedAge('UNKNOWN', 'UNKNOWN').to_pd_series()
        self.assertEqual(series.to_json(), '{"category":"UNKNOWN","category_val":0,"ranged_val":null}')

        series = EstimatedAge('OLD', '45-60').to_pd_series()
        self.assertEqual(series.to_json(), '{"category":"OLD","category_val":6,"ranged_val":[45,46,47,48,49,50,51,52,53,54,55,56,57,58,59]}')


def main():
    unittest.main()


if __name__ == "__main__":
    main()
