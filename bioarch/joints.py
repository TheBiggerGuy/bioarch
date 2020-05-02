#!/usr/bin/env python


import enum
from enum import Enum
import functools
import logging
from statistics import mean


import pandas as pd
from pandas.api.types import CategoricalDtype


from .left_right import LeftRight


logger = logging.getLogger(__name__)


@functools.total_ordering
@enum.unique
class JointCondition(Enum):
    """
    1 - slight/mild
    2 - medium
    3 - extreme
    4 - fused
    5 - SCHMORL NODES
    6 - FRACTURE
    """
    NORMAL          =  0  # noqa: E221,E222
    MILD            =  1  # noqa: E221,E222
    MEDIUM          =  2  # noqa: E221,E222
    EXTREME         =  3  # noqa: E221,E222
    FUSED           =  4  # noqa: E221,E222
    SCHMORL_NODES   =  5  # noqa: E221,E222
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
            return None
        logger.error('Failed to parse JointCondition: "%s"', value)
        raise ValueError

    @staticmethod
    def avg(left, right):
        if left is None:
            return right
        if right is None:
            return left
        return JointCondition(int(mean((left.value, right.value))))

    def __lt__(self, other):
        if other is None:
            return False
        if isinstance(other, int):
            other = JointCondition(other)
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
        return CategoricalDtype(categories=[s.name for s in JointCondition], ordered=True)


JOINTS_SUMMARY_STATS = {
    'cervical': set(['c1_3', 'c4_7']),
    'thoracic': set(['t1_4', 't5_8', 't9_12']),
    'lumbar': set(['l1_5']),
}


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
        args = [LeftRight(None, None)] * 6
        args += [None] * 7
        return Joints(*args)

    def to_pd_data_frame(self, index):
        data = {
            'id': pd.Series([index]),
        }
        for key, value in self.__dict__.items():
            if isinstance(value, LeftRight):
                data[f'{key}_left'] = pd.Series([value.left.name if value.left else None], copy=True, dtype=JointCondition.dtype())
                data[f'{key}_right'] = pd.Series([value.right.name if value.right else None], copy=True, dtype=JointCondition.dtype())
                avg = value.avg()
                data[f'{key}_avg'] = pd.Series([avg.name if avg else None], copy=True, dtype=JointCondition.dtype())
            else:
                data[f'{key}'] = pd.Series([value.name if value else None], copy=True, dtype=JointCondition.dtype())

        for prefix, cols in JOINTS_SUMMARY_STATS.items():
            subset = [value for key, value in self.__dict__.items() if key in cols and value is not None]
            min_val = min(subset) if subset else None
            max_val = max(subset) if subset else None
            count = len(subset)
            data[f'{prefix}_min'] = pd.Series([min_val.name if min_val else None], copy=True, dtype=JointCondition.dtype())
            data[f'{prefix}_max'] = pd.Series([max_val.name if max_val else None], copy=True, dtype=JointCondition.dtype())
            data[f'{prefix}_count'] = pd.Series([count], copy=True)

        return pd.DataFrame.from_dict(data).set_index('id')


if __name__ == "__main__":
    raise RuntimeError('No main available')
