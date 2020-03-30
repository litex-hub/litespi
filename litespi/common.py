"""
Stream layout for LiteSPICore->PHY connection
addr - flash byte address, used only when cmd=1
cmd  - command type: 0 - read 32-bits from flash, 1 - send new read command starting from addr
"""
spi_phy_ctl_layout = [
    ("addr", 32),
    ("cmd", 1),
]
"""
Stream layout for PHY->LiteSPICore connection
data - 32-bits of data from flash
"""
spi_phy_data_layout = [
    ("data", 32),
]
