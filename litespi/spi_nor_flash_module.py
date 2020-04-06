from litespi.spi_nor_features import SpiNorFeatures
from litespi.opcodes import SpiNorFlashOpCodes


class MetaSizes(type):
    def _table(self, mod_name, name):
        size_name  = "{}_size".format(name)
        total_name = "total_{}s".format(name)
        ts_name    = "total_size"

        provided_size_per_unit   = getattr(self, "provided_"+size_name)
        provided_number_of_units = getattr(self, "provided_"+total_name)
        provided_total_size      = getattr(self, "provided_total_size")

        size_per_unit   = getattr(self, size_name)
        number_of_units = getattr(self, total_name)
        total_size = self.total_size

        calc_size_per_unit   = int(total_size / number_of_units)
        calc_number_of_units = int(total_size / size_per_unit)
        calc_total_size      = int(size_per_unit * number_of_units)

        def check(a, b):
            if a is not None and a != b:
                return '!='
            return '=='

        def si(a, f=str):
            if a is None:
                return ''
            else:
                return f(int(a))

        return """
| {mod_name:14s}                 |     Provided == Calculated   |     Hex    |
|-----------------|--------------|------------------------------|------------|
|   size_per_unit | {size_name_:>12s} | {p_size_:>12s} {size__check} {c_size_:<12s} | {h_size_:>10s} | {p_tsize:>10s} / {p_units:10s} ({ts_name___:>10s} / {total_name:10s})
| number_of_units | {total_name:>12s} | {p_units:>12s} {units_check} {c_units:<12s} | {h_units:>10s} | {p_tsize:>10s} / {p_size_:10s} ({ts_name___:>10s} / {size_name_:10s})
|      total_size | {ts_name___:>12s} | {p_tsize:>12s} {tsize_check} {c_tsize:<12s} | {h_tsize:>10s} | {p_size_:>10s} * {p_units:10s} ({size_name_:>10s} * {ts_name___:10s})
""".format(
    mod_name = mod_name,
    name = name,
    size_name_ = size_name,
    total_name = total_name,
    ts_name___ = ts_name,
    size__check = check(provided_size_per_unit,   calc_size_per_unit  ),
    units_check = check(provided_number_of_units, calc_number_of_units),
    tsize_check = check(provided_total_size,      calc_total_size     ),
    p_size_ = si(provided_size_per_unit),
    p_units = si(provided_number_of_units),
    p_tsize = si(provided_total_size),
    c_size_ = si(calc_size_per_unit),
    c_units = si(calc_number_of_units),
    c_tsize = si(calc_total_size),
    h_size_ = si(calc_size_per_unit, hex),
    h_units = si(calc_number_of_units, hex),
    h_tsize = si(calc_total_size, hex),
)

    def _fix_and_check_sized(self, mod_name, name):
        """Makes sure that XXX_size, XXX_total and total_size match.
        IE If XXX == pages then, page_size * total_pages == total_size
        """
        size_name  = "{}_size".format(name)
        total_name = "total_{}s".format(name)

        provided_size_per_unit   = getattr(self, size_name,    None)
        provided_number_of_units = getattr(self, total_name,   None)
        provided_total_size      = getattr(self, "total_size", None)
        setattr(self, "provided_"+size_name,   provided_size_per_unit)
        setattr(self, "provided_"+total_name,  provided_number_of_units)

        provided = 0
        if provided_size_per_unit is not None:
            provided += 1
        if provided_number_of_units is not None:
            provided += 1
        if provided_total_size is not None:
            provided += 1

        assert provided >= 2, """\
{mod_name}: Must provide two of {name}_size={} (size_per_unit), total_{name}s={} (number_of_units), total_size={}
""".format(provided_size_per_unit, provided_number_of_units, provided_total_size, mod_name=mod_name, name=name)

        if provided_size_per_unit is None:
            size_per_unit = int(provided_total_size / provided_number_of_units)
        else:
            size_per_unit = int(provided_size_per_unit)

        if provided_number_of_units is None:
            number_of_units = int(provided_total_size / provided_size_per_unit)
        else:
            number_of_units = int(provided_number_of_units)

        if provided_total_size is None:
            total_size = int(provided_size_per_unit * provided_number_of_units)
        else:
            total_size = int(provided_total_size)

        setattr(self, size_name,  size_per_unit)
        setattr(self, total_name, number_of_units)

        assert   size_per_unit ==    total_size / number_of_units, self._table(mod_name, name)
        assert number_of_units ==    total_size / size_per_unit,   self._table(mod_name, name)
        assert      total_size == size_per_unit * number_of_units, self._table(mod_name, name)
        if provided_total_size is not None:
            assert provided_total_size == total_size, """\
{mod_name}: Tried to set size to {} but size was already set to {}
""".format(provided_total_size, self.total_size, mod_name=mod_name)

    def __init__(self, name, *args, **kw):
        if name == "SpiNorFlashModule":
           return
        setattr(self, "provided_total_size", getattr(self, "total_size", None))
        self._fix_and_check_sized(name, "page")
        #self._fix_and_check_sized(name, "sector")
        self.total_size = self.page_size * self.total_pages
        self.table = lambda x: self._table(name, x)


