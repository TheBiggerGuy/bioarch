#!/usr/bin/env python


import enum
from enum import Enum
import functools
import logging
from typing import Any, cast, Optional


from ensure import ensure_annotations
import pandas as pd


logger = logging.getLogger(__name__)


@functools.total_ordering
@enum.unique
class AgeCategory(Enum):
    UNKNOWN     = 0  # noqa: E221,E222
    YOUNG       = 1  # noqa: E221,E222
    YOUNG_ADULT = 2
    ADULT       = 3  # noqa: E221,E222
    MIDDLE      = 4  # noqa: E221,E222
    MIDDLE_OLD  = 5  # noqa: E221
    OLD         = 6  # noqa: E221,E222

    @staticmethod
    def parse(value: Any) -> Optional['AgeCategory']:
        if value is None:
            return None
        if type(value) == AgeCategory:  # pylint: disable=C0123
            return cast(AgeCategory, value)
        if not isinstance(value, str):
            raise ValueError(f'Failed to parse {AgeCategory.__name__}: "{value}"')
        value = value.upper()
        for category in AgeCategory:
            if value == category.name:
                return category
        if value == 'OA':
            return AgeCategory.OLD
        if value == 'MIDDLE/OLD':
            return AgeCategory.MIDDLE_OLD
        if value == 'YOUNG ADULT':
            return AgeCategory.YOUNG_ADULT
        raise ValueError(f'Failed to parse {AgeCategory.__name__}: "{value}"')

    def __lt__(self, other):
        if other is None:
            return False
        if isinstance(other, int):
            other = AgeCategory(other)
        if type(other) != type(self):  # pylint: disable=C0123
            logger.warning('Attempt to compare: %s with %s', self, other)
            raise NotImplementedError
        return (self.value < other.value)  # pylint: disable=C0325,W0143

    def __repr__(self):
        return f'{self.__class__.__name__}: {self}'

    def __str__(self):
        return self.name


class EstimatedAge(object):
    """docstring for EstimatedAge"""

    MAX_AGE = 100

    @ensure_annotations
    def __init__(self, category: str, ranged: str):
        self.category = AgeCategory.parse(category)  # pylint: disable=W0212
        self.ranged = EstimatedAge._parse_range(ranged)

    @staticmethod
    def _parse_range(range_input: Any):
        if range_input is None or range_input in ('None', '?', 'UNKNOWN'):
            return None
        if isinstance(range_input, range):
            return range_input
        if not isinstance(range_input, str):
            raise ValueError(f'Unknown age range format: "{range_input}" type({type(range_input)})')
        range_str = range_input
        if '-' in range_str:
            parts = range_str.split('-')
            if len(parts) != 2:
                raise ValueError
            return range(int(parts[0]), int(parts[1]))

        if range_str.endswith('+'):
            start = range_str[:-1]
            return range(int(start), EstimatedAge.MAX_AGE)

        if range_str.startswith('='):
            age = int(range_str[1:])
            return range(age, age + 1)

        raise ValueError(f'Unknown age range format: "{range_str}"')

    @staticmethod
    def empty():
        return EstimatedAge('UNKNOWN', 'UNKNOWN')

    def to_pd_series(self, prefix=''):
        ranged_val = None if self.ranged is None else pd.RangeIndex.from_range(self.ranged)
        values = [self.category.name, self.category.value, ranged_val]
        labels = [f'{prefix}category', f'{prefix}category_val', f'{prefix}ranged_val']
        return pd.Series(values, index=labels, copy=True)


if __name__ == "__main__":
    raise RuntimeError('No main available')
