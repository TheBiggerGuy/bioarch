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

    def test_to_quad(self):
        self.assertEqual(AgeCategory.UNKNOWN.as_quad(), AgeCategory.UNKNOWN)
        self.assertEqual(AgeCategory.YOUNG.as_quad(), AgeCategory.YOUNG)
        self.assertEqual(AgeCategory.YOUNG_ADULT.as_quad(), AgeCategory.YOUNG)
        self.assertEqual(AgeCategory.ADULT.as_quad(), AgeCategory.ADULT)
        self.assertEqual(AgeCategory.MIDDLE.as_quad(), AgeCategory.MIDDLE)
        self.assertEqual(AgeCategory.MIDDLE_OLD.as_quad(), AgeCategory.MIDDLE)
        self.assertEqual(AgeCategory.OLD.as_quad(), AgeCategory.OLD)


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
        self.assertEqual(EstimatedAge('OLD', None).ranged, None)

    def test_to_pd_data_frame(self):
        df = EstimatedAge('UNKNOWN', 'UNKNOWN').to_pd_data_frame('id1')
        self.assertEqual(df.to_json(orient='records'), '[{"category_cat":"UNKNOWN","category_val":0,"category_quad_cat":"UNKNOWN","category_quad_val":0}]')

        df = EstimatedAge('OLD', '45-60').to_pd_data_frame('id1')
        self.assertEqual(df.to_json(orient='records'), '[{"category_cat":"OLD","category_val":5,"category_quad_cat":"OLD","category_quad_val":5,"ranged":[45,46,47,48,49,50,51,52,53,54,55,56,57,58,59]}]')


def main():
    unittest.main()


if __name__ == "__main__":
    main()
