#!/usr/bin/env python


import logging
from typing import List, Optional, Union


from ensure import check, ensure_annotations
import pandas as pd


logger = logging.getLogger(__name__)


VALID_TEETH    = ('NA', '0', '1', 'A', 'B1', 'B2', 'C', 'D', 'E', 'F', 'G', 'H', 'I')  # noqa: E221
VALID_CALCULUS = ('NA', '0', '1', '2', '3')
VALID_EH       = ('NA', '0', '1')  # noqa: E221
VALID_CAVITIES = ('NA', '0', '1')
VALID_ABCESS   = ('NA', '0', '1')  # noqa: E221


class Tooth(object):
    """docstring for Tooth"""

    __slots__ = ['_tooth', '_calculus', '_eh', '_cavities', '_abcess']

    @ensure_annotations
    def __init__(self, tooth: str, calculus: str, eh: str, cavities: str, abcess: str):
        check(tooth).is_in(VALID_TEETH).or_raise(ValueError)
        check(calculus).is_in(VALID_CALCULUS).or_raise(ValueError)
        check(eh).is_in(VALID_EH).or_raise(ValueError)
        check(cavities).is_in(VALID_CAVITIES).or_raise(ValueError)
        check(abcess).is_in(VALID_ABCESS).or_raise(ValueError)
        # If there is no tooth then there can be no calculus, eh or cavities.
        # Note there can be abcess
        if tooth == 'NA':
            check(calculus).equals('NA').or_raise(ValueError)
            check(eh).equals('NA').or_raise(ValueError)
            check(cavities).equals('NA').or_raise(ValueError)

        self._tooth: str = tooth
        self._calculus: str = calculus
        self._eh: str = eh
        self._cavities: str = cavities
        self._abcess: str = abcess

    @property
    def tooth(self) -> str:
        """
        'NA', '0', '1', 'A', 'B1', 'B2', 'C', 'D', 'E', 'F', 'G', 'H', 'I'
        """
        return self._tooth

    @property
    def calculus(self) -> str:
        """
        'NA', '0', '1', '2', '3'
        """
        return self._calculus

    @property
    def eh(self) -> str:
        """
        'NA', '0', '1'
        """
        return self._eh

    @property
    def cavities(self) -> str:
        """
        'NA', '0', '1'
        """
        return self._cavities

    @property
    def abcess(self) -> str:
        """
        'NA', '0', '1'
        """
        return self._abcess

    @staticmethod
    def empty():
        return Tooth('NA', 'NA', 'NA', 'NA', 'NA')

    def _to_pd_value(self, label: str) -> Optional[Union[int, bool]]:
        val = getattr(self, label)
        if val == 'NA':
            return None

        if label == 'tooth':
            return VALID_TEETH.index(val) - 1
        if label == 'calculus':
            return VALID_CALCULUS.index(val) - 1
        if label in ('eh', 'cavities', 'abcess'):
            return bool(int(val))
        raise RuntimeError

    def to_pd_series(self, prefix=''):
        labels = []
        values = []
        for label in self.__slots__:
            label = label[1:]
            labels.append(f'{prefix}{label}')
            val = getattr(self, label)
            values.append(val)
            labels.append(f'{prefix}{label}_val')
            values.append(self._to_pd_value(label))
        return pd.Series(values, index=labels, copy=True)

    def __eq__(self, other):
        if other is None:
            return False
        if type(other) != type(self):  # pylint: disable=C0123
            raise NotImplementedError
        return (self.tooth, self.calculus, self.eh, self.cavities, self.abcess) == (other.tooth, other.calculus, other.eh, other.cavities, other.abcess)


class Mouth(object):
    """Object to hold the 32 teeth"""
    def __init__(self, teeth: List[Tooth]):
        if len(teeth) != 32:
            raise ValueError(f'Incorrect number of teeth: {len(teeth)}')
        self.teeth = teeth

    @staticmethod
    def empty():
        return Mouth([Tooth.empty()] * 32)

    def to_pd_series(self, prefix=''):
        number_of_teeth = sum([1 for t in self.teeth if t.tooth != 'NA'])
        s = pd.Series([number_of_teeth], index=[f'{prefix}number_of_teeth'], copy=True)
        for i, tooth in enumerate(self.teeth):
            s = s.append(tooth.to_pd_series(prefix=f'{prefix}tooth_{i}_'))
        for label in Tooth.__slots__:
            label = label[1:]
            subset = pd.Series([v for k, v in s.items() if label in k and k.endswith('_val')])
            s = s.append(pd.Series([subset.mean(skipna=True)], index=[f'{prefix}{label}_mean']))
            s = s.append(pd.Series([subset.max(skipna=True)], index=[f'{prefix}{label}_max']))
            s = s.append(pd.Series([subset.min(skipna=True)], index=[f'{prefix}{label}_min']))
            s = s.append(pd.Series([subset.count()], index=[f'{prefix}{label}_count']))
        return s


if __name__ == "__main__":
    raise RuntimeError('No main available')
