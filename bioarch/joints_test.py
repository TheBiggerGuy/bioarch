#!/usr/bin/env python


from importlib.resources import open_binary
import json
import unittest


from . import test as bioarch_test
from .joints import JointCondition, Joints
from .left_right import LeftRight


class JointConditionTest(unittest.TestCase):
    def test_parse(self):
        self.assertEqual(JointCondition.parse(None), None)
        self.assertEqual(JointCondition.parse('NA'), None)
        self.assertEqual(JointCondition.parse('N'), None)
        self.assertEqual(JointCondition.parse('1'), JointCondition.MILD)
        self.assertEqual(JointCondition.parse('MILD'), JointCondition.MILD)

        self.assertEqual(JointCondition.parse('0'), JointCondition.NORMAL)
        self.assertEqual(JointCondition.parse('1'), JointCondition.MILD)
        self.assertEqual(JointCondition.parse('2'), JointCondition.MEDIUM)
        self.assertEqual(JointCondition.parse('3'), JointCondition.EXTREAM)
        self.assertEqual(JointCondition.parse('4'), JointCondition.FUSED)
        self.assertEqual(JointCondition.parse('5'), JointCondition.SCHMORALS_NODES)
        self.assertEqual(JointCondition.parse('6'), JointCondition.FRACTURE)

        self.assertEqual(JointCondition.parse(0), JointCondition.NORMAL)

        with self.assertRaises(ValueError):
            JointCondition.parse('')

    def test_avg(self):
        va1 = None
        va2 = JointCondition.MILD
        self.assertEqual(JointCondition.avg(va1, va2), JointCondition.MILD)
        self.assertEqual(JointCondition.avg(va2, va1), JointCondition.MILD)

        va1 = None
        va2 = None
        self.assertEqual(JointCondition.avg(va1, va2), None)
        self.assertEqual(JointCondition.avg(va2, va1), None)

        va1 = JointCondition.MILD
        va2 = JointCondition.EXTREAM
        self.assertEqual(JointCondition.avg(va1, va2), JointCondition.MEDIUM)
        self.assertEqual(JointCondition.avg(va2, va1), JointCondition.MEDIUM)

    def test_order(self):
        self.assertEqual(sorted([JointCondition.FRACTURE, JointCondition.NORMAL]), [JointCondition.NORMAL, JointCondition.FRACTURE])
        # None is sorted first
        self.assertEqual(sorted([JointCondition.FRACTURE, JointCondition.NORMAL, None]), [None, JointCondition.NORMAL, JointCondition.FRACTURE])
        # Numbers are sorted as if they where JointCondition.value
        self.assertEqual(sorted([0, 3, JointCondition.MILD]), [0, JointCondition.MILD, 3])
        # Invalid numbers fail
        with self.assertRaises(ValueError):
            [JointCondition.MILD, -2].sort()


class JointsTest(unittest.TestCase):
    def test_to_pd_data_frame(self):
        shoulder = LeftRight(JointCondition.NORMAL, JointCondition.NORMAL)
        elbow = LeftRight(None, None)
        wrist = LeftRight(JointCondition.NORMAL, None)
        hip = LeftRight(None, JointCondition.NORMAL)
        knee = LeftRight(JointCondition.NORMAL, JointCondition.MEDIUM)
        ankle = LeftRight(None, JointCondition.FRACTURE)

        sacro_illiac = JointCondition.NORMAL
        c1_3 = None
        c4_7 = JointCondition.EXTREAM
        t1_4 = JointCondition.NORMAL
        t5_8 = None
        t9_12 = JointCondition.FRACTURE
        l1_5 = JointCondition.NORMAL

        df = Joints(shoulder, elbow, wrist, hip, knee, ankle, sacro_illiac, c1_3, c4_7, t1_4, t5_8, t9_12, l1_5).to_pd_data_frame('id1')

        with open_binary(bioarch_test, 'JointsTest.test_to_pd_data_frame.json') as json_stream:
            expected_json = json.load(json_stream)

        print(df.to_json(orient='records'))
        actual_json = json.loads(df.to_json(orient='records'))

        self.assertEqual(actual_json, expected_json)

    # https://github.com/TheBiggerGuy/bioarch/issues/21
    def test_to_pd_data_frame_joints_thoracic_max(self):
        shoulder = LeftRight(JointCondition.NORMAL, JointCondition.NORMAL)
        elbow = LeftRight(None, None)
        wrist = LeftRight(JointCondition.NORMAL, None)
        hip = LeftRight(None, JointCondition.NORMAL)
        knee = LeftRight(JointCondition.NORMAL, JointCondition.MEDIUM)
        ankle = LeftRight(None, JointCondition.FRACTURE)

        sacro_illiac = JointCondition.NORMAL
        c1_3 = None
        c4_7 = JointCondition.EXTREAM

        t1_4 = JointCondition.NORMAL
        t5_8 = None
        t9_12 = JointCondition.FRACTURE

        l1_5 = JointCondition.NORMAL

        df = Joints(shoulder, elbow, wrist, hip, knee, ankle, sacro_illiac, c1_3, c4_7, t1_4, t5_8, t9_12, l1_5).to_pd_data_frame('id1')

        thoracic_min = df['thoracic_min']
        thoracic_max = df['thoracic_max']

        self.assertEqual(thoracic_min.to_json(orient='records'), '["NORMAL"]')
        self.assertEqual(thoracic_max.to_json(orient='records'), '["FRACTURE"]')


def main():
    unittest.main()


if __name__ == "__main__":
    main()
