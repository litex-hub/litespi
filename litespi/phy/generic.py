#
# This file is part of LiteSPI
#
# Copyright (c) 2020 Antmicro <www.antmicro.com>
# SPDX-License-Identifier: BSD-2-Clause

from migen import *
from migen.genlib.fsm import FSM, NextState
from migen.genlib.cdc import MultiReg

from litespi.clkgen import LiteSPIClkGen
from litespi.common import *

from litex.soc.interconnect import stream
from litex.soc.interconnect.csr import *

from litex.build.io import SDRTristate

from litex.soc.integration.doc import AutoDoc, ModuleDoc

# Output enable masks for the tri-state buffers, data mode mask is not included as oe pins default to 0
cmd_oe_mask  = 0b00000001
soft_oe_mask = 0b00000001
addr_oe_mask = {
    1: 0b00000001,
    2: 0b00000011,
    4: 0b00001111,
    8: 0b11111111,
}


class LiteSPIPHYCore(Module, AutoCSR, AutoDoc, ModuleDoc):
    """LiteSPI PHY instantiator

    The ``LiteSPIPHYCore`` class provides a generic PHY that can be connected to the ``LiteSPICore``.

    It supports single/dual/quad/octal output reads from the flash chips.

    The following diagram shows how each clock configuration option relates to outputs and input sampling in DDR mode:

    .. wavedrom:: ../../doc/ddr-timing-diagram.json

    Parameters
    ----------
    pads : Object
        SPI pads description.

    flash : SpiNorFlashModule
        SpiNorFlashModule configuration object.

    device : str
        Device type for use by the ``LiteSPIClkGen``.

    default_divisor : int
        Default frequency divisor for clkgen.

    Attributes
    ----------
    source : Endpoint(spi_phy_data_layout), out
        Data stream.

    sink : Endpoint(spi_phy_ctl_layout), in
        Control stream.

    cs_n : Signal(), in
        Flash CS signal.

    clk_divisor : CSRStorage
        Register which holds a clock divisor value applied to clkgen.

    dummy_bits : CSRStorage
        Register which hold a number of dummy bits to send during transmission.
    """

    def shift_out(self, width, bits, next_state, trigger=[], op=[], ddr=False):
        if type(trigger) is not list:
            trigger = [trigger]
            op = [op]

        edge = self.clkgen.negedge if not ddr else trigger[0]

        res = [
            self.clkgen.en.eq(1),
            If(edge,
                NextValue(self.fsm_cnt, self.fsm_cnt+width),
                If(self.fsm_cnt == (bits-width),
                    NextValue(self.fsm_cnt, 0),
                    NextState(next_state),
                ),
            ),
        ]

        if len(trigger) == len(op):
            for i in range(len(trigger)):
                res += [If(trigger[i], *op[i])]

        return res

    def __init__(self, pads, flash, device, clock_domain, default_divisor):
        self.source                 = source = stream.Endpoint(spi_phy_data_layout)
        self.sink                   = sink   = stream.Endpoint(spi_phy_ctl_layout)
        self.cs_n                   = Signal()
        self._spi_clk_divisor       = spi_clk_divisor   = Signal(8)
        self._spi_dummy_bits        = spi_dummy_bits    = Signal(8)
        self._default_dummy_bits    = flash.dummy_bits if flash.fast_mode else 0
        self._default_divisor       = default_divisor

        self.clk_divisor            = clk_divisor       = CSRStorage(8, reset=self._default_divisor)
        self.dummy_bits             = dummy_bits        = CSRStorage(8, reset=self._default_dummy_bits)

        if clock_domain is not "sys":
            self.specials += [
                MultiReg(clk_divisor.storage, spi_clk_divisor, "litespi"),
                MultiReg(dummy_bits.storage, spi_dummy_bits, "litespi"),
            ]
        else:
            self.comb += [
                spi_clk_divisor.eq(clk_divisor.storage),
                spi_dummy_bits.eq(dummy_bits.storage),
            ]
        if hasattr(pads, "miso"):
            bus_width = 1
            pads.dq = [pads.mosi, pads.miso]
        else:
            bus_width = len(pads.dq)

        assert bus_width in [1, 2, 4, 8]

        # Check if number of pads matches configured mode
        assert flash.check_bus_width(bus_width)

        addr_bits = flash.addr_bits
        cmd_width = flash.cmd_width
        addr_width = flash.addr_width
        data_width = flash.bus_width
        command = flash.read_opcode.code
        ddr = flash.ddr

        # For Output modes there is a constant 8 dummy cycles, for I/O and DTR modes
        # there are different number of dummy cycles and in some cases they can be configurable.
        # We control a number of dummy cycles by substracting addr_width value from spi_dummy_bits,
        # so to achieve a proper number of dummy cycles when using shift_out function
        # we need to calculate total dummy bits which depends on addr_width value.
        # NOTE: these values are just default ones, in case chip has
        # different default dummy cycles for these modes or dummy cycles can be configured,
        # please adjust the dummy bits value via CSR in liblitespi accordingly.
        if (addr_width > 1):
            # DTR mode
            if (ddr):
                if (addr_width == 2):
                    self.default_dummy_bits = 6 * addr_width
                elif (addr_width == 4):
                    self.default_dummy_bits = 8 * addr_width
                else:
                    self.default_dummy_bits = 16 * addr_width
            # I/O mode
            else:
                if (addr_width == 2):
                    self.default_dummy_bits = 4 * addr_width
                elif (addr_width == 4):
                    self.default_dummy_bits = 6 * addr_width
                else:
                    self.default_dummy_bits = 16 * addr_width

        self.submodules.clkgen = clkgen = LiteSPIClkGen(pads, device, with_ddr=ddr)

        data_bits = 32
        cmd_bits = 8

        self.comb += [
            clkgen.div.eq(spi_clk_divisor),
            clkgen.sample_cnt.eq(1),
            clkgen.update_cnt.eq(1),
            pads.cs_n.eq(self.cs_n),
        ]

        dq_o  = Signal(len(pads.dq))
        dq_i  = Signal(len(pads.dq))
        dq_oe = Signal(len(pads.dq))

        for i in range(len(pads.dq)):
            self.specials += SDRTristate(
                io = pads.dq[i],
                o  = dq_o[i],
                oe = dq_oe[i],
                i  = dq_i[i],
            )

        self.fsm_cnt = Signal(8)
        addr         = Signal(addr_bits if not ddr else addr_bits+addr_width) # dummy data for the first register shift
        data         = Signal(data_bits)
        cmd          = Signal(cmd_bits)

        usr_dout  = Signal().like(sink.data)
        usr_din   = Signal().like(sink.data)
        usr_len   = Signal().like(sink.len)
        usr_width = Signal().like(sink.width)
        usr_mask  = Signal().like(sink.mask)

        din_width_cases = {1: [NextValue(usr_din, Cat(dq_i[1], usr_din))]}
        for i in [2, 4, 8]:
            din_width_cases[i] = [NextValue(usr_din, Cat(dq_i[0:i], usr_din))]

        dout_width_cases = {}
        for i in [1, 2, 4, 8]:
            dout_width_cases[i] = [dq_o.eq(usr_dout[-i:])]

        commands = {
            CMD: [
                NextValue(addr, sink.data),
                NextValue(cmd, command),
                NextState("CMD")
            ],
            READ: [
                NextState("DATA")
            ],
            USER: [
                NextValue(usr_dout, sink.data<<(32-sink.len)),
                NextValue(usr_din, 0),
                NextValue(usr_len, sink.len),
                NextValue(usr_width, sink.width),
                NextValue(usr_mask, sink.mask),
                NextState("USER")
            ],
        }

        self.submodules.fsm = fsm = FSM(reset_state="IDLE")
        fsm.act("IDLE",
            sink.ready.eq(1),
            If(sink.ready & sink.valid,
                Case(sink.cmd, commands),
            ),
        )
        fsm.act("CMD",
            dq_oe.eq(cmd_oe_mask),
            dq_o.eq(cmd[-cmd_width:]),
            self.shift_out(cmd_width, cmd_bits, "ADDR", op=[NextValue(cmd, cmd<<cmd_width)], trigger=clkgen.negedge, ddr=False),
        )
        fsm.act("ADDR",
            dq_oe.eq(addr_oe_mask[addr_width]),
            dq_o.eq(addr[-addr_width:]),
            If(spi_dummy_bits > 0,
                self.shift_out(addr_width, len(addr), "DUMMY", op=[NextValue(addr, addr<<addr_width)], trigger=clkgen.negedge if not ddr else clkgen.update, ddr=ddr)
            ).Else(
                self.shift_out(addr_width, len(addr), "IDLE", op=[NextValue(addr, addr<<addr_width)], trigger=clkgen.negedge if not ddr else clkgen.update, ddr=ddr)
            )
        )
        fsm.act("DUMMY",
            If(self.fsm_cnt < 8, dq_oe.eq(addr_oe_mask[addr_width])), # output 0's for the first dummy byte
            self.shift_out(addr_width, spi_dummy_bits, "IDLE"),
        )
        fsm.act("DATA",
            self.shift_out(data_width, data_bits, "SEND_DATA", op=[NextValue(data, Cat(dq_i[1] if data_width == 1 else dq_i[0:data_width], data))], trigger=clkgen.posedge if not ddr else clkgen.sample, ddr=ddr)
        )
        fsm.act("USER",
            dq_oe.eq(usr_mask),
            Case(usr_width, dout_width_cases),
            self.shift_out(usr_width, usr_len, "SEND_USER_DATA", trigger=[
                clkgen.posedge, # data sampling
                clkgen.negedge, # data update
            ], op=[
                [Case(usr_width, din_width_cases)],
                [NextValue(usr_dout, usr_dout<<usr_width)],
            ], ddr=False)
        ),
        fsm.act("SEND_USER_DATA",
            source.valid.eq(1),
            source.last.eq(1),
            source.data.eq(usr_din),
            If(source.ready & source.valid,
                NextState("IDLE"),
            )
        )
        fsm.act("SEND_DATA",
            source.valid.eq(1),
            source.last.eq(1),
            source.data.eq(data),
            If(source.ready & source.valid,
                NextState("IDLE"),
            )
        )


