#!/usr/bin/env python


import unittest


from .left_right import LeftRight


class BasicObjectForTest(object):
    def __init__(self, val1, avg, _max):
        self.val1 = val1
        self.avg = avg
        self.max = _max

    def __eq__(self, other):
        return (self.val1, self.avg, self.max) == (other.val1, other.avg, other.max)


class ObjectWithAvgForTest(object):
    def __init__(self, val):
        self.val = val

    @staticmethod
    def avg(left, right):
        return ObjectWithAvgForTest(left.val + right.val)

    def __eq__(self, other):
        return self.val == other.val


class LeftRightTest(unittest.TestCase):
    def test_construction(self):
        LeftRight(1, 2)
        LeftRight(1.0, 2.0)
        LeftRight('left', 'right')
        LeftRight({'a': 1}, {'a': 2})

        LeftRight(1, None)
        LeftRight(None, 1)
        LeftRight(None, None)

        with self.assertRaises(ValueError):
            LeftRight(1, 1.0)

    def test_avg(self):
        self.assertEqual(LeftRight(1, 1).avg(), 1)
        self.assertEqual(LeftRight(None, 1).avg(), 1)
        self.assertEqual(LeftRight(1, None).avg(), 1)

        self.assertEqual(LeftRight(1, 3).avg(), 2)
        self.assertEqual(LeftRight(1, 2).avg(), 1)

        self.assertEqual(LeftRight(1.0, 3.0).avg(), 2.0)
        self.assertEqual(LeftRight(1.0, 2.0).avg(), 1.5)

        left = BasicObjectForTest(1, 2, 3)
        right = BasicObjectForTest(1, 2, 3)
        self.assertEqual(LeftRight(left, right).avg(), BasicObjectForTest(1, 2, 3))
        same_object = BasicObjectForTest(1, 2, 3)
        left = BasicObjectForTest(1.0, 1, same_object)
        right = BasicObjectForTest(2.0, 3, same_object)
        self.assertEqual(LeftRight(left, right).avg(), BasicObjectForTest(1.5, 2, same_object))

        left = ObjectWithAvgForTest(1)
        right = ObjectWithAvgForTest(2)
        self.assertEqual(LeftRight(left, right).avg(), ObjectWithAvgForTest(3))

    def test_equality(self):
        lr = LeftRight(1, 1)
        self.assertEqual(lr, lr)
        self.assertEqual(LeftRight(1, 1), LeftRight(1, 1))

        self.assertNotEqual(LeftRight(1, 1), LeftRight(1, 2))
        self.assertNotEqual(LeftRight(1, 1), LeftRight(2, 1))
        self.assertNotEqual(LeftRight(1, 1), LeftRight(2, 2))
        self.assertNotEqual(LeftRight(1, 1), None)

        with self.assertRaises(NotImplementedError):
            LeftRight(1, 1).__eq__('test')


def main():
    unittest.main()


if __name__ == "__main__":
    main()
