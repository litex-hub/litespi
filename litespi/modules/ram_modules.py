from litespi.spi_nor_flash_module import SpiNorFlashModule
from litespi.opcodes import SpiNorFlashOpCodes as Codes
from litespi.ids import SpiNorFlashManufacturerIDs

# Define non-generated SPI PSRAM chips here

class APS6404L(SpiNorFlashModule):
    manufacturer_id = SpiNorFlashManufacturerIDs.NONJEDEC # AP Memory
    device_id = 0x0000
    name = "aps6404l"

    total_size  =   8388608  # bytes
    page_size   =       128  # bytes
    total_pages =     65536

    supported_opcodes = [
        Codes.READ_1_1_1,       # max 33 MHz
        Codes.READ_1_1_1_FAST,  # max 84 MHz
        Codes.READ_1_4_4,       # max 84 MHz
        Codes.READ_4_4_4_LOW,   # max 66 MHz
        Codes.READ_4_4_4,       # max 84 MHz
        Codes.PP_1_1_1,         # max 84 MHz
        Codes.PP_1_4_4,         # max 84 MHz
    ]

    dummy_cycles = {
        Codes.READ_1_1_1_FAST: 8,
        Codes.READ_1_4_4: 6,
        Codes.READ_4_4_4_LOW: 4,
        Codes.READ_4_4_4: 6,
    }
