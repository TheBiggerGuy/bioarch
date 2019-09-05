#!/usr/bin/env python


import enum
from enum import Enum
import functools
import logging
from typing import Any, cast, Optional


from ensure import ensure_annotations
import pandas as pd


logger = logging.getLogger(__name__)


class Context(object):
    """docstring for Context"""

    @ensure_annotations
    def __init__(self, tags):
        self.tags = tags

    @staticmethod
    def empty():
        return Context({})

    def to_pd_data_frame(self, index, prefix=''):
        labels = [f'{prefix}{label}' for label in self.tags.keys()]
        s = pd.Series([val for val in self.tags.values()], index=labels, copy=True)

        return pd.DataFrame.from_dict({index: s}, orient='index')


if __name__ == "__main__":
    raise RuntimeError('No main available')
