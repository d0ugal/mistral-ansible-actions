#!/usr/bin/env python

from setuptools import setup


setup(
    setup_requires=['pbr'],
    package_dir={'': 'src'},
    py_modules=['mistral_ansible_actions'],
    pbr=True,
)
