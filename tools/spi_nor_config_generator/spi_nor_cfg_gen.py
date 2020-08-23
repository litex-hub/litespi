#!/usr/bin/env python3

#
# This file is part of LiteSPI
#
# Copyright (c) 2020 Antmicro <www.antmicro.com>
# SPDX-License-Identifier: BSD-2-Clause

import argparse
import json
import os
import sys
import re
from git import Git, Repo
import progressbar
import time
from multiprocessing import Process
import subprocess
from linux_spi_nor_extract import linux_extract
from override_cfg import override_chip_cfg
from flash_module_template import generate_class
from pull_flashrom_data import dump_flashrom_data

from litespi.ids import SpiNorFlashManufacturerIDs as ManIDs
from litespi.opcodes import SpiNorFlashOpCodes

# This file produces JSONs with SPI NOR configs from Flashrom,
# OpenOCD and Linux SPI NOR driver and generate Python file with classes.

supported_modules = {
        'linux' : {
            'url' : 'https://github.com/torvalds/linux.git',
            'patch' : None,
            'build_cmds' : ['make'],
            'build_path' : 'src',
            'gen_cmd' : ['./json_gen', 'cfgs.json']
        },
        # Flashrom has a separate tool to extract data: 'pull_flashrom_data.py'
        'flashrom' : {},
        'openocd' : {
            'url' : 'https://git.code.sf.net/p/openocd/code',
            'patch' : 'openocd_json_gen.patch',
            'build_cmds' : ['./bootstrap', './configure', 'make'],
            'build_path' : 'openocd',
            'gen_cmd' : ['./src/openocd', '--dump_json', 'cfgs.json']
        },
}


class LogInfo(object):
    def __init__(self):
        rows, columns = os.popen('stty size', 'r').read().split()
        self.term_width = int(columns)
        self.stage_separator = "=" * self.term_width

    def std_print(self, string):
        print(string)

    def stage_print(self, string):
        print(self.stage_separator)
        print(string)
        print(self.stage_separator)

    def mark_done(self, string):
        print('\x1b[1A', end='\r')
        print(string + '[DONE]')

    def clear_line(self):
        print('\x1b[2K', end='\r')


class Progress(object):
    def _infinity(self):
        val = 0
        while True:
            yield val
            val += 1

    def _progress_func(self):
        widget = [progressbar.BouncingBar()]
        bar = progressbar.ProgressBar(widgets=widget)
        while True:
            for i in bar(self._infinity()):
                time.sleep(0.1)

    def start(self):
        self.proc = Process(target=self._progress_func,)
        self.proc.start()

    def stop(self):
        self.proc.terminate()


def prepare_modules(logger, bar, update):
    for module in supported_modules:
        if module == 'flashrom':
            continue
        if os.path.exists(module):
            if update:
                r = Repo(module)
                # Remove patches to avoid conflicts
                prepare_info = ('Updating repository: %s (%s)' % (module,
                    supported_modules[module]['url']))
                bar.start()
                logger.std_print(prepare_info)
                if supported_modules[module]['patch'] is not None:
                    r.git.execute(['git', 'reset', '--hard', 'HEAD^'])

                r.git.execute(['git', 'pull'])

                # Patch again after pull
                if supported_modules[module]['patch'] is not None:
                    r.git.execute(['git', 'am',
                        os.path.realpath(supported_modules[module]['patch'])])
                bar.stop()
                logger.clear_line()
                logger.mark_done(prepare_info)
                continue
            else:
                continue
        prepare_info = ('Cloning repository: %s (%s)' % (module,
            supported_modules[module]['url']))
        bar.start()
        logger.std_print(prepare_info)
        if module == 'linux':
            # Shallow clone Linux
            r = Repo.clone_from(supported_modules[module]['url'], module, depth=1)
        else:
            r = Repo.clone_from(supported_modules[module]['url'], module)
        if supported_modules[module]['patch'] is not None:
            r.git.execute(['git', 'am',
                os.path.realpath(supported_modules[module]['patch'])])
        bar.stop()
        logger.clear_line()
        logger.mark_done(prepare_info)

    # For Linux we need to cut out data from driver and generate new code
    # to extract configs and dump them as JSON
    logger.std_print("Generating code from Linux SPI NOR driver")
    linux_extract()


def build_modules(logger, bar, nproc):
    logfile = open('build.log', 'w')
    os.environ['LIBS'] = '-ljson-c'
    for module in supported_modules:
        if module == 'flashrom':
            continue
        build_info = ("Building %s..." % (module))
        logger.std_print(build_info)
        bar.start()
        for cmd in supported_modules[module]['build_cmds']:
            exe = [cmd]
            if cmd == 'make':
                exe.append('-j%s' % (nproc))
            b = subprocess.Popen(exe,
                                 cwd=os.path.realpath(
                                     supported_modules[module]['build_path']),
                                 stdout=logfile,
                                 stderr=subprocess.STDOUT)
            exitcode = b.wait()
            if exitcode != 0:
                p.terminate()
                logger.clear_line()
                logger.std_print("Build failed for target %s with exit code %d, please check build.log" % (module, exitcode))
                sys.exit(exitcode)
        bar.stop()
        logger.clear_line()
        logger.mark_done(build_info)


