#!/usr/bin/env python


import unittest


from .context import CompassBearing, Context


class CompassBearingTest(unittest.TestCase):
    def test_order(self):
        self.assertEqual(sorted([CompassBearing.SOUTH, CompassBearing.NORTH]), [CompassBearing.NORTH, CompassBearing.SOUTH])
        # None is sorted first
        self.assertEqual(sorted([CompassBearing.SOUTH, CompassBearing.NORTH, None]), [None, CompassBearing.NORTH, CompassBearing.SOUTH])
        # Numbers are sorted as if they where CompassBearing.value
        self.assertEqual(sorted([0, 3, CompassBearing.EAST]), [0, CompassBearing.EAST, 3])
        # Invalid numbers fail
        with self.assertRaises(ValueError):
            [CompassBearing.SOUTH, -1].sort()

    def test_to_short_code(self):
        self.assertEqual(CompassBearing.NORTH.to_short_code(), 'N')
        self.assertEqual(CompassBearing.NORTH_EAST.to_short_code(), 'NE')
        self.assertEqual(CompassBearing.SOUTH.to_short_code(), 'S')

    def test_parse(self):
        self.assertEqual(CompassBearing.parse('NORTH'), CompassBearing.NORTH)
        self.assertEqual(CompassBearing.parse('N'), CompassBearing.NORTH)
        self.assertEqual(CompassBearing.parse(None), None)


class ContextTest(unittest.TestCase):
    def test_constructor_position(self):
        self.assertEqual(Context(0, None, {}).body_position, 'supine')

        self.assertEqual(Context(None, None, {}).body_position, None)
        self.assertEqual(Context('NA', None, {}).body_position, None)

        with self.assertRaises(ValueError):
            Context('foo', None, {})

    def test_constructor_orientation(self):
        self.assertEqual(Context(None, CompassBearing.NORTH, {}).body_orientation, CompassBearing.NORTH)
        self.assertEqual(Context(None, None, {}).body_orientation, None)

        with self.assertRaises(ValueError):
            Context(None, 'NORTH', {})
        with self.assertRaises(ValueError):
            Context(None, 1, {})

    def test_constructor_tags(self):
        self.assertEqual(Context(None, None, {'thing': True}).tags['thing'], True)
        self.assertEqual(Context(None, None, {'thing': False}).tags['thing'], False)

        self.assertEqual(Context(None, None, {'thing': None}).tags['thing'], None)
        self.assertEqual(Context(None, None, {'thing': 'NA'}).tags['thing'], None)
        self.assertEqual(Context(None, None, {'thing': 'na'}).tags['thing'], None)

        with self.assertRaises(ValueError):
            Context(None, None, {'spear': 'foo'})

        with self.assertRaises(ValueError):
            Context(None, None, {'spear': 10})

    def test_to_pd_data_frame(self):
        context = Context(1,
                          CompassBearing.NORTH,
                          {'spear': True,
                           'pots': 'NA',
                           'knife': None})

        df = context.to_pd_data_frame('id1')
        self.assertEqual(df.to_json(orient='records'), '[{"body_position":"supine with flexed legs","body_orientation_cat":"NORTH","body_orientation_val":0,"all_spear":true,"all_pots":null,"all_knife":null,"all_count":1,"utilitarian_knife":null,"utilitarian_count":0,"textile_count":0,"equestrian_count":0,"economic_count":0,"organic_material_count":0,"appearance_count":0,"burial_container_count":0,"weapons_spear":1,"weapons_count":1,"iron_fragment_count":0,"miscellaneous_count":0}]')

        context = Context(1,
                          None,
                          {'spear': True,
                           'pots': 'NA',
                           'knife': None})

        df = context.to_pd_data_frame('id1')
        self.assertEqual(df.to_json(orient='records'), '[{"body_position":"supine with flexed legs","all_spear":true,"all_pots":null,"all_knife":null,"all_count":1,"utilitarian_knife":null,"utilitarian_count":0,"textile_count":0,"equestrian_count":0,"economic_count":0,"organic_material_count":0,"appearance_count":0,"burial_container_count":0,"weapons_spear":1,"weapons_count":1,"iron_fragment_count":0,"miscellaneous_count":0}]')

    def test_known_context_to_group(self):
        known_context_keys = {'knife': set(['utilitarian']),  # Should not be a weapons
                              'Whetstone': set(['utilitarian']),
                              'Awl': set(['utilitarian']),
                              'SCISSORS': set(['utilitarian']),
                              'iron_object': set(['iron_fragment']),
                              'textile': set(['textile']),
                              'spindle_whorl': set(['textile']),
                              'brooch': set(['appearance']),
                              'bracelet': set(['appearance']),
                              'lock': set(['miscellaneous']),
                              'keys': set(['miscellaneous']),
                              'Sword': set(['weapons']),
                              'axe': set(['weapons']),
                              'Iron_pole': set(['miscellaneous']),  # Should not be iron_fragment or weapons
                              'spear': set(['weapons']),
                              'shield_boss': set(['weapons']),
                              'cloak_fastener': set(['appearance']),
                              'iron_ring': set(['appearance']),  # SHould not be iron_fragment
                              'iron_nail/rivets': set(['iron_fragment']),
                              'transport': set(),
                              'Horse_equipment': set(['equestrian']),
                              'coffin_substitute': set(['burial_container']),
                              'coffin': set(['burial_container']),
                              'Mounts': set(['appearance']),
                              'thors_hammer': set(['miscellaneous']),
                              'beads': set(['appearance']),
                              'unidentified_bronze': set(['miscellaneous']),
                              'Bronze_disk': set(['miscellaneous']),
                              'SCALES': set(['economic']),
                              'coins': set(['economic']),
                              'VESSEL': set(['utilitarian']),
                              'comb': set(['appearance']),
                              'buckle': set(['appearance']),
                              'pot_sherd': set(['utilitarian']),
                              'FLINT_FLAKES': set(['utilitarian']),
                              'charcoal': set(['organic_material']),
                              'burned_bones': set(['organic_material']),
                              'quartz': set(['miscellaneous']),
                              'shell': set(['organic_material']),
                              'needle': set(['textile']),
                              'Flower': set(['organic_material']),
                              'animal_remains': set(['organic_material']),
                              'Body_Position': set(),
                              'disturbed': set(),
                              'decapitation': set(),
                              'double_grave': set(),
                              'Body_orientation': set(),
                              'Stone_layer': set()}
        for known_key, known_groups in known_context_keys.items():
            actual_groups = Context.group(known_key)
            self.assertEqual(actual_groups, known_groups, msg=f'{known_key} -> {actual_groups} != {known_groups}')


def main():
    unittest.main()


if __name__ == "__main__":
    main()
