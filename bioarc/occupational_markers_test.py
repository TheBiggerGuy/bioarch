#!/usr/bin/env python


import unittest


from .occupational_markers import EnthesialMarker


class EnthesialMarkerTest(unittest.TestCase):
    def test_parse(self):
        self.assertEqual(EnthesialMarker.parse(None), None)
        self.assertEqual(EnthesialMarker.parse(0), EnthesialMarker(0))
        self.assertEqual(EnthesialMarker.parse('.5'), EnthesialMarker(0.5))
        self.assertEqual(EnthesialMarker.parse('r.5'), EnthesialMarker(0.5))
        self.assertEqual(EnthesialMarker.parse('S.5'), EnthesialMarker(0.5, is_s=True))
        self.assertEqual(EnthesialMarker.parse('OE3'), EnthesialMarker(3, is_oe=True))

        with self.assertRaises(ValueError):
            EnthesialMarker.parse('')

    def test_construction(self):
        EnthesialMarker(0)
        with self.assertRaises(ValueError):
            EnthesialMarker(-1)
        with self.assertRaises(ValueError):
            EnthesialMarker(4)
        with self.assertRaises(ValueError):
            EnthesialMarker(0.1)
        with self.assertRaises(ValueError):
            EnthesialMarker(0.5, is_s=True, is_oe=True)
        with self.assertRaises(ValueError):
            EnthesialMarker(0, is_s=True)
        with self.assertRaises(ValueError):
            EnthesialMarker(0, is_oe=True)

    def test_equality(self):
        self.assertEqual(EnthesialMarker.parse('S.5'), EnthesialMarker.parse('S.5'))

        self.assertNotEqual(EnthesialMarker.parse('S.5'), EnthesialMarker.parse('.5'))
        self.assertNotEqual(EnthesialMarker.parse('S.5'), None)
        self.assertNotEqual(None, EnthesialMarker.parse('S.5'))

        with self.assertRaises(NotImplementedError):
            EnthesialMarker.parse('S.5').__eq__('hello')

    def test_avg(self):
        va1 = EnthesialMarker.parse('S.5')
        va2 = EnthesialMarker.parse('S.5')
        self.assertEqual(EnthesialMarker.avg(va1, va2), EnthesialMarker.parse('S.5'))

    def test_as_num(self):
        self.assertEqual(EnthesialMarker.parse('0').as_num(), 0.0)
        self.assertEqual(EnthesialMarker.parse('.5').as_num(), 0.5)
        self.assertEqual(EnthesialMarker.parse('3').as_num(), 3.0)
        self.assertEqual(EnthesialMarker.parse('s.5').as_num(), 3.5)
        self.assertEqual(EnthesialMarker.parse('s3').as_num(), 6.0)
        self.assertEqual(EnthesialMarker.parse('oe0.5').as_num(), 6.5)
        self.assertEqual(EnthesialMarker.parse('oe3').as_num(), 9.0)


def main():
    unittest.main()


if __name__ == "__main__":
    main()