def generate_jsons(logger):
    logfile = open('gen.log', 'w')
    formater_cmd = ['jq', '-c', '.', 'cfgs.json']
    for module in supported_modules:
        gen_info = ("Generating JSON from %s..." % (module))
        logger.std_print(gen_info)
        if module != 'flashrom':
            b = subprocess.Popen(supported_modules[module]['gen_cmd'],
                                 cwd=os.path.realpath(
                                     supported_modules[module]['build_path']),
                                 stdout=logfile,
                                 stderr=subprocess.STDOUT)
            exitcode = b.wait()
            if exitcode != 0:
                logger.std_print("JSON generation failed for target %s" % (module))
                sys.exit(exitcode)

            with open(module + '.json', 'w') as f:
                b = subprocess.Popen(formater_cmd,
                                     cwd=os.path.realpath(
                                         supported_modules[module]['build_path']),
                                     stdout=f,
                                     stderr=subprocess.STDOUT)
                exitcode = b.wait()
                if exitcode != 0:
                    logger.std_print("JSON formating failed for target %s" % (module))
                    sys.exit(exitcode)
        else:
            # Generate JSON from Flashrom tool
            dump_flashrom_data('flashrom.json', quiet=True)

        logger.mark_done(gen_info)


def separate_names(rawname, mod_var, chip_var):
    lnames = list()
    pattern = ".*\((.*?)\)"
    cutout_pattern = "\(.*?\)"
    if chip_var and not mod_var:
        if len(rawname.split('/')[-1]) < len(rawname.split('/')[0]):
            # variant: .....xx/yy
            lnames.append(rawname.split('/')[0])
            lnames.append("%s%s" %
                (rawname.split('/')[0][:-len(rawname.split('/')[1])],
                 rawname.split('/')[1]))
        else:
            # variant: .....x/.....y
            lnames = rawname.split('/')
    elif not chip_var and mod_var:
        # variant: .....(x)
        var = re.search(pattern, rawname).group(1)
        lnames.append(rawname.split('(')[0])
        lnames.append(rawname.split('(')[0] + var)
    else:
        # variants: .....(x/y)/.....(z)
        n_mod_var = rawname.count('(')
        pattern = pattern * n_mod_var
        lnames = re.sub(cutout_pattern, '', rawname).split('/')
        for n in range(0, n_mod_var):
            variant = re.search(pattern, rawname).group(n + 1)
            subvariants = variant.split('/')
            if len(subvariants) > 1:
                for sub in subvariants:
                    lnames.append("%s%s" % (lnames[n], sub))
            else:
                lnames.append("%s%s" % (lnames[n], variant))
    return lnames


cmds_ignore_list = list() # Used to skip duplicate exceptions

def generate_supported_commands(entry, logger):
    # Generate list of possible opcodes configurations (1_1_1, 1_2_2, 1_1_4 etc.)
    template = "{cmd_w}_{addr_w}_{data_w}"
    opcodes = ['1_1_1']

    # Check for fast read support
    if entry["fast_read_support"]:
        opcodes.append('1_1_1_FAST')

    for cmdw in entry["cmd_widths"]:
        for addrw in entry["addr_widths"]:
            if entry["dual_support"]:
                opcodes.append(template.format(cmd_w=cmdw,
                                               addr_w=addrw,
                                               data_w=2,))
            if entry["quad_support"]:
                opcodes.append(template.format(cmd_w=cmdw,
                                               addr_w=addrw,
                                               data_w=4,))
            if entry["octal_support"]:
                opcodes.append(template.format(cmd_w=cmdw,
                                               addr_w=addrw,
                                               data_w=8,))

    # Check for DDR support
    if entry["ddr_support"]:
        ddr_ops = list()
        for op in opcodes:
            ddr_ops.append(op + '_DTR')
        opcodes += ddr_ops

    # Check for 4B support
    if entry["addr32_support"]:
        addr32_ops = list()
        for op in opcodes:
            addr32_ops.append(op + '_4B')
        opcodes += addr32_ops

    # Assemble all possible opcodes
    commands = list()

    # READ/PP commands
    for op in opcodes:
        # Generate READ commands
        key = 'READ_' + op
        if key in cmds_ignore_list:
            continue
        if hasattr(SpiNorFlashOpCodes, key):
            commands.append('SpiNorFlashOpCodes.' + key)
        else:
            msg = ("""Command ``%s`` not implemented!
Please add it to litespi.opcodes or ignore it.
Skipping command ``%s`` ...\n""" % (key, key))
            logger.std_print(msg)
            cmds_ignore_list.append(key)
            continue

        # Generate PP commands
        key = 'PP_' + op
        if key in cmds_ignore_list:
            continue
        if hasattr(SpiNorFlashOpCodes, key):
            commands.append('SpiNorFlashOpCodes.' + key)
        else:
            msg = ("""Command ``%s`` not implemented!
Please add it to litespi.opcodes or ignore it.
Skipping command ``%s`` ...\n""" % (key, key))
            logger.std_print(msg)
            cmds_ignore_list.append(key)
            continue

    return commands


