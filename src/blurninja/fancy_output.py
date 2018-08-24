# coding=utf-8
"""
Acts as a proxy between the "colors" package and the application.
In case no package is found, then pass-through functions will be defined.

Probably a better way exists, if so please tell me! :)
"""

try:
    import colors
except ImportError:
    def __pass_through(arg):
        return arg

    bold = __pass_through
else:
    bold = colors.bold
