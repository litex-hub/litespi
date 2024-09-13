#
# This file is part of LiteSPI
#
# Copyright (c) 2020 Antmicro <www.antmicro.com>
# SPDX-License-Identifier: BSD-2-Clause

from migen import *

from litex.gen import *

from litex.soc.interconnect import stream

from litespi.common import *
from litespi.crossbar import LiteSPICrossbar
from litespi.core.master import LiteSPIMaster
from litespi.core.mmap import LiteSPIMMAP


class LiteSPICore(Module):
    def __init__(self):
        self.source = stream.Endpoint(spi_core2phy_layout)
        self.sink   = stream.Endpoint(spi_phy2core_layout)
        self.cs     = Signal()


class LiteSPI(LiteXModule):
    """SPI Controller wrapper.

    The ``LiteSPI`` class provides a wrapper that can instantiate both ``LiteSPIMMAP`` and ``LiteSPIMaster`` and connect them to the PHY.

    Both options can be used at the same time with help of ``mux_sel`` register which allows to share access to PHY via crossbar.

    Parameters
    ----------
    phy : Module
        Module or object that contains PHY stream interfaces and a cs signal to connect the ``LiteSPICore`` to.

    clk_freq : int
        Frequency of a clock connected to LiteSPI.

    clock_domain : str
        Name of LiteSPI clock domain.

    with_mmap : bool
        Enables memory-mapped SPI flash controller.

    with_master : bool
        Enables register-operated SPI master controller.

    mmap_endianness : string
        If endianness is set to ``small`` then byte order of each 32-bit word comming MMAP core will be reversed.

    with_csr : bool
        The number of dummy bits can be configure when set to True.

    with_mmap_write : bool or string
        MMAP writes are supported when set to True or "csr". When set to "csr", they are disabled by default but
        can be enabled on demand using a CSR.

        Please note that only False and "csr" should be used with flash chips! True is only meant for RAM.

        When using "csr" with a flash chip, make sure to erase the corresponding pages of the flash beforehand
        using the LiteSPI master. It is also recommended to disable mmap writing once it is not required anymore.

    Attributes
    ----------
    bus : Interface(), out
        Wishbone interface for memory-mapped flash access.
    """

    def __init__(self, phy, clock_domain="sys",
        with_mmap=True, mmap_endianness="big",
        with_master=True, master_tx_fifo_depth=1, master_rx_fifo_depth=1,
        with_csr=True, with_mmap_write=False):

        self.crossbar = crossbar = LiteSPICrossbar(clock_domain)
        self.comb += phy.cs.eq(crossbar.cs)

        if with_mmap:
            self.mmap = mmap = LiteSPIMMAP(flash=phy.flash,
                                                      endianness=mmap_endianness,
                                                      with_csr=with_csr,
                                                      with_write=with_mmap_write)
            port_mmap = crossbar.get_port(mmap.cs)
            self.bus = mmap.bus
            self.comb += [
                port_mmap.source.connect(mmap.sink),
                mmap.source.connect(port_mmap.sink),
            ]
            if hasattr(phy, "dummy_bits"):
                self.comb += phy.dummy_bits.eq(mmap._spi_dummy_bits)
        if with_master:
            self.master = master = LiteSPIMaster(
                tx_fifo_depth = master_tx_fifo_depth,
                rx_fifo_depth = master_rx_fifo_depth)
            port_master = crossbar.get_port(master.cs)
            self.comb += [
                port_master.source.connect(master.sink),
                master.source.connect(port_master.sink),
            ]

        if clock_domain != "sys":
            self.comb += [
                crossbar.tx_cdc.source.connect(phy.sink),
                phy.source.connect(crossbar.rx_cdc.sink),
            ]
        else:
            self.comb += [
                crossbar.master.source.connect(phy.sink),
                phy.source.connect(crossbar.master.sink),
            ]
