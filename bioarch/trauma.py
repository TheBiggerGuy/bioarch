#!/usr/bin/env python


import enum
from enum import Enum
import logging


import pandas as pd
from pandas.api.types import CategoricalDtype


from .left_right import LeftRight


logger = logging.getLogger(__name__)


@enum.unique
class TraumaCategory(Enum):
    NOT_PRESENT               = -1    # noqa: E221,E222
    PARTIAL_BONE              =  0.5  # noqa: E221,E222
    NORMAL                    =  1    # noqa: E221,E222
    INFECTION                 =  2    # noqa: E221,E222
    FRACTURE                  =  3    # noqa: E221,E222
    UNHEALED_FRACTURE         =  4    # noqa: E221,E222
    CRIBA                     =  5    # noqa: E221,E222
    BLUNT_FORCE_TRAUMA        =  6    # noqa: E221,E222
    SHARP_FORCE_TRAUMA        =  7    # noqa: E221,E222
    TREPONATION               =  8    # noqa: E221,E222
    UNFUSED                   =  9    # noqa: E221,E222
    BONY_GROWTH               = 10    # noqa: E221,E222
    FUSED                     = 11    # noqa: E221,E222
    OSTEOCHONDRITIS_DESSICANS = 12    # noqa: E221,E222

    @staticmethod
    def parse(value):
        if value is None:
            return None
        if type(value) == TraumaCategory:  # pylint: disable=C0123
            return value
        if isinstance(value, (float, int)):
            value = str(value)
        if not isinstance(value, str):
            raise ValueError(f'Failed to parse TraumaCategory: "{value}"')
        value = value.upper()
        for condition in TraumaCategory:
            if value == condition.name:
                return condition
            if value == str(condition.value):
                return condition
        if value in ('NA', 'N'):
            return TraumaCategory.NOT_PRESENT
        logger.error('Failed to parse TraumaCategory: "%s"', value)
        raise ValueError

    @staticmethod
    def avg(left, right):
        if left in (None, TraumaCategory.NOT_PRESENT):
            return right
        if right in (None, TraumaCategory.NOT_PRESENT):
            return left
        raise NotImplementedError()

    def __repr__(self):
        return f'{self.__class__.__name__}: {self}'

    def __str__(self):
        return self.name

    @staticmethod
    def dtype():
        return CategoricalDtype(categories=[s.name for s in TraumaCategory], ordered=True)


class Trauma(object):  # pylint: disable=R0902
    """docstring for Trauma"""

    def __init__(self, facial_bones: TraumaCategory, clavicle: LeftRight[TraumaCategory], scapula: LeftRight[TraumaCategory], humerus: LeftRight[TraumaCategory], ulna: LeftRight[TraumaCategory], radius: LeftRight[TraumaCategory], femur: LeftRight[TraumaCategory], tibia: LeftRight[TraumaCategory], fibula: LeftRight[TraumaCategory], ribs: TraumaCategory, vertabrae: TraumaCategory):
        self.facial_bones = facial_bones

        self.clavicle = clavicle
        self.scapula = scapula
        self.humerus = humerus
        self.ulna = ulna
        self.radius = radius
        self.femur = femur
        self.tibia = tibia
        self.fibula = fibula

        self.ribs = ribs
        self.vertabrae = vertabrae

    @staticmethod
    def empty():
        categories = [TraumaCategory.NOT_PRESENT] * 1
        categories += [LeftRight(TraumaCategory.NOT_PRESENT, TraumaCategory.NOT_PRESENT)] * 8
        categories += [TraumaCategory.NOT_PRESENT] * 2
        return Trauma(*categories)

    def to_pd_data_frame(self, index):
        d = {
            'id': pd.Series([index]),
        }
        for l in ('clavicle', 'scapula', 'humerus', 'ulna', 'radius', 'femur', 'tibia', 'fibula'):
            val = getattr(self, l)
            if val is None:
                continue
            if val.left is not None:
                d[f'{l}_left_cat'] = pd.Series([val.left.name],  copy=True, dtype=TraumaCategory.dtype())  # noqa: E241
                d[f'{l}_left_val'] = pd.Series([val.left.value], copy=True, dtype='Int64')
            if val.right is not None:
                d[f'{l}_right_cat'] = pd.Series([val.right.name],  copy=True, dtype=TraumaCategory.dtype())  # noqa: E241
                d[f'{l}_right_val'] = pd.Series([val.right.value], copy=True, dtype='Int64')
            if val.avg() is not None:
                d[f'{l}_avg_cat'] = pd.Series([val.avg().name],  copy=True, dtype=TraumaCategory.dtype())  # noqa: E241
                d[f'{l}_avg_val'] = pd.Series([val.avg().value], copy=True, dtype='Int64')

        for l in ('facial_bones', 'ribs', 'vertabrae'):
            val = getattr(self, l)
            if val is None:
                continue
            d[f'{l}_cat'] = pd.Series([val.name],  copy=True, dtype=TraumaCategory.dtype())  # noqa: E241
            d[f'{l}_val'] = pd.Series([val.value], copy=True, dtype='Int64')

        return pd.DataFrame.from_dict(d).set_index('id')


if __name__ == "__main__":
    raise RuntimeError('No main available')
