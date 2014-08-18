#!/usr/bin/env python
from setuptools import setup, find_packages
import os
import sys

packages = ['Ranger',
            'Ranger.src',
            'Ranger.src.Range',
            'Ranger.src.Collections',
            'Ranger.test',
            'Ranger.test.src',
            'Ranger.test.src.Range',
            'Ranger.test.src.Collections'
           ]
setup(
    name = 'ranger',
    version = '0.4',
    packages=packages,
    author = 'Eli Rodgers-Melnick',
    author_email = 'er432@cornell.edu',
    description = 'A Python package for the manipulation of Range objects',
    keywords = ['Ranges','Set','Set theory'],
    long_description = """
Ranger is a Python package for the manipulation of range objects.
Ranges may extend over discrete or continuous domains, be open or closed,
bounded or unbounded. Ranger also includes tools for managing collections
 of ranges, which may be mapped to other objects.
""",
    license = 'BSD',
    platforms = ['Linux','Mac OSX','Windows','Unix'],
    url = 'https://github.com/er432/Ranger',
    test_suite = 'Ranger.test',
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Topic :: Scientific/Engineering :: Information Analysis'
    ]
    )
