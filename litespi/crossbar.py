#
# This file is part of LiteSPI
#
# Copyright (c) 2015 Florent Kermarrec <florent@enjoy-digital.fr>
# Copyright (c) 2020 Antmicro <www.antmicro.com>
# SPDX-License-Identifier: BSD-2-Clause

from collections import OrderedDict

from migen import *
from migen.genlib.roundrobin import RoundRobin
from litespi.common import *

from litex.soc.interconnect import stream


class LiteSPIMasterPort:
    def __init__(self):
        self.source = stream.Endpoint(spi_core2phy_layout)
        self.sink   = stream.Endpoint(spi_phy2core_layout)


class LiteSPISlavePort:
    def __init__(self):
        self.source = stream.Endpoint(spi_phy2core_layout)
        self.sink   = stream.Endpoint(spi_core2phy_layout)


class LiteSPICrossbar(Module):
    """SPI Crossbar.

    Arbitrates the PHY between the cores. With a PHY clock domain (``cd`` other than ``"sys"``),
    the core-to-PHY transfers and the chip select cross through the TX AsyncFIFO together: each CS
    change is a CS-only entry of the FIFO, ordered with the transfers, and the PHY side applies it
    once the PHY has answered every transfer queued before it. A CS release, even of one ``sys``
    cycle, is therefore never lost and never cuts a transfer; ``phy_cs`` and ``phy_source`` give
    the CS and the transfers in the PHY clock domain.
    """
    def __init__(self, cd, cs_width=1):
        self.cd     = cd
        self.users  = []
        self.master = LiteSPIMasterPort()

        self.cs           = Signal(cs_width)
        self.user_cs      = []
        self.user_request = []

        if cd != "sys":
            rx_cdc = stream.AsyncFIFO(spi_phy2core_layout, 32, buffered=True)
            tx_cdc = stream.AsyncFIFO(spi_core2phy_layout + [("cs", cs_width), ("cs_only", 1)], 32, buffered=True)
            self.submodules.rx_cdc = ClockDomainsRenamer({"write": cd, "read": "sys"})(rx_cdc)
            self.submodules.tx_cdc = ClockDomainsRenamer({"write": "sys", "read": cd})(tx_cdc)
            self.phy_source = stream.Endpoint(spi_core2phy_layout)
            self.phy_cs     = Signal(cs_width)
            self.comb += self.rx_cdc.source.connect(self.master.sink)

            # CS Crossing (sys side): a CS change goes in the FIFO as a CS-only entry, before the
            # transfers that follow it. A release (CS active, then changed) is remembered until
            # its entry is written, so a one-cycle release is not lost when the FIFO is full.
            cs_sent         = Signal(cs_width)
            cs_release      = Signal()
            cs_need_release = Signal()
            self.comb += cs_need_release.eq(cs_release | ((cs_sent != 0) & (self.cs != cs_sent)))
            self.comb += [
                If(cs_need_release,
                    self.tx_cdc.sink.valid.eq(1),
                    self.tx_cdc.sink.cs.eq(0),
                    self.tx_cdc.sink.cs_only.eq(1),
                ).Elif(self.cs != cs_sent,
                    self.tx_cdc.sink.valid.eq(1),
                    self.tx_cdc.sink.cs.eq(self.cs),
                    self.tx_cdc.sink.cs_only.eq(1),
                ).Else(
                    self.master.source.connect(self.tx_cdc.sink),
                    self.tx_cdc.sink.cs.eq(cs_sent),
                )
            ]
            self.sync += [
                If(self.tx_cdc.sink.valid & self.tx_cdc.sink.ready & self.tx_cdc.sink.cs_only,
                    cs_sent.eq(self.tx_cdc.sink.cs),
                ),
                If(cs_need_release,
                    cs_release.eq(~self.tx_cdc.sink.ready),
                ),
            ]

            # CS Crossing (PHY side): apply a CS-only entry once the PHY has answered every
            # transfer it accepted (one answer per transfer), so CS never changes mid-transfer.
            pending = Signal(8)
            sync_cd = getattr(self.sync, cd)
            self.comb += [
                If(self.tx_cdc.source.cs_only,
                    self.tx_cdc.source.ready.eq(pending == 0),
                ).Else(
                    self.tx_cdc.source.connect(self.phy_source, omit={"cs", "cs_only"}),
                )
            ]
            sync_cd += [
                If(self.tx_cdc.source.valid & self.tx_cdc.source.ready & self.tx_cdc.source.cs_only,
                    self.phy_cs.eq(self.tx_cdc.source.cs),
                ),
                If(self.phy_source.valid & self.phy_source.ready,
                    If(~(self.rx_cdc.sink.valid & self.rx_cdc.sink.ready),
                        pending.eq(pending + 1),
                    )
                ).Elif(self.rx_cdc.sink.valid & self.rx_cdc.sink.ready,
                    pending.eq(pending - 1),
                ),
            ]

    def get_port(self, cs, request = None):
        user_port     = LiteSPISlavePort()
        internal_port = LiteSPISlavePort()

        tx_stream = user_port.sink

        self.comb += tx_stream.connect(internal_port.sink)

        rx_stream = internal_port.source

        self.comb += rx_stream.connect(user_port.source)

        if request is None:
            request = Signal()
            self.comb += request.eq(cs != 0)

        self.users.append(internal_port)
        self.user_cs.append(self.cs.eq(cs))
        self.user_request.append(request)

        return user_port

    def do_finalize(self):
        self.submodules.rr = RoundRobin(len(self.users))

        # TX
        self.submodules.tx_mux = tx_mux = stream.Multiplexer(spi_core2phy_layout, len(self.users))

        # RX
        self.submodules.rx_demux = rx_demux = stream.Demultiplexer(spi_phy2core_layout, len(self.users))

        for i, user in enumerate(self.users):
            self.comb += [
                user.sink.connect(getattr(tx_mux, f"sink{i}")),
                getattr(rx_demux, f"source{i}").connect(user.source),
            ]

        self.comb += [
            self.rr.request.eq(Cat(self.user_request)),

            self.tx_mux.source.connect(self.master.source),
            self.tx_mux.sel.eq(self.rr.grant),

            self.master.sink.connect(self.rx_demux.sink),
            self.rx_demux.sel.eq(self.rr.grant),

            Case(self.rr.grant, dict(enumerate(self.user_cs))),
        ]
