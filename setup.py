#!/usr/bin/env python3

import sys
from setuptools import setup
from setuptools import find_packages


if sys.version_info[:3] < (3, 5):
    raise SystemExit("You need Python 3.5+")


setup(
    name="litespi",
    description="Small footprint and configurable SPI core",
    long_description=open("README.md").read(),
    author="LiteSPI Developers",
    url="https://github.com/litex-hub",
    download_url="https://github.com/litex-hub/litespi",
    test_suite="test",
    license="BSD",
    platforms=["Any"],
    keywords="HDL ASIC FPGA hardware design",
    classifiers=[
        "Topic :: Scientific/Engineering :: Electronic Design Automation (EDA)",
        "Environment :: Console",
        "Development Status :: Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
    ],
    packages=find_packages(exclude=("test*", "sim*", "doc*", "examples*")),
    include_package_data=True,
)
