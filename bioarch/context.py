#!/usr/bin/env python


import enum
from enum import Enum
import functools
import logging
from typing import Any, cast, Dict, Optional, Union


import pandas as pd
from pandas.api.types import CategoricalDtype


logger = logging.getLogger(__name__)


@functools.total_ordering
@enum.unique
class CompassBearing(Enum):
    NORTH      = 0  # noqa: E221
    NORTH_EAST = 1
    EAST       = 2  # noqa: E221
    SOUTH_EAST = 3
    SOUTH      = 4  # noqa: E221
    SOUTH_WEST = 5
    WEST       = 6  # noqa: E221
    NORTH_WEST = 7

    @staticmethod
    def parse(value: Any) -> Optional['CompassBearing']:
        if value is None:
            return None
        if type(value) == CompassBearing:  # pylint: disable=C0123
            return cast(CompassBearing, value)
        if not isinstance(value, str):
            raise ValueError(f'Failed to parse {CompassBearing.__name__}: "{value}"')
        value = value.upper()
        for bearing in CompassBearing:
            if value == bearing.name:
                return bearing
            if value == bearing.to_short_code():
                return bearing
        raise ValueError(f'Failed to parse {CompassBearing.__name__}: "{value}"')

    def to_short_code(self):
        return ''.join([p[0] for p in str(self.name).split('_')])

    def __lt__(self, other):
        if other is None:
            return False
        if isinstance(other, int):
            other = CompassBearing(other)
        if type(other) != type(self):  # pylint: disable=C0123
            logger.warning('Attempt to compare: %s with %s', self, other)
            raise NotImplementedError
        return (self.value < other.value)  # pylint: disable=C0325,W0143

    def __repr__(self):
        return f'{self.__class__.__name__}: {self}'

    def __str__(self):
        return self.name

    @staticmethod
    def dtype():
        return CategoricalDtype(categories=[s.name for s in CompassBearing], ordered=True)


@functools.total_ordering
@enum.unique
class Present(Enum):
    NOT_PRESENT = 0
    PRESENT     = 1  # noqa: E221

    @staticmethod
    def parse(value: Any) -> Optional['Present']:
        if value is None:
            return None
        if isinstance(value, str) and value.upper() == 'NA':
            return None
        if type(value) == Present:  # pylint: disable=C0123
            return cast(Present, value)
        if value in (0, 0.0, '0', False):
            return Present.NOT_PRESENT
        if value in (1, 1.0, '1', True):
            return Present.PRESENT
        raise ValueError(f'Failed to parse {Present.__name__}: "{value}"')

    def __lt__(self, other):
        if other is None:
            return False
        if isinstance(other, int):
            other = Present(other)
        if type(other) != type(self):  # pylint: disable=C0123
            logger.warning('Attempt to compare: %s with %s', self, other)
            raise NotImplementedError
        return (self.value < other.value)  # pylint: disable=C0325,W0143

    def __repr__(self):
        return f'{self.__class__.__name__}: {self}'

    def __str__(self):
        return self.name

    @staticmethod
    def dtype():
        return CategoricalDtype(categories=[s.name for s in Present], ordered=True)


@functools.total_ordering
@enum.unique
class BodyPosition(Enum):
    SUPINE              = 0  # noqa: E221
    SUPINE_FIXED_LEGS   = 1  # noqa: E221
    CROUCHED            = 2  # noqa: E221
    CROUCHED_LEFT_SIDE  = 3  # noqa: E221
    CROUCHED_RIGHT_SIDE = 4
    STOMACH             = 5  # noqa: E221

    @staticmethod
    def parse(value: Any) -> Optional['BodyPosition']:
        if value is None:
            return None
        if isinstance(value, str) and value.upper() == 'NA':
            return None
        if type(value) == BodyPosition:  # pylint: disable=C0123
            return cast(BodyPosition, value)
        if isinstance(value, str):
            value = value.upper()
        for position in BodyPosition:
            if value == position.name:
                return position
            if value == position.value:
                return position
        raise ValueError(f'Failed to parse {BodyPosition.__name__}: "{value}"')

    def __lt__(self, other):
        if other is None:
            return False
        if isinstance(other, int):
            other = BodyPosition(other)
        if type(other) != type(self):  # pylint: disable=C0123
            logger.warning('Attempt to compare: %s with %s', self, other)
            raise NotImplementedError
        return (self.value < other.value)  # pylint: disable=C0325,W0143

    def __repr__(self):
        return f'{self.__class__.__name__}: {self}'

    def __str__(self):
        return self.name

    @staticmethod
    def dtype():
        return CategoricalDtype(categories=[s.name for s in BodyPosition], ordered=True)