class SpiNorFlashModule(metaclass=MetaSizes):
    """SPI NOR flash module

    The ``SpiNorFlashModule`` class provides an essential information about chip capabilities
    along with supported commands.

    Parameters
    ----------
    spi_nor_cfg : SpiNorConfig
        User defined configuration for a chip.

    Attributes
    ----------
    manufacturer_id : SpiNorFlashManufacturerIDs
        ID of a vendor

    device_id : int
        ID of a chip

    name : str
        name of a chip

    total_size : int
        total size of a chip in bytes

    page_size : int
        page size of a chip in bytes

    total_pages : int
        chip's total number of pages

    supported_modes : SpiNorConfig
        supported access modes of a chip

    addr_width : int
        number of lines used to send address

    addr_bits : int
        number of address bits (24 or 32)

    dummy_bits : int
        number of dummy bits to send needed for a correct transfer

    cmd_width : int
        number of lines used to send command

    read_opcode : SpiNorFlashOpCode
        command used to read the memory

    program_opcode : SpiNorFlashOpCode
        command used to program the memory

    erase_opcode : SpiNorFlashOpCode
        command used to erase the memory

    bus_width : int
        expected number of data lines

    ddr : bool
        setup module to run in DDR mode
    """

    def _configure_transfer_mode(self, cfg):
        """Configure Transfer Mode

        Funtion ``_configure_transfer_mode`` setups fields:

            * addr_bits
            * addr_width
            * bus_width

        according to user defined config and checks if only one
        mode has been selected.

        Arguments
        ---------
        cfg : SpiNorFeatures
            User defined flags used to configure chip into desired mode.

        Return value
        ------------
        bool
            True: correct chip configuration
            False: more than one mode selected (incorrect configuration)
        """

        if SpiNorFeatures.FEATURE_4BA in cfg:
            self.addr_bits = 32
        else:
            self.addr_bits = 24

        # If there is no addr_width config - select addr_width=1
        if SpiNorFeatures.FEATURE_ADDR_WIDTH_1 in cfg:
            self.addr_width = 1
        elif SpiNorFeatures.FEATURE_ADDR_WIDTH_2 in cfg:
            self.addr_width = 2
        elif SpiNorFeatures.FEATURE_ADDR_WIDTH_4 in cfg:
            self.addr_width = 4
        elif SpiNorFeatures.FEATURE_ADDR_WIDTH_8 in cfg:
            self.addr_width = 8
        else:
            self.addr_width = 1

        # Only one transmission mode can be selected
        if SpiNorFeatures.FEATURE_SINGLE in cfg:
            self.bus_width = 1
            return ((SpiNorFeatures.FEATURE_DUAL not in cfg) and
                   (SpiNorFeatures.FEATURE_QPI not in cfg) and
                   (SpiNorFeatures.FEATURE_OCTAL not in cfg))
        elif SpiNorFeatures.FEATURE_DUAL in cfg:
            self.bus_width = 2
            return ((SpiNorFeatures.FEATURE_SINGLE not in cfg) and
                   (SpiNorFeatures.FEATURE_QPI not in cfg) and
                   (SpiNorFeatures.FEATURE_OCTAL not in cfg))
        elif SpiNorFeatures.FEATURE_QPI in cfg:
            self.bus_width = 4
            return ((SpiNorFeatures.FEATURE_SINGLE not in cfg) and
                   (SpiNorFeatures.FEATURE_DUAL not in cfg) and
                   (SpiNorFeatures.FEATURE_OCTAL not in cfg))
        elif SpiNorFeatures.FEATURE_OCTAL in cfg:
            self.bus_width = 8
            return ((SpiNorFeatures.FEATURE_SINGLE not in cfg) and
                   (SpiNorFeatures.FEATURE_DUAL not in cfg) and
                   (SpiNorFeatures.FEATURE_QPI not in cfg))

    def _configure_chip(self, cfg, erase_cmd, program_cmd, ddr_mode):
        if cfg not in self.supported_modes:
            raise ValueError("Configuration (%s) not supported in chip %s!" % (cfg, self.name))
        assert self._configure_transfer_mode(cfg)

        self.cmd_width = 1 # Currently we support only cmd_width=1
        self.ddr = ddr_mode

        # Find out what read command we can use
        addr32 = ''
        fast = ''
        if SpiNorFeatures.FEATURE_4BA in cfg:
            addr32 = '_4B'
        if SpiNorFeatures.FEATURE_SINGLE in cfg:
            if SpiNorFeatures.FEATURE_FAST_READ in cfg:
                fast = '_FAST'
            else:
                self.dummy_bits = 0
                self.read_opcode = getattr(SpiNorFlashOpCodes, "READ%s%s" %
                          (fast, addr32))
        else:
            self.read_opcode = getattr(SpiNorFlashOpCodes, "READ_%d_%d_%d%s" %
                          (self.cmd_width, self.addr_width, self.bus_width, addr32))

        # Set rest of the commands
        self.erase_opcode = erase_cmd
        self.program_opcode = program_cmd

    def __init__(self, spi_nor_cfg=SpiNorFeatures.FEATURE_SINGLE,
                 erase_cmd=SpiNorFlashOpCodes.SE,
                 program_cmd=SpiNorFlashOpCodes.PP,
                 ddr_mode=False):
        # Check if mandatory attributes are set by an inheritor
        assert hasattr(self, 'manufacturer_id')
        assert hasattr(self, 'device_id')
        assert hasattr(self, 'name')
        assert hasattr(self, 'total_size')
        assert hasattr(self, 'page_size')
        assert hasattr(self, 'total_pages')
        assert hasattr(self, 'supported_modes')
        assert hasattr(self, 'dummy_bits')

        # Configure a chip using provided config
        self._configure_chip(spi_nor_cfg, erase_cmd, program_cmd, ddr_mode)

    def check_bus_width(self, width):
        return width == self.bus_width
