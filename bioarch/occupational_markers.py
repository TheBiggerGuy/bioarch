#!/usr/bin/env python


import logging
from typing import Any, List, Union


import pandas as pd


from .left_right import LeftRight, Optional


logger = logging.getLogger(__name__)


class EnthesialMarker(object):
    """docstring for EnthesialMarker"""
    def __init__(self, value: Union[int, float], is_s: bool = False, is_oe: bool = False):
        self.value = float(value)  # 0-3 in 0.5 increments
        self.is_s = is_s  # 0.5-3 in 0.5 increments ie "s0.5"
        self.is_oe = is_oe  # 0.5-3 in 0.5 increments ie "oe0.5"

        if self.is_s and self.is_oe:
            raise ValueError('Can not be both "s" and "oe" EnthesialMarker')
        if self.is_s or self.is_oe:
            if self.value < 0.5 or self.value > 3:
                raise ValueError(f'Invalid EnthesialMarker value, s/oe should be within 0.5 to 3: {self.value}')
        else:
            if self.value < 0 or self.value > 3:
                raise ValueError(f'Invalid EnthesialMarker value, non s/oe should be within 0 to 3: {self.value}')
        if self.value % 0.5 != 0.0:
            raise ValueError(f'Invalid EnthesialMarker value, not a 0.5 increment: {self.value}')

    @staticmethod
    def parse(value: Any) -> Optional['EnthesialMarker']:
        if value is None:
            return None

        original_value = value
        is_s = False
        is_oe = False
        if isinstance(value, str):
            value = value.lower()
            if value.startswith('r'):
                value = value[1:]
            elif value.startswith('s'):
                is_s = True
                value = value[1:]
            elif value.startswith('oe'):  # TODO: double check logic
                is_oe = True
                value = value[2:]
            elif value.startswith('0e'):  # TODO: double check logic
                logger.warning('Bad EnthesialMarker: %s', value)
                is_oe = True
                value = value[2:]
            elif value.startswith('eo'):  # TODO: double check logic
                logger.warning('Bad EnthesialMarker: %s', value)
                is_oe = True
                value = value[2:]
            elif value.startswith('o'):  # TODO: double check logic
                logger.warning('Bad EnthesialMarker: %s', value)
                is_oe = True
                value = value[1:]
            elif value.startswith('e'):  # TODO: double check logic
                logger.warning('Bad EnthesialMarker: %s', value)
                is_oe = True
                value = value[1:]
            try:
                value = float(value)
            except ValueError as e:
                raise ValueError(f'Unknown EnthesialMarker: "{original_value}"') from e

        if isinstance(value, int):
            value = float(value)

        if not isinstance(value, float):
            raise ValueError(f'Unknown EnthesialMarker: "{original_value}"')

        return EnthesialMarker(value, is_s=is_s, is_oe=is_oe)

    def as_num(self) -> float:
        val = self.value
        if self.is_oe:
            val += 6.0
        if self.is_s:
            val += 3.0
        return val

    @staticmethod
    def avg(left: Optional['EnthesialMarker'], right: Optional['EnthesialMarker']) -> Optional['EnthesialMarker']:
        return left if right is None else right

    def __eq__(self, other: Any):
        if other is None:
            return False
        if type(other) != type(self):  # pylint: disable=C0123
            raise NotImplementedError
        return ((self.value, self.is_s, self.is_oe) == (other.value, other.is_s, other.is_oe))  # pylint: disable=C0325

    def __repr__(self):
        return f'{self.__class__.__name__}: {self}'

    def __str__(self):
        s = 's' if self.is_s else ''
        oe = 'oe' if self.is_oe else ''
        return f'{s}{oe}{self.value}'


