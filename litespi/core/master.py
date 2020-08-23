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
    source : Endpoint(spi_phy_data_layout), out
        Data stream.

    sink : Endpoint(spi_phy_ctl_layout), in
        Control stream.

    cs_n : Signal(), out
        Slave CS signal.

    """
    def get_fifo(self, depth, layout):
        return stream.SyncFIFO(layout, depth=depth, buffered=True)

    def __init__(self, fifo_depth=8, cs_width=1):
        self.submodules.tx_fifo = tx_fifo = self.get_fifo(fifo_depth, spi_phy_ctl_layout)
        self.submodules.rx_fifo = rx_fifo = self.get_fifo(fifo_depth, spi_phy_data_layout)
        self.sink = rx_fifo.sink
        self.source = tx_fifo.source

        assert self.sink.data.nbits == self.source.data.nbits

        self.cs_n = Signal(cs_width)

        self._cs = CSRStorage(cs_width)
        self._phyconfig = CSRStorage(fields=[
            CSRField("len", size=8, offset=0, description="SPI Xfer length (in bits)."),
            CSRField("width", size=4, offset=8, description="SPI Xfer width (1/2/4/8)."),
            CSRField("mask", size=8, offset=16, description="SPI DQ output enable mask (set bits to ``1`` to enable output drivers on DQ lines)."),
        ], description="SPI PHY settings.")
        self._rxtx = CSR(self.source.data.nbits)
        self._status = CSRStatus(fields=[
            CSRField("tx_ready", size=1, offset=0, description="TX FIFO is not full."),
            CSRField("rx_ready", size=1, offset=1, description="RX FIFO is not empty."),
        ])

        # CS
        self.comb += self.cs_n.eq(~self._cs.storage)

        # TX
        self.comb += [
            tx_fifo.sink.valid.eq(self._rxtx.re),
            self._status.fields.tx_ready.eq(tx_fifo.sink.ready),
            tx_fifo.sink.data.eq(self._rxtx.r),
            tx_fifo.sink.cmd.eq(USER),
            tx_fifo.sink.len.eq(self._phyconfig.fields.len),
            tx_fifo.sink.width.eq(self._phyconfig.fields.width),
            tx_fifo.sink.mask.eq(self._phyconfig.fields.mask),
            tx_fifo.sink.last.eq(1),
        ]

        # RX
        self.comb += [
            rx_fifo.source.ready.eq(self._rxtx.we),
            self._status.fields.rx_ready.eq(rx_fifo.source.valid),
            self._rxtx.w.eq(rx_fifo.source.data),
        ]
