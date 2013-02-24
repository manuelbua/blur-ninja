BlurNinja!
==========

Calculates *gaussian* kernel weights and offsets from a binomial distribution and optionally optimize them to be used in a linearly-sampled gaussian blur shader.

For the non-initiated, get up to speed with this great, in-depth article on the subject:

http://rastergrid.com/blog/2010/09/efficient-gaussian-blur-with-linear-sampling/


Optional dependancies
==========

There is some very preliminary support for some fancy output by using [AnsiColors](https://pypi.python.org/pypi/ansicolors/1.0.2), if its already installed.
You can install it by:

    pip install ansicolors

Usage
==========

    blurninja.py [-h] [--expand EXPAND] [--reduce REDUCE] [--linear] taps

      -h, --help       show the help message and exit
      --expand EXPAND  How much to expand the tap count (expand outermost
                       coefficients)
      --reduce REDUCE  How many taps to discard at borders (eliminate outermost
                       coefficients)
      --linear         Uses linear sampling to compute weights and offsets

      taps             Specify the number of taps (kernel size) [required]

Example
==========

By following the [rastergrid's explanations](http://rastergrid.com/blog/2010/09/efficient-gaussian-blur-with-linear-sampling/), we can generate the various weights and offsets and testing different results along the way.

As a first example, we choose to define a **9-tap** filter kernel by augmenting the *row index* for later *discarding coefficients at borders* (we do this to minimize texture lookups for coefficients with little or no effect), this can be computed in this way:

    ./blurninja.py --expand 2 --reduce 2 9

The output should be something like this (note blurninja will compute **only** the positive half of both the weights and offsets):

    Computing a 9-tap filter kernel (+4/-4)
    Initial gaussian distribution: [1, 12, 66, 220, 495, 792, 924, 792, 495, 220, 66, 12, 1]
    Initial  9-tap filter kernel coefficients:
        weights: ['0.22702703', '0.19459459', '0.12162162', '0.05405405', '0.01621622']
        offsets: ['0.00000000', '1.00000000', '2.00000000', '3.00000000', '4.00000000']

I'll leave any explanation to the article in question, instead we are now going to optimize this result for a more efficient gaussian blur.
In fact, this is really simple to do, just specify the **--linear** switch on the command line to have BlurNinja optimize the weights coefficients for you: also look at the offsets, they get properly recomputed in order to correctly produce the desired result with a GL_LINEAR-enabled framebuffer (you already know this optimization revolves around retrieving information on **two texels** with a **single** texture fetch, don't you?)

So, let's BlurNinja compute all this for us, just copy the previous command line and specificy the additional **--linear** switch:

    ./blurninja.py --linear --expand 2 --reduce 2 9

This time the output should be like this:

    Computing a 9-tap filter kernel (+4/-4)  (+linear reduction)
    Initial gaussian distribution: [1, 12, 66, 220, 495, 792, 924, 792, 495, 220, 66, 12, 1]
    Initial  9-tap filter kernel coefficients:
        weights: ['0.22702703', '0.19459459', '0.12162162', '0.05405405', '0.01621622']
        offsets: ['0.00000000', '1.00000000', '2.00000000', '3.00000000', '4.00000000']

    Optimized 5-tap filter kernel coefficients:
        weights: ['0.22702703', '0.31621622', '0.07027027']
        offsets: ['0.00000000', '1.38461538', '3.23076923']

Now look at that! We just halved the number of texture fetches (5 vs. 9), making it a lot more efficient.
