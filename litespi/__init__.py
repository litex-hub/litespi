from migen import *

from litex.soc.integration.doc import AutoDoc, ModuleDoc
from litex.soc.interconnect import wishbone, stream
from litex.soc.interconnect.csr import *

from litespi.common import *
from litespi.crossbar import LiteSPICrossbar
from litespi.core.master import LiteSPIMaster
from litespi.core.mmap import LiteSPIMMAP

class LiteSPICore(Module):
    def __init__(self):
        self.source = stream.Endpoint(spi_phy_ctl_layout)
        self.sink   = stream.Endpoint(spi_phy_data_layout)
        self.cs_n   = Signal()

class LiteSPI(Module, AutoCSR, AutoDoc, ModuleDoc):
    """SPI Controller wrapper.
    
    The ``LiteSPI`` class provides a wrapper that can instantiate both ``LiteSPIMMAP`` and ``LiteSPIMaster`` and connect them to the PHY.

    Both options can be used at the same time with help of ``mux_sel`` register which allows to share access to PHY.

    Parameters
    ----------
    phy : Module
        Module or object that contains PHY stream interfaces and a cs_n signal to connect the ``LiteSPICore`` to.

    with_mmap : bool
        Enables memory-mapped SPI flash controller.

    with_master : bool
        Enables register-operated SPI master controller.

    mmap_endianness : string
        If endianness is set to ``small`` then byte order of each 32-bit word comming MMAP core will be reversed.

    Attributes
    ----------
        bus : Interface(), out
            Wishbone interface for memory-mapped flash access.
    """
    def __init__(self, phy, with_mmap=True, with_master=True, mmap_endianness="big"):
        assert with_mmap or with_master

        self._cfg = CSRStorage(fields=[
            CSRField("mux_sel", size=1, offset=0, description="SPI PHY multiplexer bit (0=SPIMMAP module attached to PHY, 1=SPI Master attached to PHY)")
        ])

        self.submodules.crossbar = crossbar = LiteSPICrossbar(self._cfg.fields.mux_sel)

        if with_mmap:
            self.submodules.mmap = mmap = LiteSPIMMAP(mmap_endianness)
            port_mmap = crossbar.get_port(MMAP_PORT, mmap.cs_n)
            self.bus = mmap.bus
            self.comb += [
                port_mmap.source.connect(mmap.sink),
                mmap.source.connect(port_mmap.sink),
            ]
        if with_master:
            self.submodules.master = master = LiteSPIMaster()
            port_master = crossbar.get_port(MASTER_PORT, master.cs_n)
            self.comb += [
                port_master.source.connect(master.sink),
                master.source.connect(port_master.sink),
            ]

        self.comb += [
            crossbar.master.source.connect(phy.sink),
            phy.source.connect(crossbar.master.sink),
            phy.cs_n.eq(crossbar.cs_n),
        ]
