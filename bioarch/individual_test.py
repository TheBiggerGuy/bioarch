#!/usr/bin/env python


from importlib.resources import open_binary
import json
import unittest


from . import test as bioarch_test
from .age import EstimatedAge
from .context import Context
from .individual import AgeSexStature, BurialInfo, Individual, LongBoneMeasurement, OsteologicalSex
from .joints import Joints
from .left_right import LeftRight
from .mouth import Mouth
from .occupational_markers import OccupationalMarkers
from .sex import Sex
from .trauma import Trauma


class OsteologicalSexTest(unittest.TestCase):
    def test_to_pd_series(self):
        pelvic = Sex.MALE
        cranium = None
        combined = Sex.MALE_ASSUMED
        os = OsteologicalSex(pelvic, cranium, combined)

        df = os.to_pd_data_frame('id1')

        self.assertEqual(df.to_json(orient='records'), '[{"pelvic_cat":"MALE","pelvic_val":100,"pelvic_bin_cat":"MALE","pelvic_bin_val":100,"combined_cat":"MALE_ASSUMED","combined_val":80,"combined_bin_cat":"MALE","combined_bin_val":100}]')


class AgeSexStatureTest(unittest.TestCase):
    def test_to_pd_series(self):
        os = OsteologicalSex(Sex.MALE, None, Sex.MALE_ASSUMED)
        age = EstimatedAge.empty()
        femur = LongBoneMeasurement.empty_lr()
        humerus = LongBoneMeasurement.empty_lr()
        tibia = LongBoneMeasurement.empty_lr()
        stature = ''
        body_mass = 'None'

        ass = AgeSexStature(os, age, femur, humerus, tibia, stature, body_mass)

        df = ass.to_pd_data_frame('id1', prefix='ass_')

        with open_binary(bioarch_test, 'AgeSexStatureTest.test_to_pd_series.json') as json_stream:
            expected_json = json.load(json_stream)

        actual_json = json.loads(df.to_json(orient='records'))

        self.assertEqual(expected_json, actual_json)


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
        joints = Joints.empty()
        trauma = Trauma.empty()
        context = Context.empty()

        individual = Individual('id_1', burial_info, age_sex_sature, mouth, occupational_markers, joints, trauma, context)

        self.assertEqual(individual.id, 'id_1')

    def test_to_pd_data_frame(self):
        burial_info = BurialInfo('site_name', 'site_id')
        age_sex_sature = AgeSexStature.empty()
        mouth = Mouth.empty()
        occupational_markers = OccupationalMarkers.empty()
        joints = Joints.empty()
        trauma = Trauma.empty()
        context = Context({'spear': True, 'pot': False})

        individual = Individual('id_1', burial_info, age_sex_sature, mouth, occupational_markers, joints, trauma, context)
        df = individual.to_pd_data_frame()

        with open_binary(bioarch_test, 'IndividualTest.test_to_pd_data_frame.json') as json_stream:
            expected_json = json.load(json_stream)

        actual_json = json.loads(df.to_json(orient='records'))

        self.assertEqual(actual_json, expected_json)


def main():
    unittest.main()


if __name__ == "__main__":
    main()
