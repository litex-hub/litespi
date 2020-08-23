#
# This file is part of LiteSPI
#
# Copyright (c) 2015 Florent Kermarrec <florent@enjoy-digital.fr>
# Copyright (c) 2020 Antmicro <www.antmicro.com>
# SPDX-License-Identifier: BSD-2-Clause

from collections import OrderedDict

from migen import *
from litespi.common import *

from litex.soc.interconnect import stream
from litex.soc.interconnect.packet import Arbiter, Dispatcher


class LiteSPIMasterPort:
    def __init__(self):
        self.source = stream.Endpoint(spi_phy_ctl_layout)
        self.sink = stream.Endpoint(spi_phy_data_layout)


class LiteSPISlavePort:
    def __init__(self):
        self.source = stream.Endpoint(spi_phy_data_layout)
        self.sink = stream.Endpoint(spi_phy_ctl_layout)


class LiteSPICrossbar(Module):
    def __init__(self, rx_mux, cd):
        self.cd = cd
        self.users = OrderedDict()
        self.rx_mux = rx_mux
        self.master = LiteSPIMasterPort()

        if cd is not "sys":
            rx_cdc = stream.AsyncFIFO(spi_phy_data_layout, 32, buffered=True)
            tx_cdc = stream.AsyncFIFO(spi_phy_ctl_layout, 32, buffered=True)
            self.submodules.rx_cdc = ClockDomainsRenamer({"write": "litespi", "read": "sys"})(rx_cdc)
            self.submodules.tx_cdc = ClockDomainsRenamer({"write": "sys", "read": "litespi"})(tx_cdc)
            self.comb += [
                self.rx_cdc.source.connect(self.master.sink),
                self.master.source.connect(self.tx_cdc.sink),
            ]

        self.cs_n = Signal()
        self.user_cs = {}

    def get_port(self, port_id, cs):
        user_port = LiteSPISlavePort()
        internal_port = LiteSPISlavePort()

        tx_stream = user_port.sink

        self.comb += tx_stream.connect(internal_port.sink)

        rx_stream = internal_port.source

        self.comb += rx_stream.connect(user_port.source)

        self.users[port_id] = internal_port
        self.user_cs[port_id] = self.cs_n.eq(cs)

        return user_port

    def do_finalize(self):
        # TX
        sinks = [port.sink for port in self.users.values()]
        self.submodules.arbiter = Arbiter(sinks, self.master.source)
        # RX
        sources = [port.source for port in self.users.values()]
        self.submodules.dispatcher = Dispatcher(self.master.sink,
                                                sources,
                                                one_hot=True)

        cases = {}
        cases["default"] = self.dispatcher.sel.eq(0)
        for i, (k, v) in enumerate(self.users.items()):
            cases[k] = self.dispatcher.sel.eq(2**i)

        self.comb += [
            Case(self.rx_mux, cases),
            Case(self.rx_mux, self.user_cs),
        ]