class OccupationalMarkers(object):  # pylint: disable=R0902
    """docstring for OccupationalMarkers"""
    def __init__(self, c_trapezius: LeftRight[EnthesialMarker], c_o_deltiod: LeftRight[EnthesialMarker], c_o_pectoralis_major: LeftRight[EnthesialMarker], c_costoclaviclar_lig: LeftRight[EnthesialMarker], c_subcalvius: LeftRight[EnthesialMarker], c_conoid_lig: LeftRight[EnthesialMarker], c_trapezoid_lig: LeftRight[EnthesialMarker], s_pectoralis_minor: LeftRight[EnthesialMarker], s_serratus_anterior: LeftRight[EnthesialMarker], s_triceps_long_head: LeftRight[EnthesialMarker], s_trapezius: LeftRight[EnthesialMarker], h_subscapularis: LeftRight[EnthesialMarker], h_teres_major: LeftRight[EnthesialMarker], h_latissimus_dorsi: LeftRight[EnthesialMarker], h_pectoralis_major: LeftRight[EnthesialMarker], h_deltoid: LeftRight[EnthesialMarker], h_coracobrachialis: LeftRight[EnthesialMarker], h_supraspinatus: LeftRight[EnthesialMarker], h_infraspinatus: LeftRight[EnthesialMarker], h_teres_minor: LeftRight[EnthesialMarker], h_o_extensor: LeftRight[EnthesialMarker], h_o_flexor: LeftRight[EnthesialMarker], u_brachialis: LeftRight[EnthesialMarker], u_o_pronator_quadrataus: LeftRight[EnthesialMarker], u_triceps_brachii: LeftRight[EnthesialMarker], u_anconeus: LeftRight[EnthesialMarker], u_o_supinator: LeftRight[EnthesialMarker], r_biceps_brachii: LeftRight[EnthesialMarker], r_supinator: LeftRight[EnthesialMarker], r_pronator_teres: LeftRight[EnthesialMarker], r_pronator_quadratus: LeftRight[EnthesialMarker], r_brachoradialis: LeftRight[EnthesialMarker], f_gluteus_minimus: LeftRight[EnthesialMarker], f_gluteus_medius: LeftRight[EnthesialMarker], f_piriformus: LeftRight[EnthesialMarker], f_obturator_internus: LeftRight[EnthesialMarker], f_obturator_externus: LeftRight[EnthesialMarker], f_quadratis_femoris: LeftRight[EnthesialMarker], f_ilioposas: LeftRight[EnthesialMarker], f_gluteus_maximus: LeftRight[EnthesialMarker], f_pectineus: LeftRight[EnthesialMarker], f_o_vastus_medialis: LeftRight[EnthesialMarker], f_o_vastus_lateralis: LeftRight[EnthesialMarker], o_adductor_magnus: LeftRight[EnthesialMarker], f_o_gastrocnemius: LeftRight[EnthesialMarker], f_o_plantaris: LeftRight[EnthesialMarker], f_o_popliteus: LeftRight[EnthesialMarker], t_tensor_fascia_latae: LeftRight[EnthesialMarker], t_quadriceps: LeftRight[EnthesialMarker], t_sartorius: LeftRight[EnthesialMarker], t_gracilis: LeftRight[EnthesialMarker], t_semitendinosus: LeftRight[EnthesialMarker], t_o_tibialus_anterior: LeftRight[EnthesialMarker], t_biceps_femoris: LeftRight[EnthesialMarker], t_semimembranosus: LeftRight[EnthesialMarker], t_popliteus: LeftRight[EnthesialMarker], t_o_soleus: LeftRight[EnthesialMarker], t_o_tibialis_posterior: LeftRight[EnthesialMarker], t_o_flexor_digitorium: LeftRight[EnthesialMarker], f_biceps_femoris: LeftRight[EnthesialMarker], f_o_extensor_muscles: LeftRight[EnthesialMarker], f_o_flexor_muscles: LeftRight[EnthesialMarker], f_o_peroneus_longus: LeftRight[EnthesialMarker], f_o_peronus_brevis: LeftRight[EnthesialMarker], f_o_soleus: LeftRight[EnthesialMarker], p_quadriceps: LeftRight[EnthesialMarker], c_achilles: LeftRight[EnthesialMarker]):
        self.c_trapezius = c_trapezius
        self.c_o_deltiod = c_o_deltiod
        self.c_o_pectoralis_major = c_o_pectoralis_major
        self.c_costoclaviclar_lig = c_costoclaviclar_lig
        self.c_subcalvius = c_subcalvius
        self.c_conoid_lig = c_conoid_lig
        self.c_trapezoid_lig = c_trapezoid_lig
        self.s_pectoralis_minor = s_pectoralis_minor
        self.s_serratus_anterior = s_serratus_anterior
        self.s_triceps_long_head = s_triceps_long_head
        self.s_trapezius = s_trapezius
        self.h_subscapularis = h_subscapularis
        self.h_teres_major = h_teres_major
        self.h_latissimus_dorsi = h_latissimus_dorsi
        self.h_pectoralis_major = h_pectoralis_major
        self.h_deltoid = h_deltoid
        self.h_coracobrachialis = h_coracobrachialis
        self.h_supraspinatus = h_supraspinatus
        self.h_infraspinatus = h_infraspinatus
        self.h_teres_minor = h_teres_minor
        self.h_o_extensor = h_o_extensor
        self.h_o_flexor = h_o_flexor
        self.u_brachialis = u_brachialis
        self.u_o_pronator_quadrataus = u_o_pronator_quadrataus
        self.u_triceps_brachii = u_triceps_brachii
        self.u_anconeus = u_anconeus
        self.u_o_supinator = u_o_supinator
        self.r_biceps_brachii = r_biceps_brachii
        self.r_supinator = r_supinator
        self.r_pronator_teres = r_pronator_teres
        self.r_pronator_quadratus = r_pronator_quadratus
        self.r_brachoradialis = r_brachoradialis
        self.f_gluteus_minimus = f_gluteus_minimus
        self.f_gluteus_medius = f_gluteus_medius
        self.f_piriformus = f_piriformus
        self.f_obturator_internus = f_obturator_internus
        self.f_obturator_externus = f_obturator_externus
        self.f_quadratis_femoris = f_quadratis_femoris
        self.f_ilioposas = f_ilioposas
        self.f_gluteus_maximus = f_gluteus_maximus
        self.f_pectineus = f_pectineus
        self.f_o_vastus_medialis = f_o_vastus_medialis
        self.f_o_vastus_lateralis = f_o_vastus_lateralis
        self.o_adductor_magnus = o_adductor_magnus
        self.f_o_gastrocnemius = f_o_gastrocnemius
        self.f_o_plantaris = f_o_plantaris
        self.f_o_popliteus = f_o_popliteus
        self.t_tensor_fascia_latae = t_tensor_fascia_latae
        self.t_quadriceps = t_quadriceps
        self.t_sartorius = t_sartorius
        self.t_gracilis = t_gracilis
        self.t_semitendinosus = t_semitendinosus
        self.t_o_tibialus_anterior = t_o_tibialus_anterior
        self.t_biceps_femoris = t_biceps_femoris
        self.t_semimembranosus = t_semimembranosus
        self.t_popliteus = t_popliteus
        self.t_o_soleus = t_o_soleus
        self.t_o_tibialis_posterior = t_o_tibialis_posterior
        self.t_o_flexor_digitorium = t_o_flexor_digitorium
        self.f_biceps_femoris = f_biceps_femoris
        self.f_o_extensor_muscles = f_o_extensor_muscles
        self.f_o_flexor_muscles = f_o_flexor_muscles
        self.f_o_peroneus_longus = f_o_peroneus_longus
        self.f_o_peronus_brevis = f_o_peronus_brevis
        self.f_o_soleus = f_o_soleus
        self.p_quadriceps = p_quadriceps
        self.c_achilles = c_achilles

    @staticmethod
    def empty() -> 'OccupationalMarkers':
        markers: List[LeftRight[EnthesialMarker]] = [LeftRight(None, None)] * 67
        return OccupationalMarkers(*markers)

    def to_pd_series(self, prefix: str = '') -> pd.Series:
        labels = []
        values = []
        for key, value in self.__dict__.items():
            labels.append(f'{prefix}{key}_left')
            values.append(value.left)
            labels.append(f'{prefix}{key}_right')
            values.append(value.right)
            labels.append(f'{prefix}{key}_avg')
            values.append(value.avg())
        s = pd.Series(values, index=labels, copy=True)

        subset = pd.Series([v.as_num() for k, v in s.items() if v is not None and k.endswith('_avg')])
        s = s.append(pd.Series([subset.mean(skipna=True)], index=[f'{prefix}mean']))
        s = s.append(pd.Series([subset.max(skipna=True)], index=[f'{prefix}max']))
        s = s.append(pd.Series([subset.min(skipna=True)], index=[f'{prefix}min']))
        s = s.append(pd.Series([subset.count()], index=[f'{prefix}count']))
        return s


if __name__ == "__main__":
    raise RuntimeError('No main available')
