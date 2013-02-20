#!/usr/bin/env python2
# coding=utf-8
"""
Compute the optimal weights and offsets for a given n-tap blur filter kernel.

Both discrete and linear sampling are supported, for an in-depth article on
the subject, please refer to the following url:

http://rastergrid.com/blog/2010/09/efficient-gaussian-blur-with-linear-sampling/

"""

__license__ = """
Copyright 2012 Manuel Bua

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

"""

import sys
import math
import argparse


# FYI, efficient gaussian blur is described in great detail here:
#

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


def draw_pascal(cols_count):
    length = len(str(binom(cols_count)))
    for i in xrange(cols_count):
        print ("{:^" + str(length) + "}").format(str(binom(i)))


def kernel_binom(taps, expand_by=0, reduce_by=0):
    """Compute discrete weights and factors
    """

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
    """Compute linearly interpolated weights and factors
    """

    res = kernel_binom(taps, expand_by, reduce_by)
    if res is None:
        print "ERR: can't perform linear reduction pass, no input data"
        return None

    w_count = len(res['weights'])
    pairs = int(w_count - 1)

    # sanity checks
    if w_count & 1 == 0:
        print "ERR: duped coefficients at center"
        return None

    if pairs % 2 > 0:
        print "ERR: can't perform bilinear reduction on non-paired texels"
        return None

    wd = res['weights']
    weights = [wd[0]]
    weights.extend([wd[x] + wd[x + 1] for x in xrange(1, w_count - 1, 2)])

    od = res['offsets']
    offsets = [0]
    offsets.extend([(od[x] * wd[x] + od[x + 1] * wd[x + 1]) / weights[i + 1]
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
            "--linear", default=False, action='store_true',
            help="Uses linear sampling to compute weights and offsets"
        )

        args = parser.parse_args()

        taps = args.taps
        exp = args.expand
        red = args.reduce
        linear = args.linear

    else:
        # debug

        taps = 9
        exp = 2
        red = 2
        linear = True

    print "Computing a %(taps)s-tap filter kernel (+%(exp)s/-%(red)s)" \
          "%(desc)s" % \
          {'taps': taps, 'exp': exp * 2, 'red': red * 2,
           'desc': " reduced by linear sampling" if linear else ""}

    print "Initial gaussian distribution: {0}".format(str(binom(taps - 1)))

    ntap = taps
    if linear:
        res = kernel_binom_linear(taps, exp, red)
        ntap = (len(res['weights']) * 2) - 1
    else:
        res = kernel_binom(taps, exp, red)

    if res is not None and ntap > 0:
        if linear:
            print "Optimized to {0}-tap filter kernel".format(ntap)

        print "weights:", ["{:.6f}".format(x) for x in res["weights"]]
        print "offsets:", ["{:.6f}".format(x) for x in res["offsets"]]


if __name__ == "__main__":
    main()
