#!/usr/bin/env python


import unittest


from .trauma import Trauma


class TraumaTest(unittest.TestCase):
    def test_to_pd_data_frame(self):
        trauma = Trauma.empty()

        df = trauma.to_pd_data_frame('id1')

        self.assertEqual(df.to_json(orient='records'), '[{"clavicle_left_cat":"NOT_PRESENT","clavicle_left_val":-1,"clavicle_right_cat":"NOT_PRESENT","clavicle_right_val":-1,"clavicle_avg_cat":"NOT_PRESENT","clavicle_avg_val":-1,"scapula_left_cat":"NOT_PRESENT","scapula_left_val":-1,"scapula_right_cat":"NOT_PRESENT","scapula_right_val":-1,"scapula_avg_cat":"NOT_PRESENT","scapula_avg_val":-1,"humerus_left_cat":"NOT_PRESENT","humerus_left_val":-1,"humerus_right_cat":"NOT_PRESENT","humerus_right_val":-1,"humerus_avg_cat":"NOT_PRESENT","humerus_avg_val":-1,"ulna_left_cat":"NOT_PRESENT","ulna_left_val":-1,"ulna_right_cat":"NOT_PRESENT","ulna_right_val":-1,"ulna_avg_cat":"NOT_PRESENT","ulna_avg_val":-1,"radius_left_cat":"NOT_PRESENT","radius_left_val":-1,"radius_right_cat":"NOT_PRESENT","radius_right_val":-1,"radius_avg_cat":"NOT_PRESENT","radius_avg_val":-1,"femur_left_cat":"NOT_PRESENT","femur_left_val":-1,"femur_right_cat":"NOT_PRESENT","femur_right_val":-1,"femur_avg_cat":"NOT_PRESENT","femur_avg_val":-1,"tibia_left_cat":"NOT_PRESENT","tibia_left_val":-1,"tibia_right_cat":"NOT_PRESENT","tibia_right_val":-1,"tibia_avg_cat":"NOT_PRESENT","tibia_avg_val":-1,"fibula_left_cat":"NOT_PRESENT","fibula_left_val":-1,"fibula_right_cat":"NOT_PRESENT","fibula_right_val":-1,"fibula_avg_cat":"NOT_PRESENT","fibula_avg_val":-1,"facial_bones_cat":"NOT_PRESENT","facial_bones_val":-1,"ribs_cat":"NOT_PRESENT","ribs_val":-1,"vertabrae_cat":"NOT_PRESENT","vertabrae_val":-1}]')


def main():
    unittest.main()


if __name__ == "__main__":
    main()
