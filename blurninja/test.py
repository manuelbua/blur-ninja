#!/usr/bin/env python2
# coding=utf-8

"""
Unittest for blurninja
"""

import unittest
from blurninja.kernel import kernel_binom, kernel_binom_linear


class TestDiscrete(unittest.TestCase):
    def _compare(self, a, b):
        for i, w in enumerate(a['weights']):
            self.assertAlmostEqual(b['weights'][i], w, 6)

        for i, o in enumerate(a['offsets']):
            self.assertEqual(b['offsets'][i], o)

    def _compare_linear(self, a, b):
        for i, w in enumerate(a['weights']):
            self.assertAlmostEqual(b['weights'][i], w, 6)

        for i, o in enumerate(a['offsets']):
            self.assertAlmostEqual(b['offsets'][i], o, 6)

    def test_3x3(self):
        res = {'weights': [0.5, 0.25],
               'offsets': [0, 1]}
        this = kernel_binom(3, 0, 0)
        self._compare(res, this)

    def test_5x5(self):
        res = {'weights': [0.375, 0.25, 0.0625],
               'offsets': [0, 1, 2]}
        this = kernel_binom(5, 0, 0)
        self._compare(res, this)

    def test_5x5_linear(self):
        res = {'weights': [0.375, 0.3125],
               'offsets': [0, 1.2]}

        this = kernel_binom_linear(kernel_binom(5, 0, 0))
        self._compare_linear(res, this)

    def test_9x9_reduce(self):
        res = {
            'weights': [0.2270270, 0.1945945, 0.1216216, 0.0540540, 0.0162162],
            'offsets': [0, 1, 2, 3, 4]}
        this = kernel_binom(9, 2, 2)
        self._compare(res, this)

    def test_9x9_linear_reduce(self):
        res = {'weights': [0.2270270, 0.3162162, 0.0702702],
               'offsets': [0, 1.3846153, 3.2307692]}
        this = kernel_binom_linear(kernel_binom(9, 2, 2))
        self._compare_linear(res, this)


if __name__ == "__main__":
    unittest.main()
