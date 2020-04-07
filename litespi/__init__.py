from migen import *

from litex.soc.interconnect import stream
from litex.soc.integration.doc import AutoDoc, ModuleDoc

from litespi.core.master import LiteSPIMaster
from litespi.core.xip import LiteSPIXIP


class LiteSPI(Module, AutoDoc, ModuleDoc):
    """Memory-mapped SPI Flash wrapper.
    
    The ``LiteSPI`` class provides a wrapper that instantiates ``LiteSPIXIP`` and connects it to PHY provided as parameter.

    Parameters
    ----------
    phy : Module
        Module or object that contains PHY stream interfaces and a cs_n signal to connect the ``LiteSPICore`` to.

    endianness : string
        If endianness is set to ``small`` then byte order of each 32-bit word comming from flash will be reversed.

    Attributes
    ----------
        bus : Interface(), out
            Wishbone interface for memory-mapped flash access.
    """
    def __init__(self, phy, endianness="big"):
        self.submodules.xip = xip = LiteSPIXIP(endianness)
        self.bus = xip.bus

        self.comb += [
            phy.cs_n.eq(xip.cs_n),
            phy.source.connect(xip.sink),
            xip.source.connect(phy.sink),
        ]
