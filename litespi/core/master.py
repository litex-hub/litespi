#
# This file is part of LiteSPI
#
# Copyright (c) 2020 Antmicro <www.antmicro.com>
# SPDX-License-Identifier: BSD-2-Clause

from migen import *
from migen.genlib.fsm import FSM, NextState

from litex.soc.interconnect import stream
from litex.soc.interconnect.csr import *

from litespi.common import *


class LiteSPIMaster(Module, AutoCSR):
    """Generic LiteSPI Master

    The ``LiteSPIMaster`` class provides a generic SPI master that can be controlled using CSRs.

    It supports multiple access modes with help of ``width`` and ``mask`` registers which can be used to configure the PHY into any supported SDR mode (single/dual/quad/octal).

    Parameters
    ----------
    fifo_depth : int
        Depth of the internal TX/RX FIFO.

    cs_width : int
        Number of CS lines to support.

    Attributes
    ----------
    source : Endpoint(spi_phy2core_layout), out
        Data stream.

    sink : Endpoint(spi_core2phy_layout), in
        Control stream.

    cs : Signal(), out
        Slave CS signal.

    """
    def __init__(self, cs_width=1, tx_fifo_depth=1, rx_fifo_depth=1):
        self.sink   = stream.Endpoint(spi_phy2core_layout)
        self.source = stream.Endpoint(spi_core2phy_layout)
        self.cs     = Signal(cs_width)
        assert self.sink.data.nbits == self.source.data.nbits

        self._cs = CSRStorage(cs_width)
        self._phyconfig = CSRStorage(fields=[
            CSRField("len",   size=8, offset=0,  description="SPI Xfer length (in bits)."),
            CSRField("width", size=4, offset=8,  description="SPI Xfer width (1/2/4/8)."),
            CSRField("mask",  size=8, offset=16, description="SPI DQ output enable mask (set bits to ``1`` to enable output drivers on DQ lines)."),
        ], description="SPI PHY settings.")
        self._rxtx = CSR(self.source.data.nbits)
        self._status = CSRStatus(fields=[
            CSRField("tx_ready", size=1, offset=0, description="TX FIFO is not full."),
            CSRField("rx_ready", size=1, offset=1, description="RX FIFO is not empty."),
        ])

        # # #

        # FIFOs.
        tx_fifo = stream.SyncFIFO(spi_core2phy_layout, depth=tx_fifo_depth)
        rx_fifo = stream.SyncFIFO(spi_phy2core_layout, depth=rx_fifo_depth)
        self.submodules += tx_fifo, rx_fifo
        self.comb += self.sink.connect(rx_fifo.sink)
        self.comb += tx_fifo.source.connect(self.source)

        # SPI CS.
        self.comb += self.cs.eq(self._cs.storage)

        # SPI TX (MOSI).
        self.comb += [
            tx_fifo.sink.valid.eq(self._rxtx.re),
            self._status.fields.tx_ready.eq(tx_fifo.sink.ready),
            tx_fifo.sink.data.eq(self._rxtx.r),
            tx_fifo.sink.len.eq(self._phyconfig.fields.len),
            tx_fifo.sink.width.eq(self._phyconfig.fields.width),
            tx_fifo.sink.mask.eq(self._phyconfig.fields.mask),
            tx_fifo.sink.last.eq(1),
        ]

        # SPI RX (MISO).
        self.comb += [
            rx_fifo.source.ready.eq(self._rxtx.we),
            self._status.fields.rx_ready.eq(rx_fifo.source.valid),
            self._rxtx.w.eq(rx_fifo.source.data),
        ]
