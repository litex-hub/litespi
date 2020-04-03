from migen import *

from litex.soc.interconnect import stream

from litex.soc.integration.doc import AutoDoc, ModuleDoc

from litespi.core import LiteSPICore


class LiteSPI(Module, AutoDoc, ModuleDoc):
    """Memory-mapped SPI Flash wrapper.
    
    The ``LiteSPI`` class provides a wrapper that instantiates ``LiteSPICore`` and connects it to PHY provided as parameter.

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
        self.submodules.core = core = LiteSPICore(endianness)
        self.bus = core.bus

        self.comb += [
            phy.cs_n.eq(core.cs_n),
            phy.source.connect(core.sink),
            core.source.connect(phy.sink),
        ]
