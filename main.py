#!/usr/bin/env python2
# coding=utf-8

"""
Comments
"""

__license__ = """
"""

__version__ = "0.0.1"
__author__ = "manuel"

import sys
import math
import argparse


# FYI, efficient gaussian blur is described in great detail here:
# http://rastergrid.com/blog/2010/09/efficient-gaussian-blur-with-linear
# -sampling/

def binom(row_index, column_index=None):
    if column_index is None:
        row = []
        columns = row_index + 1
        for c in xrange(columns):
            row.append(
                math.factorial(row_index) / (
                    math.factorial(row_index - c) * math.factorial(c)
                )
            )

        return row

    return math.factorial(row_index) / (
        math.factorial(row_index - column_index) * math.factorial(column_index)
    )


def draw_binom(rows_count):
    length = len(str(binom(rows_count - 1)))
    for i in xrange(rows_count):
        print ("{:^" + str(length) + "}").format(str(binom(i)))


def kernel_binom(taps, expand_by=0, reduce_by=0):
    row = taps - 1 + expand_by * 2
    coeffs_count = row + 1
    radius = int(taps / 2)

    # sanity check, avoid duped coefficients at center
    if coeffs_count & 1 == 0:
        print "ERR: duped coefficients at center"
        return None

    # compute total weight
    s = lambda x: binom(row, x) * 2
    total = math.pow(2, row) - sum(map(s, xrange(reduce_by)))

    # compute final weights
    weights = [binom(row, x) / total
               for x in xrange(reduce_by + radius, reduce_by - 1, -1)]
    offsets = range(radius + 1)

    return dict(weights=weights, offsets=offsets)


def kernel_binom_linear(taps, expand_by=0, reduce_by=0):
    res = kernel_binom(taps, expand_by, reduce_by)
    if res is None:
        print "ERR: previous error"
        return None

    w = res['weights']
    o = res['offsets']
    w_count = len(res['weights'])
    pairs = int(w_count - 1)

    # sanity checks
    if w_count % 2 == 0:
        print "ERR: duped coefficients at center"
        return None

    if pairs % 2 > 0:
        print "ERR: can't perform bilinear reduction on non-paired texels"
        return None

    weights = list()
    weights.append(w[0])
    weights.extend([w[x] + w[x + 1] for x in xrange(1, w_count - 1, 2)])

    offsets = list()
    offsets.append(0)
    offsets.extend([(o[x] * w[x] + o[x + 1] * w[x + 1]) / weights[i + 1]
                    for i, x in enumerate(xrange(1, w_count - 1, 2))])

    res['weights'] = weights
    res['offsets'] = offsets
    return res


def main():
    res = None
    taps = exp = red = 0
    linear = False

    if len(sys.argv) > 1:
        parser = argparse.ArgumentParser(description="Process some data")
        parser.add_argument(
            "taps", default=5, type=int,
            help="Specify the number of taps (kernel size)"
        )

        parser.add_argument(
            "--expand", default=0, type=int,
            help="How much to expand the tap count (eliminate outermost "
                 "coefficients)"
        )

        parser.add_argument(
            "--reduce", default=0, type=int,
            help="How many taps to discard at borders (eliminate outermost "
                 "coefficients)"
        )

        parser.add_argument(
            "--linear", default=0, type=int,
            help="Uses linear sampling to compute weights and offsets"
        )

        args = parser.parse_args()

        taps = args.taps
        exp = args.expand
        red = args.reduce
        linear = args.linear

    else:
        # debug

        taps = 5
        exp = 2
        red = 2
        linear = False

    print "Computing a %(taps)sx%(taps)s kernel (+%(exp)s/-%(red)s)" \
          "%(desc)s" % \
          {'taps': taps, 'exp': exp * 2, 'red': red * 2,
           'desc': ", linear sampling" if linear else ""}

    if linear:
        res = kernel_binom_linear(taps, exp, red)
    else:
        res = kernel_binom(taps, exp, red)

    if res is not None:
        radius = int(taps / 2)
        print "Radius:", str(radius), "(+1)"
        print "weights:", ["{:.6f}".format(x) for x in res["weights"]]
        print "offsets:", ["{:.6f}".format(x) for x in res["offsets"]]


if __name__ == "__main__":
    main()
