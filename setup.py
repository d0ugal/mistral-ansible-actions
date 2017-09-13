#!/usr/bin/env python

from setuptools import setup


setup(
    setup_requires=['pbr', 'mistral-lib', 'oslo.concurrency'],
    package_dir={'': '.'},
    py_modules=['mistral_ansible_actions'],
    pbr=True,
)
