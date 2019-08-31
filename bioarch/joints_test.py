#!/usr/bin/env python


import unittest


from .joints import JointCondition


class JointConditionTest(unittest.TestCase):
    def test_parse(self):
        self.assertEqual(JointCondition.parse(None), None)
        self.assertEqual(JointCondition.parse('NA'), JointCondition.NOT_PRESENT)
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


def main():
    unittest.main()


if __name__ == "__main__":
    main()
