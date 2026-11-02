# AGENTS.md: LiteSPI

SPI/SPI-flash core for LiteX: PHYs (generic, DDR, vendor-specific), memory-mapped (MMAP) and
master frontends, crossbar, SPI NOR module database and flash model, standalone generator.

Read the LiteX agent page first: https://github.com/enjoy-digital/litex/wiki/LiteX-for-AI-Agents (framework map, conventions, how to
verify a change, contribute back). Index of the whole wiki for agents: https://github.com/enjoy-digital/litex/wiki/llms.txt.

## Where things are

- `litespi/phy/`: PHYs; `litespi/core/`: MMAP and master cores; `litespi/crossbar.py`, `clkgen.py`, `cscontrol.py`.
- `litespi/modules/`, `ids.py`, `opcodes.py`, `spi_nor_features.py`: the flash chips database (add a chip there).
- `litespi/flash_model.py`: flash simulation model; `litespi/gen.py` (`litespi_gen`): standalone core; `test/`.

## Verify a change

```sh
python3 -m pytest -v                                                # what CI runs
python3 -m litex_boards.targets.digilent_arty --with-spi-flash --build --no-compile
```

- A new flash chip: add it to the module database with its datasheet IDs/opcodes/features, and
  check the BIOS (`liblitespi`) handles its quad/octal enable.
- MMAP read paths are timing-sensitive on small FPGAs: rebuild the targeted board when changing them.

## Rules

- Style: https://github.com/enjoy-digital/litex/blob/master/doc/coding_style.md (match the
  surrounding file; `module: Description of the change.` commit titles; one change per commit).
- Never edit generated files (`build/`, `csr.h`, `csr.csv`, the Verilog): change the Python.
- One topic per pull request, from the default development branch, with what was tested and on
  which hardware; say that an agent wrote it and who supervised. Do not rename options or
  reformat unrelated code.
- Hardware: never flash a board or write its SPI flash unless the user asked; `--load` (volatile)
  is the default for experiments.

## Debug on hardware

Method: https://github.com/enjoy-digital/litex/wiki/Debug-A-SoC-On-Hardware (check the link and `--ident` first, registers before
traces, narrow LiteScope captures). `litex_mcp` gives the same loop as MCP tools (CSRs by name,
LiteScope captures, builds with parsed timing, simulation): https://github.com/enjoy-digital/litex/wiki/LiteX-for-AI-Agents#drive-a-soc-through-mcp.
