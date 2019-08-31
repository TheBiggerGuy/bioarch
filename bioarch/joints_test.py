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
        self.assertEqual(series.to_json(), '{"shoulder_left":{"name":"NORMAL","value":0},"shoulder_right":{"name":"NORMAL","value":0},"shoulder_avg":{"name":"NORMAL","value":0},"elbow_left":null,"elbow_right":null,"elbow_avg":null,"wrist_left":{"name":"NORMAL","value":0},"wrist_right":null,"wrist_avg":{"name":"NORMAL","value":0},"hip_left":null,"hip_right":{"name":"NORMAL","value":0},"hip_avg":{"name":"NORMAL","value":0},"knee_left":{"name":"NORMAL","value":0},"knee_right":{"name":"MEDIUM","value":2},"knee_avg":{"name":"MILD","value":1},"ankle_left":null,"ankle_right":{"name":"FRACTURE","value":6},"ankle_avg":{"name":"FRACTURE","value":6},"sacro_illiac":{"name":"NORMAL","value":0},"sacro_illiac_avg":{"name":"NORMAL","value":0},"c1_3":null,"c1_3_avg":null,"c4_7":{"name":"NORMAL","value":0},"c4_7_avg":{"name":"NORMAL","value":0},"t1_4":{"name":"NORMAL","value":0},"t1_4_avg":{"name":"NORMAL","value":0},"t5_8":{"name":"NORMAL","value":0},"t5_8_avg":{"name":"NORMAL","value":0},"t9_12":{"name":"NORMAL","value":0},"t9_12_avg":{"name":"NORMAL","value":0},"l1_5":{"name":"NORMAL","value":0},"l1_5_avg":{"name":"NORMAL","value":0},"mean":0.6363636364,"max":6,"min":0,"count":11}')

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
