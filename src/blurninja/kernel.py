"""

"""
# coding=utf-8
from __future__ import print_function
from builtins import range
import math
#
from blurninja.binom import binom


def kernel_binom(taps, expand_by=0, reduce_by=0):
    """Compute discrete weights and factors
    """

    row = taps - 1 + expand_by * 2
    coeffs_count = row + 1
    radius = int(taps / 2)

    # sanity check, avoid duped coefficients at center
    if coeffs_count & 1 == 0:
        print("ERR: duped coefficients at center")
        return None

    # compute total weight
    total = math.pow(2, row) - sum(map(lambda x: binom(row, x) * 2, range(reduce_by)))

    # compute final weights
    weights = [binom(row, x) / total
               for x in range(reduce_by + radius, reduce_by - 1, -1)]
    offsets = range(radius + 1)

    return dict(weights=weights, offsets=offsets)


def kernel_binom_linear(discrete_data):
    """Compute linearly interpolated weights and factors
    """
    if discrete_data is None:
        print("ERR: can't perform linear reduction pass, no input data")
        return None

    wd = discrete_data['weights']
    od = discrete_data['offsets']

    w_count = len(wd)
    pairs = int(w_count - 1)

    # sanity checks
    if w_count & 1 == 0:
        print("ERR: duped coefficients at center")
        return None

    if pairs % 2 > 0:
        print("ERR: can't perform bilinear reduction on non-paired texels")
        return None

    weights = [wd[0]]
    weights.extend([wd[x] + wd[x + 1] for x in range(1, w_count - 1, 2)])

    offsets = [0]
    offsets.extend([(od[x] * wd[x] + od[x + 1] * wd[x + 1]) / weights[i + 1]
                    for i, x in enumerate(range(1, w_count - 1, 2))])

    return dict(weights=weights, offsets=offsets)
