#!/usr/bin/env python


from typing import Dict, Optional, Union


import pandas as pd


def parse_value(value):
    if value is None:
        return None
    if isinstance(value, str) and value.upper() == 'NA':
        return None
    if value in (1, '1'):
        return True
    if value in (0, '0'):
        return False
    raise ValueError(f'Failed to parse Boolean value "{value}" for context')


KNOWN_GROUPS = {
    'utilitarian'  : set(['knife', 'whetstone', 'awl', 'scissors', 'vessel', 'pot_sherd', 'flint', 'flakes', 'flint_flakes']),  # noqa: E203
    'textile'      : set(['textile', 'needle', 'spindle_whorl']),  # noqa: E203
    'equestrian'   : set(['equestrian', 'horse_equipment']),  # noqa: E203
    'economic'     : set(['coins', 'scales']),  # noqa: E203
    'organic_material': set(['animal_remains', 'charcoal', 'flower', 'shell', 'burned_bones']),
    'appearance'   : set(['brooch', 'cloak ring', 'bracelet', 'beads', 'comb', 'buckle', 'mounts', 'cloak_fastener', 'iron_ring']),  # noqa: E203
    'burial_container': set(['coffin', 'coffin_substitute']),
    'weapons'      : set(['sword', 'axe', 'iron_pole', 'shield_boss', 'spear']),  # noqa: E203
    'iron_fragment': set(['iron frafments', 'nails', 'iron_object', 'iron_nail/rivets']),
    'miscellaneous': set(['lock', 'keys', 'thors_hammer', 'bronze_item', 'bronze_disk', 'quartz', 'unidentified_bronze']),
}


class Context(object):
    """docstring for Context"""

    def __init__(self, tags: Dict[str, Optional[Union[str, int, bool, float]]]):
        self.tags = {k: parse_value(v) for k, v in tags.items()}

    @staticmethod
    def empty():
        return Context({})

    @staticmethod
    def group(value):
        value = value.lower()
        groups = set()
        for group_name, group in KNOWN_GROUPS.items():
            if value in group:
                groups.add(group_name)
        return groups

    def _to_pd_series(self, prefix, tags):  # pylint: disable=R0201
        labels = [f'{prefix}{label}' for label in tags.keys()]
        s = pd.Series([val for val in tags.values()], index=labels, copy=True)  # pylint: disable=R1721
        s = s.append(pd.Series([s.count()], index=[f'{prefix}count']))
        return s

    def to_pd_data_frame(self, index, prefix=''):
        group_series = [self._to_pd_series(f'{prefix}all_', self.tags)]
        for group_name, group in KNOWN_GROUPS.items():
            group_series.append(self._to_pd_series(f'{prefix}{group_name}_', {k: v for k, v in self.tags.items() if k.lower() in group}))

        return pd.DataFrame.from_dict({index: pd.concat(group_series)}, orient='index')


if __name__ == "__main__":
    raise RuntimeError('No main available')
