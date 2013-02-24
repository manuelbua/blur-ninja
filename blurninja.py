#!/usr/bin/env python2
# coding=utf-8
"""
Calculates gaussian kernel weights and offsets from a binomial distribution and
optionally adjust the weights and offsets for a linearly-sampled gaussian blur
shader.

Both discrete and linear sampling are supported, for an in-depth article on
the subject, please refer to the following url:

http://rastergrid.com/blog/2010/09/efficient-gaussian-blur-with-linear-sampling/

"""

__license__ = """
Copyright 2013 Manuel Bua

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

import argparse
from blurninja.fancy_output import bold
from blurninja.binom import binom
from blurninja.kernel import kernel_binom, kernel_binom_linear


def main():
    parser = argparse.ArgumentParser(
        description="Calculates gaussian kernel weights and offsets from a "
                    "binomial distribution and optionally adjust the weights "
                    "and offsets for a linearly-sampled gaussian blur shader.")

    parser.add_argument(
        "taps", default=5, type=int,
        help="Specify the number of taps (kernel size)"
    )

    parser.add_argument(
        "--expand", default=0, type=int,
        help="How much to expand the tap count (expand outermost "
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

    print "Computing a", \
        bold("{0}-tap".format(taps)), \
        "filter kernel (+%(exp)s/-%(red)s) %(desc)s" % \
        {
            'taps': taps,
            'exp': exp * 2,
            'red': red * 2,
            'desc': " (+linear reduction)" if linear else ""
        }

    print "Initial gaussian distribution: {0}".format(
        bold(str(binom(taps - 1)))
    )

    ntap = taps

    res_discrete = kernel_binom(taps, exp, red)
    res_linear = None

    if linear:
        res_linear = kernel_binom_linear(res_discrete)
        ntap = (len(res_linear['weights']) * 2) - 1

    if res_discrete is not None:
        float_format = "{:.8f}"

        print "Initial ", \
            bold("{0}-tap".format(taps)), \
            "filter kernel coefficients:".format(taps)

        print "\tweights:", \
            [float_format.format(x) for x in res_discrete["weights"]]

        print "\toffsets:", \
            [float_format.format(x) for x in res_discrete["offsets"]]

        if linear and res_linear is not None:
            print "\nOptimized", \
                bold("{0}-tap".format(ntap)), \
                "filter kernel coefficients:".format(ntap)
            print "\tweights:", \
                [float_format.format(x) for x in res_linear["weights"]]

            print "\toffsets:", \
                [float_format.format(x) for x in res_linear["offsets"]]


if __name__ == "__main__":
    main()
