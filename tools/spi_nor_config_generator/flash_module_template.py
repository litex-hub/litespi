#
# This file is part of LiteSPI
#
# Copyright (c) 2020 Antmicro <www.antmicro.com>
# SPDX-License-Identifier: BSD-2-Clause

from litespi.spi_nor_features import SpiNorFeatures


def generate_class(vendor_id,
                   device_id,
                   chip_name,
                   total_size,
                   page_size,
                   total_pages,
                   dummy_bits,
                   supported_commands,
                   dummy_cycles=None,
                   quad_enable=None):
    name = chip_name.replace('-', '_').replace('.', 'x')
    # Add 'X' character for chip name starting with digit
    if chip_name[0].isdigit():
        name = 'X' + name

    cmds_builder = '[\n        '
    for cmd in supported_commands:
        cmds_builder += ('%s,\n        ' % (cmd))
    cmds_builder = cmds_builder[:-4] + ']'

    optional_attributes = ""
    if quad_enable is not None:
        optional_attributes += '    quad_enable = "{}"\n'.format(quad_enable)

    if dummy_cycles is not None:
        optional_attributes += "\n    dummy_cycles = {\n"
        for opcode, cycles in dummy_cycles.items():
            optional_attributes += "        {}: {},\n".format(opcode, cycles)
        optional_attributes += "    }\n"

    genclass = '''class {pn}(SpiNorFlashModule):

    manufacturer_id = {vid}
    device_id = 0x{did:04x}
    name = "{pfn}"

    total_size  = {ts:10d}   # bytes
    page_size   = {ps:10d}   # bytes
    total_pages = {tp:10d}

    supported_opcodes = {ops}
    dummy_bits = {dbits}
{optional_attributes}


'''.format(
        pn=name.upper(),
        pfn=chip_name,
        vid=vendor_id,
        did=device_id,
        ts=total_size,
        ps=page_size,
        tp=total_pages,
        ops=cmds_builder,
        dbits=dummy_bits,
        optional_attributes=optional_attributes,
    )
    return genclass
