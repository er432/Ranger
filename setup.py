#!/usr/bin/env python
from setuptools import setup, find_packages
import os
import sys

sys.path.insert(0,'Ranger')
import release
version = release.write_versionfile()
sys.path.pop(0)
packages = ['Ranger',
            'Ranger.src',
            'Ranger.src.Range'
           ]
setup(
    name = release.name.lower(),
    version = version,
    author = release.authors['Rodgers-Melnick'][0],
    author_email = release.authors['Rodgers-Melnick'][1],
    description = release.description,
    keywords = release.keywords,
    long_description = release.long_description,
    license = release.license,
    platforms = release.platforms,
    url = release.url,
    test_suite = 'Ranger.test',
    classifiers = release.classifiers
    )
