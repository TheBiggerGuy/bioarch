#!/usr/bin/env python


import unittest


from .context import Context


class ContextTest(unittest.TestCase):
    def test_to_pd_data_frame(self):
        context = Context({'spear': True, 'pots': 2})

        df = context.to_pd_data_frame('id1', prefix='context_')

        self.assertEqual(df.to_json(orient='records'), '[{"context_spear":true,"context_pots":2}]')


def main():
    unittest.main()


if __name__ == "__main__":
    main()
