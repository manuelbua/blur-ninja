"""

"""
# coding=utf-8
from __future__ import print_function
from builtins import range
#
from blurninja.binom import binom


def kernel_binom(taps, expand_by=0, reduce_by=0):
    """

    :param taps:
    :type taps: int
    :param expand_by:
    :type expand_by: int
    :param reduce_by:
    :type reduce_by: int
    :return: {'weigths': List[float], 'offsets': List[int]}
    :rtype: dict
    """
    """Compute discrete weights and factors
    """

    row = taps - 1 + (expand_by << 1)
    coeffs_count = row + 1
    radius = taps >> 1

    # sanity check, avoid duped coefficients at center
    if coeffs_count & 1 == 0:
        ValueError("Duped coefficients at center")

    # compute total weight
    # https://en.wikipedia.org/wiki/Power_of_two
    # TODO: seems to be not optimal ...
    total = float(1 << row) - sum([binom(row, x) * 2 for x in range(reduce_by)])

    # compute final weights
    return dict(
        weights=[binom(row, x) / total for x in range(reduce_by + radius, reduce_by - 1, -1)],
        offsets=range(radius + 1)
    )


def kernel_binom_linear(discrete_data):
    """Compute linearly interpolated weights and factors

    :param discrete_data: {'weigths': List[float], 'offsets': List[int]}
    :type discrete_data: dict
    :return:
    :rtype: dict
    """
    if discrete_data is None:
        ValueError("Can't perform linear reduction pass, no input data")

    wd = discrete_data['weights']
    od = discrete_data['offsets']

    w_count = len(wd)

    # sanity checks
    pairs = w_count - 1
    if w_count & 1 == 0:
        raise ValueError("Duped coefficients at center")

    if pairs % 2 != 0:
        raise ValueError("Can't perform bilinear reduction on non-paired texels")

    weights = [wd[0]] + [wd[x] + wd[x + 1] for x in range(1, w_count - 1, 2)]
    # TODO: non optimal, performed double computations
    offsets = [0] + [(od[x] * wd[x] + od[x + 1] * wd[x + 1]) / weights[i + 1]
                     for i, x in enumerate(range(1, w_count - 1, 2))]

    return dict(weights=weights, offsets=offsets)
