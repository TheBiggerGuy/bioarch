#!/usr/bin/env python


import sys


from .age import AgeCategory, EstimatedAge
from .individual import AgeSexStature, BurialInfo, Individual, LongBoneMeasurement, OsteologicalSex
from .left_right import LeftRight
from .mouth import Mouth, Tooth
from .occupational_markers import EnthesialMarker, OccupationalMarkers
from .sex import Sex


if sys.version_info < (3, 7):
    print('ERROR: Only Python 3.7 and above is supported')
    sys.exit(-1)


__title__ = 'bioarch'
__version__ = '0.0.7'
__author__ = 'Guy Taylor'

__all__ = ['AgeCategory', 'EstimatedAge'] + ['AgeSexStature', 'BurialInfo', 'Individual', 'LongBoneMeasurement', 'OsteologicalSex'] + \
          ['EnthesialMarker', 'OccupationalMarkers'] + ['LeftRight'] + ['Mouth', 'Tooth'] + ['Sex']
