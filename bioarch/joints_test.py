#!/usr/bin/env python


import unittest


from .joints import is_none_or_na, JointCondition, Joints
from .left_right import LeftRight


class JointConditionTest(unittest.TestCase):
    def test_parse(self):
        self.assertEqual(JointCondition.parse(None), None)
        self.assertEqual(JointCondition.parse('NA'), JointCondition.NOT_PRESENT)
        self.assertEqual(JointCondition.parse('N'), JointCondition.NOT_PRESENT)
        self.assertEqual(JointCondition.parse('NOT_PRESENT'), JointCondition.NOT_PRESENT)
        self.assertEqual(JointCondition.parse('1'), JointCondition.MILD)
        self.assertEqual(JointCondition.parse('MILD'), JointCondition.MILD)

        self.assertEqual(JointCondition.parse('-1'), JointCondition.NOT_PRESENT)
        self.assertEqual(JointCondition.parse('0'), JointCondition.NORMAL)
        self.assertEqual(JointCondition.parse('1'), JointCondition.MILD)
        self.assertEqual(JointCondition.parse('2'), JointCondition.MEDIUM)
        self.assertEqual(JointCondition.parse('3'), JointCondition.EXTREAM)
        self.assertEqual(JointCondition.parse('4'), JointCondition.FUSED)
        self.assertEqual(JointCondition.parse('5'), JointCondition.SCHMORALS_NODES)
        self.assertEqual(JointCondition.parse('6'), JointCondition.FRACTURE)

        self.assertEqual(JointCondition.parse(-1), JointCondition.NOT_PRESENT)
        self.assertEqual(JointCondition.parse(0), JointCondition.NORMAL)

        with self.assertRaises(ValueError):
            JointCondition.parse('')

    def test_avg(self):
        va1 = JointCondition.NOT_PRESENT
        va2 = JointCondition.MILD
        self.assertEqual(JointCondition.avg(va1, va2), JointCondition.MILD)
        self.assertEqual(JointCondition.avg(va2, va1), JointCondition.MILD)

        va1 = None
        va2 = JointCondition.MILD
        self.assertEqual(JointCondition.avg(va1, va2), JointCondition.MILD)
        self.assertEqual(JointCondition.avg(va2, va1), JointCondition.MILD)

        va1 = None
        va2 = None
        self.assertEqual(JointCondition.avg(va1, va2), None)

        va1 = JointCondition.MILD
        va2 = JointCondition.EXTREAM
        self.assertEqual(JointCondition.avg(va1, va2), JointCondition.MEDIUM)
        self.assertEqual(JointCondition.avg(va2, va1), JointCondition.MEDIUM)

    def test_order(self):
        self.assertEqual(sorted([JointCondition.FRACTURE, JointCondition.NORMAL]), [JointCondition.NORMAL, JointCondition.FRACTURE])
        # None is sorted first
        self.assertEqual(sorted([JointCondition.FRACTURE, JointCondition.NORMAL, None]), [None, JointCondition.NORMAL, JointCondition.FRACTURE])
        # +-inf is sorted first/last
        self.assertEqual(sorted([float('inf'), JointCondition.FRACTURE, JointCondition.NORMAL, float('-inf')]), [float('-inf'), JointCondition.NORMAL, JointCondition.FRACTURE, float('inf')])
        # Numbers are sorted as if they where JointCondition.value
        self.assertEqual(sorted([0, 3, JointCondition.MILD]), [0, JointCondition.MILD, 3])
        # Invalid numbers fail
        with self.assertRaises(ValueError):
            [JointCondition.MILD, -2].sort()


class JointsTest(unittest.TestCase):
    def test_to_pd_series(self):
        shoulder = LeftRight(JointCondition.NORMAL, JointCondition.NORMAL)
        elbow = LeftRight(JointCondition.NOT_PRESENT, JointCondition.NOT_PRESENT)
        wrist = LeftRight(JointCondition.NORMAL, JointCondition.NOT_PRESENT)
        hip = LeftRight(JointCondition.NOT_PRESENT, JointCondition.NORMAL)
        knee = LeftRight(JointCondition.NORMAL, JointCondition.MEDIUM)
        ankle = LeftRight(None, JointCondition.FRACTURE)

        sacro_illiac = JointCondition.NORMAL
        c1_3 = JointCondition.NOT_PRESENT
        c4_7 = JointCondition.NORMAL
        t1_4 = JointCondition.NORMAL
        t5_8 = JointCondition.NORMAL
        t9_12 = JointCondition.NORMAL
        l1_5 = JointCondition.NORMAL

        joints = Joints(shoulder, elbow, wrist, hip, knee, ankle, sacro_illiac, c1_3, c4_7, t1_4, t5_8, t9_12, l1_5)

        series = joints.to_pd_series()
        self.assertEqual(series.to_json(), '{"shoulder_left":"NORMAL","shoulder_right":"NORMAL","shoulder_avg":"NORMAL","elbow_left":null,"elbow_right":null,"elbow_avg":null,"wrist_left":"NORMAL","wrist_right":null,"wrist_avg":"NORMAL","hip_left":null,"hip_right":"NORMAL","hip_avg":"NORMAL","knee_left":"NORMAL","knee_right":"MEDIUM","knee_avg":"MILD","ankle_left":null,"ankle_right":"FRACTURE","ankle_avg":"FRACTURE","sacro_illiac":"NORMAL","sacro_illiac_avg":"NORMAL","c1_3":null,"c1_3_avg":null,"c4_7":"NORMAL","c4_7_avg":"NORMAL","t1_4":"NORMAL","t1_4_avg":"NORMAL","t5_8":"NORMAL","t5_8_avg":"NORMAL","t9_12":"NORMAL","t9_12_avg":"NORMAL","l1_5":"NORMAL","l1_5_avg":"NORMAL","mean":0.6363636364,"max":6,"min":0,"count":11}')

    def test_is_none_or_na(self):
        self.assertEqual(is_none_or_na(None), True)

        self.assertEqual(is_none_or_na(JointCondition.NOT_PRESENT), True)
        self.assertEqual(is_none_or_na(JointCondition.NORMAL), False)

        self.assertEqual(is_none_or_na(LeftRight(JointCondition.NOT_PRESENT, JointCondition.NOT_PRESENT)), True)
        self.assertEqual(is_none_or_na(LeftRight(JointCondition.NOT_PRESENT, JointCondition.NORMAL)), False)
        self.assertEqual(is_none_or_na(LeftRight(JointCondition.NORMAL, JointCondition.NOT_PRESENT)), False)
        self.assertEqual(is_none_or_na(LeftRight(JointCondition.NORMAL, JointCondition.NORMAL)), False)


def main():
    unittest.main()


if __name__ == "__main__":
    main()