def generate_final(logger, output_class):
    # Merge JSONs
    all_entries = list()
    for module in supported_modules:
        with open(module + '.json') as json_file:
            for entry in json_file:
                data = json.loads(entry)
                all_entries.append(data)

    # Separate variations (e.g. w25q128fv/w25q128jv) into individual entries
    plain_all_entries = list()
    for entry in all_entries:
        model_var = ('(' in entry["chip_name"])
        chip_var = ('/' in entry["chip_name"])
        if not model_var and not chip_var:
            # No variations
            plain_all_entries.append(entry)
            continue
        lnames = separate_names(entry["chip_name"], model_var, chip_var)
        for name in lnames:
            new_entry = dict()
            for key in entry:
                if key == "chip_name":
                    new_entry[key] = name
                else:
                    new_entry[key] = entry[key]
            plain_all_entries.append(new_entry)

    # Search for duplicates
    seen_id = set()
    seen_name = set()
    seen_vendor = set()
    uniqs = list()
    for entry in plain_all_entries:
        if entry["id"] not in seen_id and entry["chip_name"] not in seen_name:
            uniqs.append(entry)
            seen_id.add(entry["id"])
            seen_name.add(entry["chip_name"])
        elif entry["chip_name"] not in seen_name:
            duplicate = False
            # Check if it has '.' characters so we can treat them as regex
            if '.' in entry["chip_name"]:
                pattern = re.compile(entry["chip_name"])
                for u in uniqs:
                    result = pattern.match(u["chip_name"])
                    if result != None:
                        duplicate = True
                        break

            if not duplicate:
                uniqs.append(entry)
                seen_name.add(entry["chip_name"])

    # Convert to enums
    for entry in uniqs:
        entry["device_id"] = ((entry["id"] >> 24) & 0xFFFF)
        vendor_id = ((entry["id"] >> 40) & 0xFFFF)
        if vendor_id == 0x7F:
            # Continuation code -> VID is actually in Device ID part
            entry["device_id"] = (entry["device_id"] & 0xFF)
            vendor_id = (entry["device_id"] >> 8)

        try:
            entry["vendor_id"] = ManIDs(vendor_id)
        except:
            logger.std_print("""\
Vendor id: 0x{vid:04x} does not exist in SpiNorFlashManufacturerIDs enum.
Check vendor ID for {name}""".format(vid=vendor_id, name=entry["chip_name"]))
            raise
        del entry["id"]
        entry["total_pages"] = int(entry["total_size"] / entry["page_size"])
        # Set defaults (override them in next step if needed)
        entry["dummy_bits"] = 8
        entry["addr_widths"] = [1]
        entry["ddr_support"] = False
        entry["cmd_widths"] = [1]


    # Override config if possible and generate supported opcodes
    for entry in uniqs:
        # Override configs
        if entry["chip_name"] in override_chip_cfg.keys():
            for key in override_chip_cfg[entry["chip_name"]]:
                entry[key] = override_chip_cfg[entry["chip_name"]][key]

        entry["supported_commands"] = generate_supported_commands(entry, logger)

    with open(output_class, "w") as pyfile:
        pyfile.write("""# Generated using 'spi_nor_cfg_gen.py'
from litespi.spi_nor_flash_module import SpiNorFlashModule
from litespi.opcodes import SpiNorFlashOpCodes
from litespi.ids import SpiNorFlashManufacturerIDs


""")
        uniqs = sorted(uniqs, key=lambda k: k['chip_name'])
        for entry in uniqs:
            pyfile.write(generate_class(entry["vendor_id"],
                                        entry["device_id"],
                                        entry["chip_name"],
                                        entry["total_size"],
                                        entry["page_size"],
                                        entry["total_pages"],
                                        entry["dummy_bits"],
                                        entry["supported_commands"]
                                        )
                        )

    logger.std_print("Python SPI NOR modules generated to %s" % (output_class))


def main():
    parser = argparse.ArgumentParser(description='''\
This tool downloads modules:
Flashrom, OpenOCD, Linux SPI NOR driver, patches them
and use JSONs generated from them to generate Python classes
used later on to configure LiteX SPI NOR controller.''')
    parser.add_argument('--modules-out', required=True, action='store',
            help='Generate Python modules.')
    parser.add_argument('--nproc', required=False, action='store',
            help='Number of jobs to use.')
    parser.add_argument('--update-modules', required=False, action='store_true',
            help='Update cloned modules.')

    args = parser.parse_args()

    bar = Progress()
    logger = LogInfo()

    output_class = ("%s.py" % (args.modules_out))

    logger.stage_print("Prepare modules")
    prepare_modules(logger, bar, args.update_modules)
    logger.stage_print("Build modules")
    build_modules(logger, bar, args.nproc)
    logger.stage_print("Generate JSONs")
    generate_jsons(logger)
    logger.stage_print("Create modules")
    generate_final(logger, output_class)

if __name__ == "__main__":
    main()
