from migen import *
from migen.genlib.fsm import FSM, NextState

from litespi.clkgen import LiteSPIClkGen
from litespi.common import *

from litex.soc.interconnect import stream

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


class LiteSPIPHY(Module, AutoDoc, ModuleDoc):
    """Generic LiteSPI PHY

    The ``LiteSPIPHY`` class provides a generic PHY that can be connected to the ``LiteSPICore``.

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

    Attributes
    ----------
    source : Endpoint(spi_phy_data_layout), out
        Data stream.

    sink : Endpoint(spi_phy_ctl_layout), in
        Control stream.

    cs_n : Signal(), in
        Flash CS signal.

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

    def __init__(self, pads, flash, device="xc7"):
        self.source = source = stream.Endpoint(spi_phy_data_layout)
        self.sink   = sink   = stream.Endpoint(spi_phy_ctl_layout)

        self.cs_n     = Signal()

        if hasattr(pads, "miso"):
            bus_width = 1
            pads.dq = [pads.mosi, pads.miso]
        else:
            bus_width = len(pads.dq)

        assert bus_width in [1, 2, 4, 8]

        # Check if number of pads matches configured mode
        assert flash.check_bus_width(bus_width)

        addr_bits = flash.addr_bits
        dummy_bits = flash.dummy_bits if flash.fast_mode else 0
        cmd_width = flash.cmd_width
        addr_width = flash.addr_width
        data_width = flash.bus_width
        command = flash.read_opcode.code
        ddr = flash.ddr

        self.submodules.clkgen = clkgen = LiteSPIClkGen(pads, device, with_ddr=ddr)

        data_bits = 32
        cmd_bits = 8

        self.comb += [
            clkgen.div.eq(2), # TODO: clkgen options should be SoftCPU configurable
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
            self.shift_out(addr_width, len(addr), "DUMMY" if dummy_bits else "IDLE", op=[NextValue(addr, addr<<addr_width)], trigger=clkgen.negedge if not ddr else clkgen.update, ddr=ddr)
        )
        fsm.act("DUMMY",
            If(self.fsm_cnt < 8, dq_oe.eq(addr_oe_mask[addr_width])), # output 0's for the first dummy byte
            self.shift_out(addr_width, dummy_bits, "IDLE"),
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
            source.data.eq(usr_din),
            If(source.ready & source.valid,
                NextState("IDLE"),
            )
        )
        fsm.act("SEND_DATA",
            source.valid.eq(1),
            source.data.eq(data),
            If(source.ready & source.valid,
                NextState("IDLE"),
            )
        )
