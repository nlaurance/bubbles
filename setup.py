#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

import os
from setuptools import setup, find_packages

from pip._internal.req import parse_requirements
from pip._internal.download import PipSession

here = os.path.abspath(os.path.dirname(__file__))
about = {}

with open("README.md", "r") as f:
    readme = f.read()

install_reqs = parse_requirements(
    os.path.join(here, "requirements.txt"), session=PipSession()
)
requirements = [str(ir.req) for ir in install_reqs]

setup(
    author="Nicolas Laurance",
    author_email="nicolas.laurance@gmail.com",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.7",
    ],
    description="adds info bubbles on selenium screenshots",
    install_requires=requirements,
    long_description=readme,
    include_package_data=True,
    keywords="bubbles selenium",
    name="bubbles",
    packages=find_packages(include=["bubbles"]),
    url="https://github.com/nlaurance/bubbles",
    version="0.0.2",
    zip_safe=False,
)
