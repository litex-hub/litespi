#
# This file is part of LiteSPI
#
# Copyright (c) 2020 Antmicro <www.antmicro.com>
# SPDX-License-Identifier: BSD-2-Clause

from collections import namedtuple

from litespi.spi_nor_features import SpiNorFeatures
from litespi.opcodes import SpiNorFlashOpCodes
from litespi.spi_nor_flash_metasizes import MetaSizes


SpiNorFlashEraseCommand = namedtuple("SpiNorFlashEraseCommand", "opcode size addr_bits")


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
        Preferred erase opcode. When omitted, the first command from ``erase_commands`` is used.

    erase_commands : list of SpiNorFlashEraseCommand
        Ordered erase operations supported by the chip. Each entry describes the opcode, erase
        size in bytes, and address length in bits. The first entry is preferred by default.

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

    erase_size : int or None
        number of bytes erased by ``erase_opcode``

    erase_addr_bits : int or None
        number of address bits sent with ``erase_opcode``

    erase_commands : tuple of SpiNorFlashEraseCommand
        normalized erase operations supported by the chip

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


        self.cmd_width  = int(cfg.cmd_width)
        self.addr_width = int(cfg.addr_width)
        self.bus_width  = int(cfg.data_width)

        self.fast_mode = "FAST" in cfg.name or self.bus_width > 1

        self._read_opcode = read_cmd

    def check_bus_width(self, width):
        return width >= self.bus_width

    @staticmethod
    def _legacy_erase_command(opcode, total_size):
        geometries = {
            SpiNorFlashOpCodes.BE_256       : (       256, 24),
            SpiNorFlashOpCodes.BE_4K        : (  4 * 1024, 24),
            SpiNorFlashOpCodes.BE_4K_PMC    : (  4 * 1024, 24),
            SpiNorFlashOpCodes.BE_32K       : ( 32 * 1024, 24),
            SpiNorFlashOpCodes.SE           : ( 64 * 1024, 24),
            SpiNorFlashOpCodes.BE_4K_4B     : (  4 * 1024, 32),
            SpiNorFlashOpCodes.BE_32K_4B    : ( 32 * 1024, 32),
            SpiNorFlashOpCodes.SE_4B        : ( 64 * 1024, 32),
            SpiNorFlashOpCodes.CHIP_ERASE   : (total_size, 0),
            SpiNorFlashOpCodes.CHIP_ERASE_ALT   : (total_size, 0),
            SpiNorFlashOpCodes.CHIP_ERASE_ATMEL : (total_size, 0),
        }
        if opcode not in geometries:
            raise ValueError("Erase geometry is required for command %s" % (str(opcode),))
        size, addr_bits = geometries[opcode]
        return SpiNorFlashEraseCommand(opcode, size, addr_bits)

    def _configure_erase(self, erase_cmd, erase_commands):
        class_commands = getattr(type(self), "erase_commands", None)
        if erase_commands is None:
            erase_commands = class_commands

        # Preserve the historical 64-KiB/SE behavior for modules that do not yet provide erase
        # geometry. Explicit legacy opcodes are translated when their geometry is unambiguous.
        if erase_commands is None:
            opcode = SpiNorFlashOpCodes.SE if erase_cmd is None else erase_cmd
            erase_commands = [self._legacy_erase_command(opcode, self.total_size)]

        normalized = []
        for command in erase_commands:
            if not isinstance(command, SpiNorFlashEraseCommand):
                try:
                    command = SpiNorFlashEraseCommand(*command)
                except (TypeError, ValueError):
                    raise ValueError("Invalid SPI NOR erase command descriptor: %r" % (command,))
            if not isinstance(command.size, int) or command.size <= 0:
                raise ValueError("SPI NOR erase size must be a positive integer")
            if command.addr_bits not in [0, 24, 32]:
                raise ValueError("SPI NOR erase address length must be 0, 24, or 32 bits")
            normalized.append(command)

        self.erase_commands = tuple(normalized)
        if not normalized:
            if erase_cmd is not None:
                raise ValueError("Cannot select an erase command on a non-erasable module")
            self.erase_command   = None
            self.erase_opcode    = None
            self.erase_size      = None
            self.erase_addr_bits = None
            return

        if erase_cmd is None:
            selected = normalized[0]
        else:
            selected = next((command for command in normalized if command.opcode == erase_cmd), None)
            if selected is None:
                raise ValueError("Erase command (%s) has no geometry for chip %s!" %
                    (str(erase_cmd), self.name))

        self.erase_command   = selected
        self.erase_opcode    = selected.opcode
        self.erase_size      = selected.size
        self.erase_addr_bits = selected.addr_bits

    def _configure_chip(self, default_read_cmd, erase_cmd, erase_commands, program_cmd):
        # Check if commands on the list are supported
        for cmd in self.read_cmds:
            if cmd not in self.supported_opcodes:
                raise ValueError("""\
Read command (%s) not supported in chip %s!""" % (str(cmd), self.name))

        # Check if program command is supported
        if program_cmd not in self.supported_opcodes:
            raise ValueError("Programm command (%s) not supported in chip %s!" % (str(program_cmd), self.name))

        # Set commands
        self.read_opcode = default_read_cmd
        self.program_opcode = program_cmd
        self._configure_erase(erase_cmd, erase_commands)

    def __init__(self, default_read_cmd,
                 read_cmds=None,
                 program_cmd=SpiNorFlashOpCodes.PP_1_1_1,
                 erase_cmd=None,
                 erase_commands=None):
        # Check if mandatory attributes are set by an inheritor
        assert hasattr(self, 'manufacturer_id')
        assert hasattr(self, 'device_id')
        assert hasattr(self, 'name')
        assert hasattr(self, 'total_size')
        assert hasattr(self, 'page_size')
        assert hasattr(self, 'total_pages')
        assert hasattr(self, 'supported_opcodes')
        assert hasattr(self, 'dummy_bits') or hasattr(self, 'dummy_cycles')

        if read_cmds is None:
            read_cmds = []
        # Make sure default read command is on the list
        if default_read_cmd not in read_cmds:
            read_cmds.append(default_read_cmd)

        self.read_cmds = read_cmds

        if hasattr(self, "dummy_cycles"):
            if isinstance(self.dummy_cycles, dict):
                self.dummy_cycles = self.dummy_cycles.get(default_read_cmd, self.dummy_bits if hasattr(self, 'dummy_bits') else 0)
        else:
            self.dummy_cycles = self.dummy_bits

        # Configure a chip using provided default_read_cmd
        self._configure_chip(default_read_cmd,
                             erase_cmd,
                             erase_commands,
                             program_cmd)
