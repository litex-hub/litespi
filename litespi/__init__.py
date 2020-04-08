from migen import *

from litex.soc.integration.doc import AutoDoc, ModuleDoc
from litex.soc.interconnect import wishbone, stream
from litex.soc.interconnect.csr import *

from litespi.common import *
from litespi.core.master import LiteSPIMaster
from litespi.core.xip import LiteSPIXIP

class LiteSPICore(Module):
    def __init__(self):
        self.source = stream.Endpoint(spi_phy_ctl_layout)
        self.sink   = stream.Endpoint(spi_phy_data_layout)
        self.cs_n   = Signal()

class LiteSPI(Module, AutoCSR, AutoDoc, ModuleDoc):
    """SPI Controller wrapper.
    
    The ``LiteSPI`` class provides a wrapper that can instantiate both ``LiteSPIXIP`` and ``LiteSPIMaster`` and connect them to the PHY.

    Both options can be used at the same time with help of ``mux_sel`` register which allows to share access to PHY.

    Parameters
    ----------
    phy : Module
        Module or object that contains PHY stream interfaces and a cs_n signal to connect the ``LiteSPICore`` to.

    with_xip : bool
        Enables memory-mapped SPI flash controller.

    with_master : bool
        Enables register-operated SPI master controller.

    xip_endianness : string
        If endianness is set to ``small`` then byte order of each 32-bit word comming XIP core will be reversed.

    Attributes
    ----------
        bus : Interface(), out
            Wishbone interface for memory-mapped flash access.
    """
    def __init__(self, phy, with_xip=True, with_master=True, xip_endianness="big"):
        assert with_xip or with_master

        self._cfg = CSRStorage(fields=[
            CSRField("mux_sel", size=1, offset=0, description="SPI PHY multiplexer bit (0=SPIXIP module attached to PHY, 1=SPI Master attached to PHY)")
        ])

        self.submodules.xip    = xip = LiteSPIXIP(xip_endianness) if with_xip else LiteSPICore()
        self.submodules.master = master = LiteSPIMaster() if with_master else LiteSPICore()

        if with_xip:
            self.bus = xip.bus

        self.comb += [
            If(self._cfg.fields.mux_sel,
                master.source.connect(phy.sink),
                phy.source.connect(master.sink),
                phy.cs_n.eq(master.cs_n),
            ).Else(
                xip.source.connect(phy.sink),
                phy.source.connect(xip.sink),
                phy.cs_n.eq(xip.cs_n),
            )
        ]
