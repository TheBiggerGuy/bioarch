#!/usr/bin/env python


import enum
from enum import Enum
import functools
import logging


from pandas.api.types import CategoricalDtype


logger = logging.getLogger(__name__)


@functools.total_ordering
@enum.unique
class Sex(Enum):
    MALE           = 100  # noqa: E221
    MALE_LIKELY    =  90  # noqa: E221,E222
    MALE_ASSUMED   =  80  # noqa: E221,E222
    UNKNOWN        =  50  # noqa: E221,E222
    FEMALE_ASSUMED =  20  # noqa: E221,E222
    FEMALE_LIKELY  =  10  # noqa: E221,E222
    FEMALE         =   0  # noqa: E221,E222

    @staticmethod
    def parse(value):
        if value is None:
            return None
        if type(value) == Sex:  # pylint: disable=C0123
            return value
        if not isinstance(value, str):
            raise ValueError(f'Failed to parse sex: "{value}"')
        value = value.upper()
        if value == 'M':
            return Sex.MALE
        if value in ('M?', '?M'):
            return Sex.MALE_LIKELY
        if value in ('M??', '??M'):
            return Sex.MALE_ASSUMED
        if value == 'F':
            return Sex.FEMALE
        if value in ('F?', '?F'):
            return Sex.FEMALE_LIKELY
        if value in ('F??', '??F'):
            return Sex.FEMALE_ASSUMED
        if value == '?':
            return Sex.UNKNOWN
        logger.error('Failed to parse sex: "%s"', value)
        return Sex.UNKNOWN

    def as_bin(self):
        if self == Sex.UNKNOWN:
            return None
        if int(self.value) > 50:  # For to int to fix https://github.com/PyCQA/pylint/issues/2306
            return Sex.MALE
        return Sex.FEMALE

    def __lt__(self, other):
        if other is None:
            return False
        if isinstance(other, int):
            other = Sex(other)
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
        return CategoricalDtype(categories=[s.name for s in Sex], ordered=True)


if __name__ == "__main__":
    raise RuntimeError('No main available')
