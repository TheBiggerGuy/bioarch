#!/usr/bin/env python


import functools
from typing import Optional


import pandas as pd


from .age import EstimatedAge
from .context import Context
from .joints import Joints
from .left_right import LeftRight
from .mouth import Mouth
from .occupational_markers import OccupationalMarkers
from .sex import Sex
from .trauma import Trauma


# Notes:
#  * https://www.archaeologists.net/sites/default/files/ifa_paper_7.pdf


class BurialInfo(object):
    """docstring for BurialInfo"""
    def __init__(self, site_name: str, site_id: str):
        if site_name is None or site_id is None:
            raise ValueError('site_name and site_id required')
        if site_name == '' or site_id == '':
            raise ValueError('site_name and site_id required')
        self.name = site_name
        self.id = site_id

    def to_pd_series(self, prefix=''):
        labels = [f'{prefix}{label}' for label in ['name', 'id']]
        return pd.Series([self.name, self.id], index=labels, copy=True)


@functools.total_ordering
class LongBoneMeasurement(object):
    """docstring for LongBoneMeasurement"""

    def __init__(self, _max: Optional[float], bi: Optional[float], head: Optional[float], distal: Optional[float]):
        self.max = _max
        self.bi = bi
        self.head = head
        self.distal = distal

    @staticmethod
    def empty():
        return LongBoneMeasurement(None, None, None, None)

    @staticmethod
    def empty_lr():
        return LeftRight(LongBoneMeasurement.empty(), LongBoneMeasurement.empty())

    def to_pd_series(self, prefix=''):
        labels = [f'{prefix}{label}' for label in ['max', 'bi', 'head', 'distal']]
        return pd.Series([self.max, self.bi, self.head, self.distal], index=labels, copy=True)

    def __eq__(self, other):
        if type(other) != type(self):  # pylint: disable=C0123
            raise NotImplementedError
        return ((self.max, self.bi, self.head, self.distal) == (other.max, other.bi, other.head, other.distal))  # pylint: disable=C0325

    def __lt__(self, other):
        if type(other) != type(self):  # pylint: disable=C0123
            raise NotImplementedError
        return ((self.max, self.bi, self.head, self.distal) < (other.max, other.bi, other.head, other.distal))  # pylint: disable=C0325


class OsteologicalSex(object):
    """docstring for OsteologicalSex"""
    def __init__(self, pelvic: Optional[Sex], cranium: Optional[Sex], combined: Optional[Sex]):
        self.pelvic = pelvic
        self.cranium = cranium
        self.combined = combined

    @staticmethod
    def empty():
        return OsteologicalSex(None, None, None)

    def to_pd_data_frame(self, index):
        d = {
            'id': pd.Series([index]),
        }
        for l in ('pelvic', 'cranium', 'combined'):
            val = getattr(self, l)
            d[f'{l}_cat'] = pd.Series([val.name if val else None],  copy=True, dtype=Sex.dtype())  # noqa: E241
            d[f'{l}_val'] = pd.Series([val.value if val else None], copy=True, dtype='Int64')
            val_bin = val.as_bin() if val else None
            d[f'{l}_bin_cat'] = pd.Series([val_bin.name if val_bin else None],  copy=True, dtype=Sex.dtype())  # noqa: E241
            d[f'{l}_bin_val'] = pd.Series([val_bin.value if val_bin else None], copy=True, dtype='Int64')

        return pd.DataFrame.from_dict(d).set_index('id')


class AgeSexStature(object):
    """docstring for AgeSexStature"""

    __slots__ = ['osteological_sex', 'age', 'femur', 'humerus', 'tibia', 'stature', 'body_mass']

    def __init__(self, osteological_sex: OsteologicalSex, age: EstimatedAge, femur: LongBoneMeasurement, humerus: LongBoneMeasurement, tibia: LongBoneMeasurement, stature: Optional[str], body_mass: Optional[str]):
        # Sex
        self.osteological_sex = osteological_sex
        # Age
        self.age = age
        # Long bones
        self.femur = femur
        self.humerus = humerus
        self.tibia = tibia
        # Other
        self.stature = stature
        self.body_mass = body_mass

    @staticmethod
    def empty():
        return AgeSexStature(OsteologicalSex.empty(), EstimatedAge.empty(), LongBoneMeasurement.empty_lr(), LongBoneMeasurement.empty_lr(), LongBoneMeasurement.empty_lr(), None, None)

    def to_pd_data_frame(self, index):
        data = {
            'id': pd.Series([index]),
            'stature': pd.Series([self.stature]),
            'body_mass': pd.Series([self.body_mass]),
        }
        df = pd.DataFrame.from_dict(data).set_index('id')

        s = pd.Series([])
        for bone in ('femur', 'humerus', 'tibia'):
            lr_val = getattr(self, bone)
            s = s.append(lr_val.left.to_pd_series(prefix=f'{bone}_left_'))
            s = s.append(lr_val.right.to_pd_series(prefix=f'{bone}_right_'))
            s = s.append(lr_val.avg().to_pd_series(prefix=f'{bone}_avg_'))
        long_bones = pd.DataFrame.from_dict({index: s}, orient='index')

        age = self.age.to_pd_data_frame(index).add_prefix(f'age_').rename(columns={f'age_id': 'id'})
        oss = self.osteological_sex.to_pd_data_frame(index).add_prefix(f'osteological_sex_').rename(columns={f'osteological_sex_id': 'id'})

        return df.join(long_bones, on='id', how='outer') \
                 .join(age, on='id', how='outer') \
                 .join(oss, on='id', how='outer')


class Individual(object):
    """docstring for Individual"""
    def __init__(self, _id: str, site: BurialInfo, age_sex_stature: AgeSexStature, mouth: Mouth, occupational_markers: OccupationalMarkers, joints: Joints, trauma: Trauma, context: Context):
        self.id = _id
        self.site = site
        self.age_sex_stature = age_sex_stature
        self.mouth = mouth
        self.occupational_markers = occupational_markers
        self.joints = joints
        self.trauma = trauma
        self.context = context

    def to_pd_data_frame(self):
        s = pd.Series([self.id], index=['id'], copy=True)
        s = s.append(self.site.to_pd_series(prefix='site_'))
        s = s.append(self.mouth.to_pd_series(prefix='mouth_'))
        s = s.append(self.joints.to_pd_series(prefix='joints_'))

        ass_df = self.age_sex_stature.to_pd_data_frame(self.id).add_prefix('ass_').rename(columns={f'ass_id': 'id'})
        om_df = self.occupational_markers.to_pd_data_frame(self.id).add_prefix('om_').rename(columns={f'om_id': 'id'})
        trauma_df = self.trauma.to_pd_data_frame(self.id).add_prefix('trauma_').rename(columns={f'trauma_id': 'id'})
        context_df = self.context.to_pd_data_frame(self.id).add_prefix('context_').rename(columns={f'context_id': 'id'})

        df = pd.DataFrame.from_dict({self.id: s}, orient='index')
        return df.join(ass_df, on='id', how='outer') \
                 .join(om_df, on='id', how='outer') \
                 .join(trauma_df, on='id', how='outer') \
                 .join(context_df, on='id', how='outer')


if __name__ == "__main__":
    raise RuntimeError('No main available')
