#
# This file is part of LiteSPI
#
# Copyright (c) 2020 Antmicro <www.antmicro.com>
# SPDX-License-Identifier: BSD-2-Clause

from migen import *
from migen.genlib.cdc import MultiReg
from migen.genlib.misc import WaitTimer

from litespi.common import *
from litespi.clkgen import LiteSPIClkGen

from litex.soc.interconnect import stream
from litex.soc.interconnect.csr import *

from litex.build.io import SDRTristate

from litex.soc.integration.doc import AutoDoc, ModuleDoc

# Output enable masks for the tri-state buffers, data mode mask is not included as oe pins default to 0

cmd_oe_mask  = {
    1: 0b00000001,
    2: 0b00000011,
    4: 0b00001111,
    8: 0b11111111,
}
soft_oe_mask = 0b00000001
addr_oe_mask = {
    1: 0b00000001,
    2: 0b00000011,
    4: 0b00001111,
    8: 0b11111111,
}

# LiteSPI PHY Core ---------------------------------------------------------------------------------

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
    source : Endpoint(spi_phy2core_layout), out
        Data stream.

    sink : Endpoint(spi_core2phy_layout), in
        Control stream.

    cs : Signal(), in
        Flash CS signal.

    clk_divisor : CSRStorage
        Register which holds a clock divisor value applied to clkgen.

    dummy_bits : CSRStorage
        Register which hold a number of dummy bits to send during transmission.
    """
    def __init__(self, pads, flash, device, clock_domain, default_divisor, cs_delay):
        self.source              = source = stream.Endpoint(spi_phy2core_layout)
        self.sink                = sink   = stream.Endpoint(spi_core2phy_layout)
        self.cs                  = Signal.like(pads.cs_n)
        self._spi_clk_divisor    = spi_clk_divisor = Signal(8)
        self._spi_dummy_bits     = spi_dummy_bits  = Signal(8)
        if flash.cmd_width == 1:
            self._default_dummy_bits = flash.dummy_bits if flash.fast_mode else 0
        elif flash.cmd_width == 4:
            self._default_dummy_bits = flash.dummy_bits * 3 if flash.fast_mode else 0
        else:
            raise NotImplementedError(f'Command width of {flash.cmd_width} bits is currently not supported!')
        self._default_divisor    = default_divisor

        self.clk_divisor         = clk_divisor     = CSRStorage(8, reset=self._default_divisor)
        self.dummy_bits          = dummy_bits      = CSRStorage(8, reset=self._default_dummy_bits)

        # # #

        if clock_domain != "sys":
            self.specials += MultiReg(clk_divisor.storage, spi_clk_divisor, "litespi")
            self.specials += MultiReg(dummy_bits.storage,  spi_dummy_bits,  "litespi")
        else:
            self.comb += spi_clk_divisor.eq(clk_divisor.storage)
            self.comb += spi_dummy_bits.eq(dummy_bits.storage)
        if hasattr(pads, "miso"):
            bus_width = 1
            pads.dq   = [pads.mosi, pads.miso]
        else:
            bus_width = len(pads.dq)

        assert bus_width in [1, 2, 4, 8]

        # Check if number of pads matches configured mode.
        assert flash.check_bus_width(bus_width)

        addr_bits  = flash.addr_bits
        cmd_width  = flash.cmd_width
        addr_width = flash.addr_width
        data_width = flash.bus_width
        command    = flash.read_opcode.code
        ddr        = flash.ddr

        # For Output modes there is a constant 8 dummy cycles, for I/O and DTR modes there are
        # different number of dummy cycles and in some cases they can be configurable.
        # We control a number of dummy cycles by substracting addr_width value from spi_dummy_bits,
        # so to achieve a proper number of dummy cycles when using shift_out function we need to
        # calculate total dummy bits which depends on addr_width value.
        # NOTE: these values are just default ones, in case chip has different default dummy cycles
        # for these modes or dummy cycles can be configured, please adjust the dummy bits value via
        # CSR in liblitespi accordingly.
        if (addr_width > 1):
            # DTR mode.
            if (ddr):
                if (addr_width == 2):
                    self.default_dummy_bits = 6 * addr_width
                elif (addr_width == 4):
                    self.default_dummy_bits = 8 * addr_width
                else:
                    self.default_dummy_bits = 16 * addr_width
            # I/O mode.
            else:
                if (addr_width == 2):
                    self.default_dummy_bits = 4 * addr_width
                elif (addr_width == 4):
                    self.default_dummy_bits = 6 * addr_width
                else:
                    self.default_dummy_bits = 16 * addr_width

        # Clock Generator.
        self.submodules.clkgen = clkgen = LiteSPIClkGen(pads, device, with_ddr=ddr)
        self.comb += [
            clkgen.div.eq(spi_clk_divisor),
            clkgen.sample_cnt.eq(1),
            clkgen.update_cnt.eq(1),
        ]

        # CS control.
        cs_timer = WaitTimer(cs_delay + 1) # Ensure cs_delay cycles between XFers.
        cs_out   = Signal.like(self.cs)
        self.submodules += cs_timer
        self.comb += [
            cs_timer.wait.eq(self.cs != 0),
            If(cs_timer.done,
                cs_out.eq(self.cs)
            ).Else(
                cs_out.eq(0)
            ),
            pads.cs_n.eq(~cs_out)
        ]

        # I/Os.
        data_bits = 32
        cmd_bits  = 8

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

        # FSM.
        shift_cnt = Signal(8, reset_less=True)
        addr      = Signal(addr_bits if not ddr else addr_bits + addr_width, reset_less=True)
        data      = Signal(data_bits, reset_less=True)
        cmd       = Signal(cmd_bits,  reset_less=True)

        usr_dout  = Signal(len(sink.data),  reset_less=True)
        usr_din   = Signal(len(sink.data),  reset_less=True)
        usr_len   = Signal(len(sink.len),   reset_less=True)
        usr_width = Signal(len(sink.width), reset_less=True)
        usr_mask  = Signal(len(sink.mask),  reset_less=True)

        din_width_cases = {1: [NextValue(usr_din, Cat(dq_i[1], usr_din))]}
        for i in [2, 4, 8]:
            din_width_cases[i] = [NextValue(usr_din, Cat(dq_i[0:i], usr_din))]

        dout_width_cases = {}
        for i in [1, 2, 4, 8]:
            dout_width_cases[i] = [dq_o.eq(usr_dout[-i:])]

        self.submodules.fsm = fsm = FSM(reset_state="IDLE")
        fsm.act("IDLE",
            sink.ready.eq(cs_timer.done),
            If(sink.valid & sink.ready,
                Case(sink.cmd, {
                    CMD: [
                        NextValue(addr, sink.data),
                        NextValue(cmd,  command),
                        NextState("CMD")
                    ],
                    READ: [
                        NextState("DATA")
                    ],
                    USER: [
                        NextValue(usr_dout,  sink.data << (32-sink.len)),
                        NextValue(usr_din,   0),
                        NextValue(usr_len,   sink.len),
                        NextValue(usr_width, sink.width),
                        NextValue(usr_mask,  sink.mask),
                        NextState("USER")
                    ]
                })
            )
        )

        def shift_out(width, bits, next_state, trigger=[], op=[], ddr=False):
            if type(trigger) is not list:
                trigger = [trigger]
                op      = [op]

            edge = self.clkgen.negedge if not ddr else trigger[0]
            res  = [
                self.clkgen.en.eq(1),
                If(edge,
                    NextValue(shift_cnt, shift_cnt+width),
                    If(shift_cnt == (bits-width),
                        NextValue(shift_cnt, 0),
                        NextState(next_state),
                    ),
                ),
            ]

            if len(trigger) == len(op):
                for i in range(len(trigger)):
                    res += [If(trigger[i], *op[i])]

            return res

        fsm.act("CMD",
            dq_oe.eq(cmd_oe_mask[cmd_width]),
            dq_o.eq(cmd[-cmd_width:]),
            shift_out(
                width      = cmd_width,
                bits       = cmd_bits,
                next_state = "ADDR",
                op         = [NextValue(cmd, cmd<<cmd_width)],
                trigger    = clkgen.negedge,
                ddr        = False,
            ),
        )
        fsm.act("ADDR",
            dq_oe.eq(addr_oe_mask[addr_width]),
            dq_o.eq(addr[-addr_width:]),
            If(spi_dummy_bits != 0,
                shift_out(
                    width      = addr_width,
                    bits       = len(addr),
                    next_state = "DUMMY",
                    op         = [NextValue(addr, addr<<addr_width)],
                    trigger    = clkgen.negedge if not ddr else clkgen.update,
                    ddr        = ddr
                )
            ).Else(
                shift_out(
                    width      = addr_width,
                    bits       = len(addr),
                    next_state = "IDLE",
                    op         = [NextValue(addr, addr<<addr_width)],
                    trigger    = clkgen.negedge if not ddr else clkgen.update,
                    ddr        = ddr
                )
            )
        )
        fsm.act("DUMMY",
            If(shift_cnt < 8, dq_oe.eq(addr_oe_mask[addr_width])), # output 0's for the first dummy byte
            shift_out(
                width      = addr_width,
                bits       = spi_dummy_bits,
                next_state = "IDLE"
            ),
        )
        fsm.act("DATA",
            shift_out(
                width      = data_width,
                bits       = data_bits,
                next_state = "DATA_END",
                op         = [NextValue(data, Cat(dq_i[1] if data_width == 1 else dq_i[0:data_width], data))],
                trigger    = clkgen.posedge_reg2 if not ddr else clkgen.sample,
                ddr        = ddr
            )
        )
        fsm.act("DATA_END",
            If(spi_clk_divisor > 0,
                # Last data cycle was already captured in the DATA state.
                NextState("SEND_DATA"),
            ).Elif(clkgen.posedge_reg2,
                # Capture last data cycle.
                NextValue(data, Cat(dq_i[1] if data_width == 1 else dq_i[0:data_width], data)),
                NextState("SEND_DATA"),
            )
        )
        fsm.act("USER",
            dq_oe.eq(usr_mask),
            Case(usr_width, dout_width_cases),
            shift_out(
                width      = usr_width,
                bits       = usr_len,
                next_state = "USER_END",
                trigger    = [
                    clkgen.posedge_reg2, # data sampling
                    clkgen.negedge,      # data update
                ],
                op = [
                    [Case(usr_width, din_width_cases)],
                    [NextValue(usr_dout, usr_dout<<usr_width)],
                ],
                ddr = False)
        )
        fsm.act("USER_END",
            If(spi_clk_divisor > 0,
                # Last data cycle was already captured in the USER state.
                NextState("SEND_USER_DATA"),
            ).Elif(clkgen.posedge_reg2,
                # Capture last data cycle.
                Case(usr_width, din_width_cases),
                NextState("SEND_USER_DATA"),
            )
        )
        fsm.act("SEND_USER_DATA",
            source.valid.eq(1),
            source.last.eq(1),
            source.data.eq(usr_din),
            If(source.ready,
                NextState("IDLE"),
            )
        )
        fsm.act("SEND_DATA",
            source.valid.eq(1),
            source.last.eq(1),
            source.data.eq(data),
            If(source.ready,
                NextState("IDLE"),
            )
        )

# LiteSPI PHY --------------------------------------------------------------------------------------

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
    source : Endpoint(spi_phy2core_layout), out
        Data stream from ``LiteSPIPHYCore``.

    sink : Endpoint(spi_core2phy_layout), in
        Control stream from ``LiteSPIPHYCore``.

    cs : Signal(), in
        Flash CS signal from ``LiteSPIPHYCore``.
    """

    def __init__(self, pads, flash, device="xc7", clock_domain="sys", default_divisor=9, cs_delay=10):
        self.phy = LiteSPIPHYCore(pads, flash, device, clock_domain, default_divisor, cs_delay)

        self.source = self.phy.source
        self.sink   = self.phy.sink
        self.cs     = self.phy.cs

        # # #

        if clock_domain != "sys":
            self.clock_domains.cd_litespi = ClockDomain()
            self.phy = ClockDomainsRenamer("litespi")(self.phy)
            self.comb += self.cd_litespi.clk.eq(ClockSignal(clock_domain))
            self.comb += self.cd_litespi.rst.eq(ResetSignal(clock_domain))

        self.submodules.spiflash_phy = self.phy

    def get_csrs(self):
        return self.spiflash_phy.get_csrs()
