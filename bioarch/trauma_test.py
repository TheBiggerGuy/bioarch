#!/usr/bin/env python


import unittest


from .left_right import LeftRight
from .trauma import Trauma, TraumaCategory


class TraumaCategoryTest(unittest.TestCase):
    def test_parse(self):
        self.assertEqual(TraumaCategory.parse('NA'), TraumaCategory.NOT_PRESENT)
        self.assertEqual(TraumaCategory.parse('-1'), TraumaCategory.NOT_PRESENT)
        self.assertEqual(TraumaCategory.parse('0.5'), TraumaCategory.PARTIAL_BONE)
        self.assertEqual(TraumaCategory.parse('1'), TraumaCategory.NORMAL)
        self.assertEqual(TraumaCategory.parse('2'), TraumaCategory.INFECTION)
        self.assertEqual(TraumaCategory.parse('3'), TraumaCategory.FRACTURE)
        self.assertEqual(TraumaCategory.parse('4'), TraumaCategory.UNHEALED_FRACTURE)
        self.assertEqual(TraumaCategory.parse('5'), TraumaCategory.CRIBA)
        self.assertEqual(TraumaCategory.parse('6'), TraumaCategory.BLUNT_FORCE_TRAUMA)
        self.assertEqual(TraumaCategory.parse('7'), TraumaCategory.SHARP_FORCE_TRAUMA)
        self.assertEqual(TraumaCategory.parse('8'), TraumaCategory.TREPONATION)
        self.assertEqual(TraumaCategory.parse('9'), TraumaCategory.UNFUSED)
        self.assertEqual(TraumaCategory.parse('10'), TraumaCategory.BONY_GROWTH)
        self.assertEqual(TraumaCategory.parse('11'), TraumaCategory.FUSED)
        self.assertEqual(TraumaCategory.parse('12'), TraumaCategory.OSTEOCHONDRITIS_DESSICANS)

        self.assertEqual(TraumaCategory.parse('na'), TraumaCategory.parse('NA'))
        self.assertEqual(TraumaCategory.parse('FRACTURE'), TraumaCategory.parse('fracture'))
        self.assertEqual(TraumaCategory.parse('FRACTURE'), TraumaCategory.FRACTURE)
        self.assertEqual(TraumaCategory.parse(None), None)
        self.assertEqual(TraumaCategory.parse(TraumaCategory.FRACTURE), TraumaCategory.FRACTURE)

    def test_avg(self):
        self.assertEqual(TraumaCategory.avg(TraumaCategory.NOT_PRESENT, TraumaCategory.NOT_PRESENT), TraumaCategory.NOT_PRESENT)

        self.assertEqual(TraumaCategory.avg(TraumaCategory.NOT_PRESENT, TraumaCategory.PARTIAL_BONE), TraumaCategory.PARTIAL_BONE)
        self.assertEqual(TraumaCategory.avg(TraumaCategory.PARTIAL_BONE, TraumaCategory.NOT_PRESENT), TraumaCategory.PARTIAL_BONE)

        self.assertEqual(TraumaCategory.avg(TraumaCategory.PARTIAL_BONE, TraumaCategory.PARTIAL_BONE), TraumaCategory.PARTIAL_BONE)

        with self.assertRaises(NotImplementedError):
            TraumaCategory.avg(TraumaCategory.PARTIAL_BONE, TraumaCategory.NORMAL)


class TraumaTest(unittest.TestCase):
    def test_to_pd_data_frame(self):
        trauma = Trauma.empty()
        trauma.facial_bones = TraumaCategory.INFECTION
        trauma.clavicle = LeftRight(TraumaCategory.NOT_PRESENT, TraumaCategory.NORMAL)
        trauma.scapula = LeftRight(TraumaCategory.NORMAL, TraumaCategory.NOT_PRESENT)
        trauma.humerus = LeftRight(TraumaCategory.NORMAL, TraumaCategory.NORMAL)
        trauma.ulna = LeftRight(TraumaCategory.NORMAL, TraumaCategory.INFECTION)

        df = trauma.to_pd_data_frame('id1')

        self.assertEqual(df.to_json(orient='records'), '[{"clavicle_left_cat":"NOT_PRESENT","clavicle_left_val":-1,"clavicle_right_cat":"NORMAL","clavicle_right_val":1,"clavicle_avg_cat":"NORMAL","clavicle_avg_val":1,"scapula_left_cat":"NORMAL","scapula_left_val":1,"scapula_right_cat":"NOT_PRESENT","scapula_right_val":-1,"scapula_avg_cat":"NORMAL","scapula_avg_val":1,"humerus_left_cat":"NORMAL","humerus_left_val":1,"humerus_right_cat":"NORMAL","humerus_right_val":1,"humerus_avg_cat":"NORMAL","humerus_avg_val":1,"ulna_left_cat":"NORMAL","ulna_left_val":1,"ulna_right_cat":"INFECTION","ulna_right_val":2,"radius_left_cat":"NOT_PRESENT","radius_left_val":-1,"radius_right_cat":"NOT_PRESENT","radius_right_val":-1,"radius_avg_cat":"NOT_PRESENT","radius_avg_val":-1,"femur_left_cat":"NOT_PRESENT","femur_left_val":-1,"femur_right_cat":"NOT_PRESENT","femur_right_val":-1,"femur_avg_cat":"NOT_PRESENT","femur_avg_val":-1,"tibia_left_cat":"NOT_PRESENT","tibia_left_val":-1,"tibia_right_cat":"NOT_PRESENT","tibia_right_val":-1,"tibia_avg_cat":"NOT_PRESENT","tibia_avg_val":-1,"fibula_left_cat":"NOT_PRESENT","fibula_left_val":-1,"fibula_right_cat":"NOT_PRESENT","fibula_right_val":-1,"fibula_avg_cat":"NOT_PRESENT","fibula_avg_val":-1,"facial_bones_cat":"INFECTION","facial_bones_val":2,"ribs_cat":"NOT_PRESENT","ribs_val":-1,"vertabrae_cat":"NOT_PRESENT","vertabrae_val":-1}]')


def main():
    unittest.main()


if __name__ == "__main__":
    main()
