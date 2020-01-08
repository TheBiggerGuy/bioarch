#!/usr/bin/env python


from typing import Dict, Optional, Union


import pandas as pd


class Context(object):
    """docstring for Context"""

    def __init__(self, tags: Dict[str, Optional[Union[str, int, bool, float]]]):
        self.tags = tags

    @staticmethod
    def empty():
        return Context({})

    def to_pd_data_frame(self, index, prefix=''):
        labels = [f'{prefix}{label}' for label in self.tags.keys()]
        s = pd.Series([val for val in self.tags.values()], index=labels, copy=True)  # pylint: disable=R1721

        return pd.DataFrame.from_dict({index: s}, orient='index')


if __name__ == "__main__":
    raise RuntimeError('No main available')
