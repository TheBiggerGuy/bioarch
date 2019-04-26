#!/usr/bin/env python


import unittest


from .sex import Sex


class SexTest(unittest.TestCase):
    def test_order(self):
        self.assertEqual(sorted([Sex.MALE, Sex.FEMALE]), [Sex.FEMALE, Sex.MALE])
        self.assertEqual(sorted([Sex.MALE_LIKELY, Sex.MALE_ASSUMED]), [Sex.MALE_ASSUMED, Sex.MALE_LIKELY])
        # None is sorted first
        self.assertEqual(sorted([Sex.MALE_LIKELY, Sex.MALE_ASSUMED, None]), [None, Sex.MALE_ASSUMED, Sex.MALE_LIKELY])
        # Numbers are sorted as if they where Sex.value
        self.assertEqual(sorted([0, 100, Sex.MALE_ASSUMED]), [0, Sex.MALE_ASSUMED, 100])
        # Invalid numbers fail
        with self.assertRaises(ValueError):
            [Sex.MALE_ASSUMED, -1].sort()

    def test_parse(self):
        self.assertEqual(Sex.parse('M'), Sex.MALE)
        self.assertEqual(Sex.parse('M?'), Sex.MALE_LIKELY)
        self.assertEqual(Sex.parse('?M'), Sex.MALE_LIKELY)
        self.assertEqual(Sex.parse('M??'), Sex.MALE_ASSUMED)
        self.assertEqual(Sex.parse('??M'), Sex.MALE_ASSUMED)
        self.assertEqual(Sex.parse('?'), Sex.UNKNOWN)
        self.assertEqual(Sex.parse('F??'), Sex.FEMALE_ASSUMED)
        self.assertEqual(Sex.parse('??F'), Sex.FEMALE_ASSUMED)
        self.assertEqual(Sex.parse('F?'), Sex.FEMALE_LIKELY)
        self.assertEqual(Sex.parse('?F'), Sex.FEMALE_LIKELY)
        self.assertEqual(Sex.parse('F'), Sex.FEMALE)

        self.assertEqual(Sex.parse('M'), Sex.parse('m'))
        self.assertEqual(Sex.parse(None), None)
        self.assertEqual(Sex.parse(Sex.MALE), Sex.MALE)


def main():
    unittest.main()


if __name__ == "__main__":
    main()