class LiteSPIPHY(Module,AutoDoc, AutoCSR,  ModuleDoc):
    """LiteSPI PHY instantiator

    The ``LiteSPIPHY`` class instantiate generic PHY - ``LiteSPIPHYCore`` that can be connected to the ``LiteSPICore``,
    handles optional clock domain wrapping for whole PHY and interfaces streams and CS signal from PHY logic.

    Parameters
    ----------
    pads : Object
        SPI pads description.

    flash : SpiNorFlashModule
        SpiNorFlashModule configuration object.

    device : str
        Device type for use by the ``LiteSPIClkGen``.

    clock_domain : str
        Name of LiteSPI clock domain.

    default_divisor : int
        Default frequency divisor for clkgen.

    Attributes
    ----------
    source : Endpoint(spi_phy_data_layout), out
        Data stream from ``LiteSPIPHYCore``.

    sink : Endpoint(spi_phy_ctl_layout), in
        Control stream from ``LiteSPIPHYCore``.

    cs_n : Signal(), in
        Flash CS signal from ``LiteSPIPHYCore``.
    """

    def __init__(self, pads, flash, device="xc7", clock_domain="sys", default_divisor=9):
        self.phy = LiteSPIPHYCore(pads, flash, device, clock_domain, default_divisor)

        self.source         = self.phy.source
        self.sink           = self.phy.sink
        self.cs_n           = self.phy.cs_n

        if clock_domain is not "sys":
            self.clock_domains.cd_litespi = ClockDomain()
            self.phy = ClockDomainsRenamer("litespi")(self.phy)
            self.comb += self.cd_litespi.clk.eq(ClockSignal(clock_domain))
            self.comb += self.cd_litespi.rst.eq(ResetSignal(clock_domain))

        self.submodules.spiflash_phy = self.phy

    def get_csrs(self):
        return self.spiflash_phy.get_csrs()
