# -*- encoding: utf-8 -*-
from setuptools import find_packages
from setuptools import setup

# https://docs.python.org/3/distutils/setupscript.html
setup(
    name='blur-ninja',
    version='1.0.0',
    license='Apache License, Version 2.0',
    description='',
    author='Manuel Bua, Lionel ATTY',
    author_email='yoyonel@hotmail.com',
    url='https://github.com/manuelbua/blur-ninja.git',
    packages=['blurninja.{}'.format(x) for x in find_packages('src/blurninja')],
    package_dir={'': 'src'},
    classifiers=[
        # complete classifier list: http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Operating System :: Unix',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
        'Topic :: Utilities',
    ],
    keywords=[],
    install_requires=[
        "ansicolors==1.1.8",
        "future==0.16.0",
    ],
    extras_require={},
    entry_points={
        'console_scripts': [
            'blurninja = blurninja.app:main'
        ]
    },
)
