#!/usr/bin/env python3

from setuptools import setup
from setuptools import find_packages


with open("README.md", "r", encoding="utf-8") as fp:
    long_description = fp.read()


setup(
    name                          = "litespi",
    version                       = "2024.12",
    description                   = "Small footprint and configurable SPI core",
    long_description              = long_description,
    long_description_content_type = "text/markdown",
    author                        = "LiteSPI Developers",
    url                           = "https://github.com/litex-hub",
    download_url                  = "https://github.com/litex-hub/litespi",
    test_suite                    = "test",
    license                       = "BSD",
    python_requires               = "~=3.7",
    install_requires              = ["pyyaml", "litex"],
    extras_require                = {
        "develop": [
          "meson"
          "pexpect"
          "setuptools"
          "requests"
        ]
    },
    packages                      = find_packages(exclude=("test*", "sim*", "doc*", "examples*")),
    include_package_data          = True,
    keywords                      = "HDL ASIC FPGA hardware design",
    classifiers                   = [
        "Topic :: Scientific/Engineering :: Electronic Design Automation (EDA)",
        "Environment :: Console",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
    ],
    entry_points = {
        "console_scripts": [
            "litespi_gen=litespi.gen:main",
        ],
    },
)
