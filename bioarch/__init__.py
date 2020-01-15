#!/usr/bin/env python


import sys


from .age import AgeCategory, EstimatedAge
from .context import Context
from .individual import AgeSexStature, BurialInfo, Individual, LongBoneMeasurement, OsteologicalSex
from .joints import JointCondition, Joints
from .left_right import LeftRight
from .mouth import Mouth, Tooth
from .occupational_markers import EnthesialMarker, OccupationalMarkers
from .sex import Sex
from .trauma import Trauma, TraumaCategory


if sys.version_info < (3, 7):
    print('ERROR: Only Python 3.7 and above is supported')
    sys.exit(-1)


__title__ = 'bioarch'
__version__ = '0.0.27'
__author__ = 'Guy Taylor'

__all__ = ['AgeCategory', 'EstimatedAge'] + ['Context'] + ['AgeSexStature', 'BurialInfo', 'Individual', 'LongBoneMeasurement', 'OsteologicalSex'] + \
          ['JointCondition', 'Joints'] + ['EnthesialMarker', 'OccupationalMarkers'] + ['LeftRight'] + ['Mouth', 'Tooth'] + ['Sex'] + ['Trauma', 'TraumaCategory']
