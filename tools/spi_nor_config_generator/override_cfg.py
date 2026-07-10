# Some features are not present in the databases parsed by the generator. This is especially true
# for capabilities discovered through SFDP at runtime, or for database entries that intentionally
# describe only a conservative fallback. Keep those corrections here instead of editing
# ``generated_modules.py`` directly so that they survive regeneration.

# Override config template:
# 'chip_name' : {
#   'vendor_id' : SpiNorFlashManufacturerIDs,
#   'device_id' : int,
#   'total_size' : int,
#   'page_size' : int,
#   'total_pages' : int,
#   'dummy_bits' : int,
#   'addr_widths' : list(int), # [1,2,4,8]
#   'cmd_widths' : list(int), # [1,2,4,8]
#   'ddr_support' : bool,
#   'dual_support' : bool,
#   'quad_support' : bool,
#   'octal_support' : bool,
#   'fast_read_support' : bool,
#   'addr32_support' : bool,
#   'supported_opcodes' : list(str),        # Replace the generated opcode list.
#   'supported_opcodes_add' : list(str),    # Append opcodes missing from imported data.
#   'supported_opcodes_remove' : list(str), # Remove opcodes incorrectly inferred from imported data.
#   'dummy_cycles' : dict(str, int),
#   'quad_enable' : str,
# }

from litespi.opcodes import SpiNorFlashOpCode, SpiNorFlashOpCodes


_OUTPUT_OVERRIDE_KEYS = {
    "supported_opcodes",
    "supported_opcodes_add",
    "supported_opcodes_remove",
    "dummy_cycles",
    "quad_enable",
}


def opcode_ref(name):
    """Return the Python source reference for an opcode name, validating it first."""
    prefix = "SpiNorFlashOpCodes."
    if name.startswith(prefix):
        name = name[len(prefix):]
    if (not hasattr(SpiNorFlashOpCodes, name) or
            not isinstance(getattr(SpiNorFlashOpCodes, name), SpiNorFlashOpCode)):
        raise ValueError("Unknown SPI NOR opcode: %s" % name)
    return prefix + name


def apply_source_overrides(entry, override):
    """Apply fields that affect opcode inference before commands are generated."""
    for key, value in override.items():
        if key not in _OUTPUT_OVERRIDE_KEYS:
            entry[key] = value


def apply_output_overrides(entry, override):
    """Apply explicit module attributes after the imported capabilities are interpreted."""
    replace = override.get("supported_opcodes")
    add     = override.get("supported_opcodes_add", [])
    remove  = override.get("supported_opcodes_remove", [])
    if replace is not None and (add or remove):
        raise ValueError("supported_opcodes cannot be combined with additive opcode overrides")

    commands = entry["supported_commands"]
    if replace is not None:
        commands = [opcode_ref(name) for name in replace]
    else:
        remove = {opcode_ref(name) for name in remove}
        commands = [command for command in commands if command not in remove]
        commands.extend(opcode_ref(name) for name in add)

    # Preserve declaration order while avoiding duplicates introduced by overlapping sources or
    # an additive override that has since appeared upstream.
    entry["supported_commands"] = list(dict.fromkeys(commands))

    if "dummy_cycles" in override:
        dummy_cycles = {}
        for name, cycles in override["dummy_cycles"].items():
            if not isinstance(cycles, int) or cycles < 0:
                raise ValueError("Dummy cycles must be a non-negative integer")
            dummy_cycles[opcode_ref(name)] = cycles
        entry["dummy_cycles"] = dummy_cycles

    if "quad_enable" in override:
        quad_enable = override["quad_enable"]
        if not isinstance(quad_enable, str) or not quad_enable:
            raise ValueError("quad_enable must be a non-empty string")
        entry["quad_enable"] = quad_enable