KNOWN_GROUPS = {
    'utilitarian'  : set(['knife', 'whetstone', 'awl', 'scissors', 'vessel', 'pot_sherd', 'flint', 'flakes', 'flint_flakes']),  # noqa: E203
    'textile'      : set(['textile', 'needle', 'spindle_whorl']),  # noqa: E203
    'equestrian'   : set(['equestrian', 'horse_equipment']),  # noqa: E203
    'economic'     : set(['coins', 'scales']),  # noqa: E203
    'organic_material': set(['animal_remains', 'charcoal', 'flower', 'shell', 'burned_bones']),
    'appearance'   : set(['brooch', 'cloak ring', 'bracelet', 'beads', 'comb', 'buckle', 'mounts', 'cloak_fastener', 'iron_ring']),  # noqa: E203
    'burial_container': set(['coffin', 'coffin_substitute']),
    'weapons'      : set(['sword', 'axe', 'shield_boss', 'spear']),  # noqa: E203
    'iron_fragment': set(['iron frafments', 'nails', 'iron_object', 'iron_nail/rivets']),
    'miscellaneous': set(['lock', 'keys', 'thors_hammer', 'bronze_item', 'bronze_disk', 'quartz', 'unidentified_bronze', 'iron_pole']),
}


class Context(object):
    """docstring for Context"""

    def __init__(self, body_position: Optional[BodyPosition], body_orientation: Optional[CompassBearing], tags: Dict[str, Optional[Union[str, int, bool, float]]]):
        if body_position is not None and not isinstance(body_position, BodyPosition):
            raise ValueError(f'Invalid body_position: "{body_position}"')
        self.body_position = body_position

        if body_orientation is not None and not isinstance(body_orientation, CompassBearing):
            raise ValueError(f'Invalid body_orientation: "{body_orientation}"')
        self.body_orientation = body_orientation

        self.tags = {k.lower(): Present.parse(v) for k, v in tags.items()}

    @staticmethod
    def empty():
        return Context(None, None, {})

    @staticmethod
    def group(value):
        value = value.lower()
        groups = set()
        for group_name, group in KNOWN_GROUPS.items():
            if value in group:
                groups.add(group_name)
        return groups

    def to_pd_data_frame(self, index):
        data = {
            'id': pd.Series([index]),
        }

        data['body_position_cat'] = pd.Series([self.body_position.name if self.body_position else None], copy=True, dtype=BodyPosition.dtype())
        data['body_position_val'] = pd.Series([self.body_position.value if self.body_position else None], copy=True, dtype='Int64')

        data['body_orientation_cat'] = pd.Series([self.body_orientation.name if self.body_orientation else None], copy=True, dtype=CompassBearing.dtype())
        data['body_orientation_val'] = pd.Series([self.body_orientation.value if self.body_orientation else None], copy=True, dtype='Int64')

        for key, value in self.tags.items():
            data[f'all_{key}_cat'] = pd.Series([value.name if value else None], copy=True, dtype=Present.dtype())
            data[f'all_{key}_val'] = pd.Series([value.value if value else None], copy=True, dtype='Int64')

        for group_name, group in KNOWN_GROUPS.items():
            status_set = {v for k, v in self.tags.items() if k in group and v}
            if Present.PRESENT in status_set:
                present = Present.PRESENT
            elif Present.NOT_PRESENT in status_set:
                present = Present.NOT_PRESENT
            else:
                present = None
            data[f'{group_name}_cat'] = pd.Series([present.name if present else None], copy=True, dtype=Present.dtype())
            data[f'{group_name}_val'] = pd.Series([present.value if present else None], copy=True, dtype='Int64')

        return pd.DataFrame.from_dict(data).set_index('id')


if __name__ == "__main__":
    raise RuntimeError('No main available')
