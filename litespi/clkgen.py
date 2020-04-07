from migen import *

from litex.soc.integration.doc import AutoDoc, ModuleDoc


class LiteSPIClkGen(Module, AutoDoc, ModuleDoc):
    """SPI Clock generator

    The ``LiteSPIClkGen`` class provides a generic SPI clock generator.

    It supports accessing CLK pin on a reserved pin by instantiating device specific modules (currently 7 Series only).

    Parameters
    ----------
    pads : Object
        SPI pads description.

    device : str
        Device type for determining how to get output pin if it was not provided in pads.

    cnt_width : int
        Width of the internal counter ``cnt`` used for dividing the clock.

    with_ddr : bool
        Generate additional ``sample`` and ``update`` signals.

    Attributes
    ----------
    div : Signal(8), in
        Clock divisor, output clock frequency will be equal to ``sys_clk_freq/(2*(1+div))``.

    posedge : Signal(), out
        Outputs 1 when there is a rising edge on the generated clock, 0 otherwise.

    negedge : Signal(), out
        Outputs 1 when there is a falling edge on the generated clock, 0 otherwise.

    en : Signal(), in
        Clock enable input, output clock will be generated if set to 1, 0 resets the core.

    sample : Signal(), out
        Outputs 1 when ``sample_cnt==cnt``, can be used to sample incoming DDR data.

    sample_cnt : Signal(8), in
        Controls generation of the ``sample`` signal.

    update : Signal(), out
        Outputs 1 when ``update_cnt==cnt``, can be used to update outgoing DDR data.

    update_cnt : Signal(8), in
        Controls generation of the ``update`` signal.
    """
    def __init__(self, pads, device, cnt_width=8, with_ddr=False):
        self.div        = div        = Signal(cnt_width)
        self.sample_cnt = sample_cnt = Signal(cnt_width)
        self.update_cnt = update_cnt = Signal(cnt_width)
        self.posedge    = posedge    = Signal()
        self.negedge    = negedge    = Signal()
        self.sample     = sample     = Signal()
        self.update     = update     = Signal()
        self.en         = en         = Signal()
        cnt             = Signal(cnt_width)
        clk             = Signal()

        self.comb += [
            posedge.eq(~clk & (cnt == div)),
            negedge.eq(clk & (cnt == div)),
            sample.eq(cnt == sample_cnt),
            update.eq(cnt == update_cnt),
        ]

        self.sync += [
            If(en,
                If(cnt < div,
                    cnt.eq(cnt+1),
                ).Else(
                    cnt.eq(0),
                    clk.eq(~clk),
                )
            ).Else(
                clk.eq(0),
                cnt.eq(0),
            )
        ]

        if not hasattr(pads, "clk"):
            pads.clk = Signal()
            if device == "xc7":
                e2_clk = Signal()
                e2_net = Signal()
                e2_cnt = Signal(4)
                self.specials += Instance("STARTUPE2",
                    i_CLK=0,
                    i_GSR=0,
                    i_GTS=0,
                    i_KEYCLEARB=0,
                    i_PACK=0,
                    i_USRCCLKO=e2_net,
                    i_USRCCLKTS=0,
                    i_USRDONEO=1,
                    i_USRDONETS=1,
                )
                # startupe2 needs 3 usrcclko cycles to switch over to user clock
                self.comb += If(e2_cnt == 6,
                                 e2_net.eq(pads.clk)
                             ).Else(
                                 e2_net.eq(e2_clk)
                             )
                self.sync += If(e2_cnt < 6,
                                 e2_cnt.eq(e2_cnt+1),
                                 e2_clk.eq(~e2_clk)
                             )
            else:
                raise NotImplementedError

        self.comb += pads.clk.eq(clk)
