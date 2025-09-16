#
# This file is part of LiteSPI
#
# Copyright (c) 2020 Antmicro <www.antmicro.com>
# SPDX-License-Identifier: BSD-2-Clause

from migen import *

from litex.gen import *

from litespi.common import *

from litespi.phy.generic_sdr import LiteSPISDRPHYCore
from litespi.phy.generic_ddr import LiteSPIDDRPHYCore

# LiteSPI PHY --------------------------------------------------------------------------------------

class LiteSPIPHY(LiteXModule):
    """LiteSPI PHY instantiator

    The ``LiteSPIPHY`` class instantiate generic PHY - ``LiteSPIPHYCore`` that can be connected to the ``LiteSPICore``,
    handles optional clock domain wrapping for whole PHY and interfaces streams and CS signal from PHY logic.

    Parameters
    ----------
    pads : Object
        SPI pads description.

    flash : SpiNorFlashModule
        SpiNorFlashModule configuration object.

    device : str
        Device type for use by the ``LiteSPIClkGen``.

    clock_domain : str
        Name of LiteSPI clock domain.

    default_divisor : int (1:1 rate)
        Default frequency divisor for clkgen.

    rate : str
        Rate: 1:1 SDR, 1:2 DDR.

    extra_latency : int
        Compensate for additional Output/Input latency

    Attributes
    ----------
    source : Endpoint(spi_phy2core_layout), out
        Data stream from ``LiteSPIPHYCore``.

    sink : Endpoint(spi_core2phy_layout), in
        Control stream from ``LiteSPIPHYCore``.

    cs : Signal(), in
        Flash CS signal from ``LiteSPIPHYCore``.
    """

    def __init__(self, pads, flash, device="xc7", clock_domain="sys", default_divisor=9, cs_delay=10, rate="1:1", **kwargs):
        assert rate in ["1:1", "1:2"]
        if rate == "1:1":
            phy = LiteSPISDRPHYCore(pads, flash, device, clock_domain, default_divisor, cs_delay, **kwargs)
        if rate == "1:2":
            phy = LiteSPIDDRPHYCore(pads, flash, cs_delay, **kwargs)

        self.flash = flash

        self.source = phy.source
        self.sink   = phy.sink
        self.cs     = phy.cs

        # # #

        if clock_domain != "sys":
            phy = ClockDomainsRenamer(clock_domain)(phy)

        self.spiflash_phy = phy

    def get_csrs(self):
        return self.spiflash_phy.get_csrs()
