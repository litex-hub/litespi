#
# This file is part of LiteSPI
#
# Copyright (c) 2020 Antmicro <www.antmicro.com>
# SPDX-License-Identifier: BSD-2-Clause


from litespi.spi_nor_features import SpiNorFeatures
from litespi.opcodes import SpiNorFlashOpCodes
from litespi.spi_nor_flash_metasizes import MetaSizes


class SpiNorFlashModule(metaclass=MetaSizes):
    """SPI NOR flash module

    The ``SpiNorFlashModule`` class provides an essential information about chip capabilities
    along with supported commands.

    Parameters
    ----------
    default_read_cmd : SpiNorFlashOpCode
        Default user defined read command also used to
        configure a chip into initial desired mode.

    read_cmds : list of SpiNorFlashOpCode
        List of read commands that can be used by SPI NOR controller
        default: default_read_cmd

    program_cmd : SpiNorFlashOpCode
        User defined program command.
        default: PP_1_1_1 (single mode page program)

    erase_cmd : SpiNorFlashOpCode
        User defined erase command. Default value is Sector Erase.
        default: SE (sector erase)

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

    addr_width : int
        number of lines used to send address

    addr_bits : int
        number of address bits (24 or 32)

    supported_opcodes : list of SpiNorFlashOpCode
        list of supported opcodes (READ/PP)

    dummy_bits : int
        number of dummy bits to send needed for a correct transfer

    fast_mode : bool
        chip configured in fast mode
        True -> dummy_bits used
        False -> no dummy_bits

    cmd_width : int
        number of lines used to send command

    read_cmds : list of SpiNorFlashOpCode
        list of available read commands

    program_opcode : SpiNorFlashOpCode
        command used to program the memory

    erase_opcode : SpiNorFlashOpCode
        command used to erase the memory

    bus_width : int
        expected number of data lines

    ddr : bool
        setup module to run in DDR mode

    Properties
    ----------
    read_opcode : SpiNorFlashOpCode
        command used to read the memory
        as well as configures chip into desired mode
    """

    @property
    def read_opcode(self):
        return self._read_opcode

    @read_opcode.setter
    def read_opcode(self, read_cmd):
        """read opcode

        Property ``read_opcode`` defines chip mode,
        hence follwing attributes are set:

            * cmd_width
            * addr_width
            * bus_width
            * addr_bits
            * ddr
        """

        cfg = SpiNorFlashOpCodes()
        cfg.name = SpiNorFlashOpCodes.name_from_value(SpiNorFlashOpCodes, read_cmd)

        self.ddr = "DTR" in cfg.name
        if "4B" in cfg.name:
            self.addr_bits = 32
        else:
            self.addr_bits = 24


        self.cmd_width = int(cfg.cmd_width)
        self.addr_width = int(cfg.addr_width)
        self.bus_width = int(cfg.data_width)

        self.fast_mode = "FAST" in cfg.name or self.bus_width > 1

        self._read_opcode = read_cmd

    def check_bus_width(self, width):
        return width >= self.bus_width

    def _configure_chip(self, default_read_cmd,
                        erase_cmd,
                        program_cmd):
        # Check if commands on the list are supported
        for cmd in self.read_cmds:
            if cmd not in self.supported_opcodes:
                raise ValueError("""\
Read command (%s) not supported in chip %s!""" % (str(cmd), self.name))

        # Check if program command is supported
        if program_cmd not in self.supported_opcodes:
            raise ValueError("Read command (%s) not supported in chip %s!" % (str(read_cmd), self.name))

        # Set commands
        self.read_opcode = default_read_cmd
        self.program_opcode = program_cmd
        self.erase_opcode = erase_cmd

    def __init__(self, default_read_cmd,
                 read_cmds=[],
                 program_cmd=SpiNorFlashOpCodes.PP_1_1_1,
                 erase_cmd=SpiNorFlashOpCodes.SE):
        # Check if mandatory attributes are set by an inheritor
        assert hasattr(self, 'manufacturer_id')
        assert hasattr(self, 'device_id')
        assert hasattr(self, 'name')
        assert hasattr(self, 'total_size')
        assert hasattr(self, 'page_size')
        assert hasattr(self, 'total_pages')
        assert hasattr(self, 'supported_opcodes')
        assert hasattr(self, 'dummy_bits')

        # Make sure default read command is on the list
        if default_read_cmd not in read_cmds:
            read_cmds.append(default_read_cmd)

        self.read_cmds = read_cmds

        # Configure a chip using provided default_read_cmd
        self._configure_chip(default_read_cmd,
                             erase_cmd,
                             program_cmd)
