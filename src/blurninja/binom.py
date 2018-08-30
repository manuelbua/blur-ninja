# coding=utf-8
from builtins import range
import math


def binom(row_index, column_index=None):
    """
    Computes the n-th coefficient or an entire row from Pascal's triangle
    binomial coefficients.
    """
    if column_index is None:
        return [
            math.factorial(row_index) / (math.factorial(row_index - c) * math.factorial(c))
            for c in range(row_index + 1)
        ]

    return math.factorial(row_index) / (math.factorial(row_index - column_index) * math.factorial(column_index))


def draw_binom(row):
    """
    Draws an ugly, ascii-based Pascal triangle up to the specified
    row (included)
    """
    length = len(str(binom(row)))
    for i in range(row):
        print("{:^" + str(length) + "}").format(str(binom(i)))
