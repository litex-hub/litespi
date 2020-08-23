#
# This file is part of LiteSPI
#
# Copyright (c) 2020 Antmicro <www.antmicro.com>
# SPDX-License-Identifier: BSD-2-Clause

"""
Stream layout for LiteSPICore->PHY connection:
data - flash byte address when cmd=1, data to transmit when cmd=2, unused in cmd=0
cmd  - command type: 0 - read 32-bits from flash, 1 - send new read command starting from addr, 2 - perform custom SPI operation described by additonal settings
Following settings are used only when cmd=2:
len - xfer length (in bits)
width - xfer width (1/2/4/8)
mask - dq output enable control (1 enables a output on a particular pin)
"""
spi_phy_ctl_layout = [
    ("data", 32),
    ("cmd", 2),
    ("len", 6),
    ("width", 4),
    ("mask", 8),
]
CMD = 0
READ = 1
USER = 2
"""
Stream layout for PHY->LiteSPICore connection
data - 32-bits of data from flash
"""
spi_phy_data_layout = [
    ("data", 32),
]

MMAP_PORT = 0
MASTER_PORT = 1