override_chip_cfg = {
        'at25sf161' : {
            'supported_opcodes_add' : [
                'READ_1_1_4',
            ],
        },
        'is25lp128' : {
            'supported_opcodes_add' : [
                'READ_1_1_4',
            ],
        },
        'is25wp512m' : {
            'dual_support' : True,
            'quad_support' : True,
            'supported_opcodes' : [
                'READ_1_1_1',
                'READ_1_1_1_4B',
                'READ_1_1_1_FAST',
                'READ_1_1_1_FAST_4B',
                'READ_1_1_2',
                'READ_1_1_2_4B',
                'READ_1_2_2',
                'READ_1_2_2_4B',
                'READ_1_1_4',
                'READ_1_1_4_4B',
                'READ_4_4_4',
                'READ_4_4_4_4B',
                'PP_1_1_1',
                'PP_1_1_2',
                'PP_1_1_4',
            ],
            'dummy_cycles' : {
                'READ_1_1_1_FAST'    : 8,
                'READ_1_1_1_FAST_4B' : 8,
                'READ_1_1_2'         : 8,
                'READ_1_1_2_4B'      : 8,
                'READ_1_2_2'         : 4,
                'READ_1_2_2_4B'      : 4,
                'READ_1_1_4'         : 8,
                'READ_1_1_4_4B'      : 8,
                'READ_1_4_4'         : 6,
                'READ_1_4_4_4B'      : 6,
                'READ_4_4_4'         : 6,
                'READ_4_4_4_4B'      : 6,
            },
        },
        'mx25lm51245' : {
            'octal_support' : True,
        },
        'mx25r512f' : {
            'dual_support' : True,
            'quad_support' : True,
        },
        'mx25r1035f' :  {
            'dual_support' : True,
            'quad_support' : True,
        },
        'mx25r2035f' :  {
            'dual_support' : True,
            'quad_support' : True,
        },
        'mx25r4035f' :  {
            'dual_support' : True,
            'quad_support' : True,
        },
        'mx25r8035f' :  {
            'dual_support' : True,
            'quad_support' : True,
        },
        'mx25r1635f' :  {
            'dual_support' : True,
            'quad_support' : True,
        },
        'w25q64jv' :  {
            'dual_support' : True,
            'quad_support' : True,
        },
        'gd25q512mc' :  {
            'dual_support' : True,
            'quad_support' : True,
        },
        'is25lp512m' :  {
            'dual_support' : True,
            'quad_support' : True,
        },
        's25fl128l' : {
            'supported_opcodes_add' : [
                'READ_1_4_4',
            ],
        },
        's25fl128s' : {
            'supported_opcodes_add' : [
                'READ_1_1_4',
            ],
        },
        'w25q128jv' : {
            'supported_opcodes_add' : [
                'READ_1_2_2',
                'READ_1_4_4',
            ],
            'dummy_cycles' : {
                'READ_1_2_2' : 0,
                'READ_1_4_4' : 4,
            },
        },
        'w25q256jw' : {
            'supported_opcodes_add' : [
                'READ_1_1_1_4B',
                'READ_1_1_2_4B',
                'READ_1_2_2_4B',
                'READ_1_1_4_4B',
                'READ_1_4_4_4B',
            ],
            'dummy_cycles' : {
                'READ_1_1_2'    : 8,
                'READ_1_1_2_4B' : 8,
                'READ_1_2_2'    : 4,
                'READ_1_2_2_4B' : 4,
                'READ_1_1_4'    : 32,
                'READ_1_1_4_4B' : 32,
                'READ_1_4_4'    : 6,
                'READ_1_4_4_4B' : 6,
            },
        },
}


# These devices use the same vendor-specific quad-enable sequence. The information is not encoded
# by the generic dual/quad capability flags imported by the generator.
for chip_name in [
    'is25lp016d', 'is25lp080d', 'is25lp128', 'is25lp256', 'is25lp512m',
    'is25lq040b', 'is25wp032', 'is25wp064', 'is25wp128', 'is25wp256', 'is25wp512m',
    'mx25l25635e', 'mx25r1035f', 'mx25r1635f', 'mx25r2035f', 'mx25r3235f',
    'mx25r4035f', 'mx25r512f', 'mx25r8035f', 'mx25u12835f', 'mx25u1635e',
    'mx25u3235e', 'mx25u3235f', 'mx25u51245g', 'mx25u6435e', 'mx25v8035f',
    'mx66l1g45g', 'mx66l1g55g', 'mx66l51235l', 'mx66u51235f',
]:
    override_chip_cfg.setdefault(chip_name, {})['quad_enable'] = 'wrsr_sr1_bit6'

for chip_name in [
    's25fl128s', 's25fl128s0', 's25fl128s1', 's25fl256s1', 's25fl512s', 's25fs512s',
]:
    override_chip_cfg.setdefault(chip_name, {})['quad_enable'] = 'wrr_cr1_bit1'
