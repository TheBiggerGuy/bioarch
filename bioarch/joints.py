#!/usr/bin/env python


import enum
from enum import Enum
import functools
import logging
from statistics import mean


import pandas as pd


from .left_right import LeftRight


logger = logging.getLogger(__name__)


def is_none_or_na(condition):
    if condition is None:
        return True
    if isinstance(condition, LeftRight):
        return is_none_or_na(condition.avg())
    return condition == JointCondition.NOT_PRESENT


@functools.total_ordering
@enum.unique
class JointCondition(Enum):
    """
    NA- does not exist
    1 - slight/mild
    2 - medium
    3 - extreme
    4 - fused
    5 - SCHMORALS NODES
    6 - FRACTURE
    """
    NOT_PRESENT     = -1  # noqa: E221,E222
    NORMAL          =  0  # noqa: E221,E222
    MILD            =  1  # noqa: E221,E222
    MEDIUM          =  2  # noqa: E221,E222
    EXTREAM         =  3  # noqa: E221,E222
    FUSED           =  4  # noqa: E221,E222
    SCHMORALS_NODES =  5  # noqa: E221,E222
    FRACTURE        =  6  # noqa: E221,E222

    @staticmethod
    def parse(value):
        if value is None:
            return None
        if type(value) == JointCondition:  # pylint: disable=C0123
            return value
        if isinstance(value, int):
            value = str(value)
        if not isinstance(value, str):
            raise ValueError(f'Failed to parse JointCondition: "{value}"')
        value = value.upper()
        for condition in JointCondition:
            if value == condition.name:
                return condition
            if value == str(condition.value):
                return condition
        if value in ('NA', 'N'):
            return JointCondition.NOT_PRESENT
        logger.error('Failed to parse JointCondition: "%s"', value)
        raise ValueError

    @staticmethod
    def avg(left, right):
        if left in (None, JointCondition.NOT_PRESENT):
            return right
        if right in (None, JointCondition.NOT_PRESENT):
            return left
        return JointCondition(int(mean((left.value, right.value))))

    def __lt__(self, other):
        if other is None:
            return False
        if other == float('inf'):
            return True
        if other == float('-inf'):
            return False
        if isinstance(other, int):
            other = JointCondition(other)
        if type(other) != type(self):  # pylint: disable=C0123
            logger.warning('Attempt to compare: %s (%s) with %s (%s)', self, type(self), other, type(other))
            raise NotImplementedError
        return (self.value < other.value)  # pylint: disable=C0325,W0143

    def __repr__(self):
        return f'{self.__class__.__name__}: {self}'

    def __str__(self):
        return self.name


class Joints(object):  # pylint: disable=R0902
    """docstring for Joints"""
    def __init__(self, shoulder: LeftRight[JointCondition], elbow: LeftRight[JointCondition], wrist: LeftRight[JointCondition], hip: LeftRight[JointCondition], knee: LeftRight[JointCondition], ankle: LeftRight[JointCondition], sacro_illiac: JointCondition, c1_3: JointCondition, c4_7: JointCondition, t1_4: JointCondition, t5_8: JointCondition, t9_12: JointCondition, l1_5: JointCondition):
        self.shoulder = shoulder
        self.elbow = elbow
        self.wrist = wrist
        self.hip = hip
        self.knee = knee
        self.ankle = ankle
        self.sacro_illiac = sacro_illiac
        self.c1_3 = c1_3
        self.c4_7 = c4_7
        self.t1_4 = t1_4
        self.t5_8 = t5_8
        self.t9_12 = t9_12
        self.l1_5 = l1_5

    @staticmethod
    def empty():
        args = [LeftRight(JointCondition.NOT_PRESENT, JointCondition.NOT_PRESENT)] * 6
        args += [JointCondition.NOT_PRESENT] * 7
        return Joints(*args)

    @staticmethod
    def _to_pd_value(condition: JointCondition):
        if condition is None:
            return None
        if condition == JointCondition.NOT_PRESENT:
            return None
        return condition.name

    def _to_pd_series(self, subset_of_self, prefix):  # pylint: disable=R0201
        labels = []
        values = []
        for key, value in subset_of_self.items():
            if isinstance(value, LeftRight):
                labels.append(f'{prefix}{key}_left')
                values.append(Joints._to_pd_value(value.left))
                labels.append(f'{prefix}{key}_right')
                values.append(Joints._to_pd_value(value.right))
                labels.append(f'{prefix}{key}_avg')
                values.append(Joints._to_pd_value(value.avg()))
            else:
                labels.append(f'{prefix}{key}')
                values.append(Joints._to_pd_value(value))
                labels.append(f'{prefix}{key}_avg')
                values.append(Joints._to_pd_value(value))
        s = pd.Series(values, index=labels, copy=True)

        subset = pd.Series([JointCondition.parse(v).value for k, v in s.items() if not is_none_or_na(v) and k.endswith('_avg')])
        s = s.append(pd.Series([subset.mean(skipna=True)], index=[f'{prefix}mean']))
        s = s.append(pd.Series([subset.max(skipna=True)], index=[f'{prefix}max']))
        s = s.append(pd.Series([subset.min(skipna=True)], index=[f'{prefix}min']))
        s = s.append(pd.Series([subset.count()], index=[f'{prefix}count']))
        return s

    def to_pd_series(self, prefix=''):
        return pd.concat([self._to_pd_series({k: v for k, v in self.__dict__.items()}, f'{prefix}all_'),  # pylint: disable=R1721
                          self._to_pd_series({k: v for k, v in self.__dict__.items() if k.startswith('c')}, f'{prefix}cervical_'),
                          self._to_pd_series({k: v for k, v in self.__dict__.items() if k.startswith('t')}, f'{prefix}thoracic_'),
                          self._to_pd_series({k: v for k, v in self.__dict__.items() if k.startswith('l')}, f'{prefix}lumbar_')])


if __name__ == "__main__":
    raise RuntimeError('No main available')
