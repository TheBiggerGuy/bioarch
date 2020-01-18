#!/usr/bin/env python


import unittest


from pandas.api.types import CategoricalDtype


from .context import CompassBearing, Context, Present


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
        self.assertEqual(Context(None, None, {'thing': True}).tags['thing'], Present.PRESENT)
        self.assertEqual(Context(None, None, {'thing': False}).tags['thing'], Present.NOT_PRESENT)

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
                           'comb': 'NA',
                           'knife': None})

        df = context.to_pd_data_frame('id1')

        self.assertIsInstance(df['body_orientation_cat'].dtypes, CategoricalDtype)
        self.assertIsInstance(df['all_spear_cat'].dtypes, CategoricalDtype)
        self.assertIsInstance(df['weapons_cat'].dtypes, CategoricalDtype)
        self.assertEqual(df.to_json(orient='records'), '[{"body_position":"supine with flexed legs","body_orientation_cat":"NORTH","body_orientation_val":0,"all_spear_cat":"PRESENT","all_spear_val":1,"all_comb_cat":null,"all_comb_val":null,"all_knife_cat":null,"all_knife_val":null,"utilitarian_cat":null,"utilitarian_val":null,"textile_cat":null,"textile_val":null,"equestrian_cat":null,"equestrian_val":null,"economic_cat":null,"economic_val":null,"organic_material_cat":null,"organic_material_val":null,"appearance_cat":null,"appearance_val":null,"burial_container_cat":null,"burial_container_val":null,"weapons_cat":"PRESENT","weapons_val":1,"iron_fragment_cat":null,"iron_fragment_val":null,"miscellaneous_cat":null,"miscellaneous_val":null}]')

        context = Context(1,
                          None,
                          {'spear': True,
                           'comb': 'NA',
                           'knife': None})

        df = context.to_pd_data_frame('id1')
        self.assertIsInstance(df['body_orientation_cat'].dtypes, CategoricalDtype)
        self.assertIsInstance(df['all_comb_cat'].dtypes, CategoricalDtype)
        self.assertIsInstance(df['appearance_cat'].dtypes, CategoricalDtype)
        self.assertEqual(df.to_json(orient='records'), '[{"body_position":"supine with flexed legs","body_orientation_cat":null,"body_orientation_val":null,"all_spear_cat":"PRESENT","all_spear_val":1,"all_comb_cat":null,"all_comb_val":null,"all_knife_cat":null,"all_knife_val":null,"utilitarian_cat":null,"utilitarian_val":null,"textile_cat":null,"textile_val":null,"equestrian_cat":null,"equestrian_val":null,"economic_cat":null,"economic_val":null,"organic_material_cat":null,"organic_material_val":null,"appearance_cat":null,"appearance_val":null,"burial_container_cat":null,"burial_container_val":null,"weapons_cat":"PRESENT","weapons_val":1,"iron_fragment_cat":null,"iron_fragment_val":null,"miscellaneous_cat":null,"miscellaneous_val":null}]')

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
