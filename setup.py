from setuptools import setup, find_packages
import os

here = os.path.abspath(os.path.dirname(__file__))

setup(
    name='Ranger',
    author='Eli Rodgers-Melnick',
    author_email='er432@cornell.edu',
    description='Generic library for dealing with ranges',
    packages=['Ranger',
              'Ranger.src',
              'Ranger.src.Range'
              ],
    include_package_data=True,
    platforms='any',
    classifiers = [
        'Programming Language :: Python',
        'Natural Language :: English',
        'Operating System :: OS Independent'
        ]
    )
