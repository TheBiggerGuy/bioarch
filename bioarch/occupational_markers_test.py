#!/usr/bin/env python


from importlib.resources import open_binary
import json
from random import Random
import unittest


from . import test as bioarch_test
from .left_right import LeftRight
from .occupational_markers import EnthesialMarker, OccupationalMarkers


class EnthesialMarkerTest(unittest.TestCase):
    def test_parse(self):
        self.assertEqual(EnthesialMarker.parse(None), None)

        self.assertEqual(EnthesialMarker.parse(0), EnthesialMarker(0))
        self.assertEqual(EnthesialMarker.parse(0.0), EnthesialMarker(0))

        self.assertEqual(EnthesialMarker.parse(0.0), EnthesialMarker(0.0, is_s=False, is_oe=False))
        self.assertEqual(EnthesialMarker.parse(0.5), EnthesialMarker(0.5, is_s=False, is_oe=False))

        self.assertEqual(EnthesialMarker.parse(3.5), EnthesialMarker(0.5, is_s=True, is_oe=False))
        self.assertEqual(EnthesialMarker.parse(4.0), EnthesialMarker(1.0, is_s=True, is_oe=False))

        self.assertEqual(EnthesialMarker.parse(6.5), EnthesialMarker(0.5, is_s=False, is_oe=True))
        self.assertEqual(EnthesialMarker.parse(7.0), EnthesialMarker(1.0, is_s=False, is_oe=True))

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


class OccupationalMarkersTest(unittest.TestCase):
    def setUp(self):
        self.random = Random(666)

    def random_em(self):
        return EnthesialMarker.parse(self.random.choice((None, 0, 1.5, 3.0, 3.5, 6.5)))

    def test_to_pd_data_frame_values(self):
        df = OccupationalMarkers(*[LeftRight(self.random_em(), self.random_em()) for _ in range(0, 67)]).to_pd_data_frame('id1')

        with open_binary(bioarch_test, 'OccupationalMarkersTest.test_to_pd_data_frame_values.json') as json_stream:
            expected_json = json.load(json_stream)

        print(df.to_json(orient='records'))
        actual_json = json.loads(df.to_json(orient='records'))

        self.assertEqual(actual_json, expected_json)

    def test_to_pd_data_frame_empty(self):
        df = OccupationalMarkers.empty().to_pd_data_frame('id1')

        with open_binary(bioarch_test, 'OccupationalMarkersTest.test_to_pd_data_frame_empty.json') as json_stream:
            expected_json = json.load(json_stream)

        print(df.to_json(orient='records'))
        actual_json = json.loads(df.to_json(orient='records'))

        self.assertEqual(actual_json, expected_json)


def main():
    unittest.main()


if __name__ == "__main__":
    main()
