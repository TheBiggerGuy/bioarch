#!/usr/bin/env python


import unittest


from .context import Context


class ContextTest(unittest.TestCase):
    def test_constructor(self):
        self.assertEqual(Context({'thing': True}).tags['thing'], True)
        self.assertEqual(Context({'thing': False}).tags['thing'], False)

        self.assertEqual(Context({'thing': None}).tags['thing'], None)
        self.assertEqual(Context({'thing': 'NA'}).tags['thing'], None)
        self.assertEqual(Context({'thing': 'na'}).tags['thing'], None)

        with self.assertRaises(ValueError):
            Context({'spear': 'foo'})

        with self.assertRaises(ValueError):
            Context({'spear': 10})

    def test_to_pd_data_frame(self):
        context = Context({'spear': True,
                           'pots': 'NA',
                           'knife': None})

        df = context.to_pd_data_frame('id1', prefix='context_')

        self.assertEqual(df.to_json(orient='records'), '[{"context_all_spear":true,"context_all_pots":null,"context_all_knife":null,"context_all_count":1,"context_utilitarian_knife":null,"context_utilitarian_count":0,"context_textile_count":0,"context_equestrian_count":0,"context_economic_count":0,"context_organic_material_count":0,"context_appearance_count":0,"context_burial_container_count":0,"context_weapons_spear":1,"context_weapons_count":1,"context_iron_fragment_count":0,"context_miscellaneous_count":0}]')

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
                              'Iron_pole': set(['weapons']),  # Should not be iron_fragment
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
