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
    def __init__(self, cd):
        self.cd     = cd
        self.users  = []
        self.master = LiteSPIMasterPort()
        if cd != "sys":
            rx_cdc = stream.AsyncFIFO(spi_phy2core_layout, 32, buffered=True)
            tx_cdc = stream.AsyncFIFO(spi_core2phy_layout, 32, buffered=True)
            self.submodules.rx_cdc = ClockDomainsRenamer({"write": cd, "read": "sys"})(rx_cdc)
            self.submodules.tx_cdc = ClockDomainsRenamer({"write": "sys", "read": cd})(tx_cdc)
            self.comb += [
                self.rx_cdc.source.connect(self.master.sink),
                self.master.source.connect(self.tx_cdc.sink),
            ]

        self.cs           = Signal()
        self.user_cs      = []
        self.user_request = []

    def get_port(self, cs, request = None):
        user_port     = LiteSPISlavePort()
        internal_port = LiteSPISlavePort()

        tx_stream = user_port.sink

        self.comb += tx_stream.connect(internal_port.sink)

        rx_stream = internal_port.source

        self.comb += rx_stream.connect(user_port.source)

        if request is None:
            request = Signal()
            self.comb += request.eq(cs)

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
