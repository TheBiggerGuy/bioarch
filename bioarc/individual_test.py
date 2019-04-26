#!/usr/bin/env python


import unittest


from .individual import AgeSexStature, BurialInfo, Individual, LongBoneMeasurement
from .left_right import LeftRight
from .mouth import Mouth
from .occupational_markers import OccupationalMarkers


class LongBoneMeasurementTest(unittest.TestCase):
    def test_lr_avg(self):
        left_femur = LongBoneMeasurement(1.0, None, 1.0, None)
        right_femur = LongBoneMeasurement(2.0, 2.0, None, None)

        femur = LeftRight(left_femur, right_femur)
        avg_femur = femur.avg()
        self.assertEqual(avg_femur.max, 1.5)
        self.assertEqual(avg_femur.bi, 2.0)
        self.assertEqual(avg_femur.head, 1.0)
        self.assertEqual(avg_femur.distal, None)

        femur = LeftRight(LongBoneMeasurement.empty(), right_femur)
        avg_femur = femur.avg()
        self.assertEqual(avg_femur, right_femur)

        femur = LeftRight(left_femur, LongBoneMeasurement.empty())
        avg_femur = femur.avg()
        self.assertEqual(avg_femur, left_femur)

        femur = LeftRight(LongBoneMeasurement.empty(), LongBoneMeasurement.empty())
        avg_femur = femur.avg()
        self.assertEqual(avg_femur, LongBoneMeasurement.empty())


class IndividualTest(unittest.TestCase):
    def test_basic(self):
        burial_info = BurialInfo('site_name', 'site_id')
        age_sex_sature = AgeSexStature.empty()
        mouth = Mouth.empty()
        occupational_markers = OccupationalMarkers.empty()

        individual = Individual('id_1', burial_info, age_sex_sature, mouth, occupational_markers)

        self.assertEqual(individual.id, 'id_1')

    def test_to_pd_series(self):
        burial_info = BurialInfo('site_name', 'site_id')
        age_sex_sature = AgeSexStature.empty()
        mouth = Mouth.empty()
        occupational_markers = OccupationalMarkers.empty()

        individual = Individual('id_1', burial_info, age_sex_sature, mouth, occupational_markers)
        individual.to_pd_series()


def main():
    unittest.main()


if __name__ == "__main__":
    main()
