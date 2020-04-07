#!/usr/bin/env python3

from setuptools import setup
from setuptools import find_packages


setup(
    name="litespi",
    description="Small footprint and configurable SPI core",
    author="LiteSPI Developers",
    url="https://github.com/litex-hub",
    download_url="https://github.com/litex-hub/litespi",
    test_suite="test",
    license="BSD",
    python_requires="~=3.6",
    packages=find_packages(exclude=("test*", "sim*", "doc*", "examples*")),
    include_package_data=True,
)
