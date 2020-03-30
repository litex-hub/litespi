from migen import *
from migen.genlib.fsm import FSM, NextState

from litespi.clkgen import LiteSPIClkGen
from litespi.common import *

from litex.soc.interconnect import stream

# Output enable masks for the tri-state buffers, data mode mask is not included as oe pins default to 0
cmd_oe_mask = 0b0001
soft_oe_mask = 0b0001
addr_oe_mask = {
    1: 0b0001,
    2: 0b0011,
    4: 0b1111,
}

def GetConfig(flash=None):
    if flash is None:
        # TODO: replace with a named tuple/configuration object
        # addr_bits, dummy_bits, cmd_width, addr_width, data_width, command
        return (24, 8, 1, 1, 1, 0x0b)

class LiteSPIPHY(Module):
    """Generic LiteSPI PHY

    The ``LiteSPIPHY`` class provides a generic PHY that can be connected to the ``LiteSPICore``.

    It supports single/dual/quad output reads from the flash chips.

    Parameters
    ----------
    pads : Object
        SPI pads description.

    flash : FlashModule
        FlashModule configuration object or None, if None is provided then the default configuration is used.

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
    def shift_out(self, width, bits, next_state, negedge_op=None, posedge_op=None):
        res = [
            self.clkgen.en.eq(1),
            If(self.clkgen.negedge,
                NextValue(self.fsm_cnt, self.fsm_cnt+width),
                If(self.fsm_cnt == (bits-width),
                    NextValue(self.fsm_cnt, 0),
                    NextState(next_state),
                ),
            ),
        ]

        if negedge_op is not None:
            res += [If(self.clkgen.negedge, *negedge_op)]

        if posedge_op is not None:
            res += [If(self.clkgen.posedge, *posedge_op)]

        return res

    def __init__(self, pads, flash=None, device="xc7"):
        self.source = source = stream.Endpoint(spi_phy_data_layout)
        self.sink   = sink   = stream.Endpoint(spi_phy_ctl_layout)

        self.cs_n     = Signal()

        self.submodules.clkgen = clkgen = LiteSPIClkGen(pads, device)

        addr_bits, dummy_bits, cmd_width, addr_width, data_width, command = GetConfig(flash)

        data_bits = 32
        cmd_bits = 8

        self.comb += [
            clkgen.div.eq(2), # should be SoftCPU configurable
            pads.cs_n.eq(self.cs_n),
            pads.clk.eq(clkgen.clk),
        ]

        if hasattr(pads, "miso"):
            bus_width = 1
            pads.dq = [pads.mosi, pads.miso]
        else:
            bus_width = len(pads.dq)

        assert bus_width in [1, 2, 4]

        dq_o  = Signal(len(pads.dq))
        dq_i  = Signal(len(pads.dq))
        dq_oe = Signal(len(pads.dq))

        for i in range(len(pads.dq)):
            t = TSTriple()
            self.specials += t.get_tristate(pads.dq[i])
            self.comb += [
                dq_i[i].eq(t.i),
                t.o.eq(dq_o[i]),
                t.oe.eq(dq_oe[i]),
            ]

        self.fsm_cnt = Signal(max=31)
        addr         = Signal(addr_bits)
        data         = Signal(data_bits)
        cmd          = Signal(cmd_bits)

        self.submodules.fsm = fsm = FSM(reset_state="IDLE")
        fsm.act("IDLE",
            sink.ready.eq(1),
            If(sink.ready & sink.valid,
                If(sink.cmd, # command request
                    NextValue(addr, sink.addr),
                    NextValue(cmd, command),
                    NextState("CMD"),
                ).Else( # data request
                    NextState("DATA"),
                ),
            ),
        )
        fsm.act("CMD",
            dq_oe.eq(cmd_oe_mask),
            dq_o.eq(cmd[-1] if cmd_width == 1 else cmd[-cmd_width:]),
            self.shift_out(cmd_width, cmd_bits, "ADDR", negedge_op=[NextValue(cmd, cmd<<cmd_width)]),
        )
        fsm.act("ADDR",
            dq_oe.eq(addr_oe_mask[addr_width]),
            dq_o.eq(addr[-1] if addr_width == 1 else addr[-addr_width:]),
            self.shift_out(addr_width, addr_bits, "DUMMY", negedge_op=[NextValue(addr, addr<<addr_width)]),
        )
        fsm.act("DUMMY",
            self.shift_out(addr_width, dummy_bits, "IDLE"),
        )
        fsm.act("DATA",
            self.shift_out(data_width, data_bits, "SEND_DATA", posedge_op=[NextValue(data, Cat(dq_i[1] if data_width == 1 else dq_i[0:data_width], data))]),
        )
        fsm.act("SEND_DATA",
            source.valid.eq(1),
            source.data.eq(data),
            If(source.ready & source.valid,
                NextState("IDLE"),
            )
        )
