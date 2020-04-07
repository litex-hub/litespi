# Generated using 'spi_nor_cfg_gen.py'
from litespi.spi_nor_flash_module import SpiNorFlashModule
from litespi.opcodes import SpiNorFlashOpCodes
from litespi.ids import SpiNorFlashManufacturerIDs


class X160S33B(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.INTEL
    device_id = 0x8911
    name = "160s33b"

    total_size  =    2097152   # bytes
    page_size   =        256   # bytes
    total_pages =       8192

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
    ]
    dummy_bits = 8


class X25DF081A(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.ATMEL
    device_id = 0x4501
    name = "25df081a"

    total_size  =    1048576   # bytes
    page_size   =        256   # bytes
    total_pages =       4096

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class X25F160S33B8(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.INTEL
    device_id = 0x8911
    name = "25f160s33b8"

    total_size  =    2097152   # bytes
    page_size   =        256   # bytes
    total_pages =       8192

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class X25F160S33T8(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.INTEL
    device_id = 0x8915
    name = "25f160s33t8"

    total_size  =    2097152   # bytes
    page_size   =        256   # bytes
    total_pages =       8192

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class X25F320S33B8(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.INTEL
    device_id = 0x8912
    name = "25f320s33b8"

    total_size  =    4194304   # bytes
    page_size   =        256   # bytes
    total_pages =      16384

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class X25F320S33T8(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.INTEL
    device_id = 0x8916
    name = "25f320s33t8"

    total_size  =    4194304   # bytes
    page_size   =        256   # bytes
    total_pages =      16384

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class X25F640S33B8(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.INTEL
    device_id = 0x8913
    name = "25f640s33b8"

    total_size  =    8388608   # bytes
    page_size   =        256   # bytes
    total_pages =      32768

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class X25F640S33T8(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.INTEL
    device_id = 0x8917
    name = "25f640s33t8"

    total_size  =    8388608   # bytes
    page_size   =        256   # bytes
    total_pages =      32768

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class X320S33B(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.INTEL
    device_id = 0x8912
    name = "320s33b"

    total_size  =    4194304   # bytes
    page_size   =        256   # bytes
    total_pages =      16384

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
    ]
    dummy_bits = 8


class X3S1400AN(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.ATMEL
    device_id = 0x2600
    name = "3S1400AN"

    total_size  =    2162688   # bytes
    page_size   =        528   # bytes
    total_pages =       4096

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class X3S200AN(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.ATMEL
    device_id = 0x2400
    name = "3S200AN"

    total_size  =     540672   # bytes
    page_size   =        264   # bytes
    total_pages =       2048

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class X3S400AN(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.ATMEL
    device_id = 0x2400
    name = "3S400AN"

    total_size  =     540672   # bytes
    page_size   =        264   # bytes
    total_pages =       2048

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class X3S50AN(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.ATMEL
    device_id = 0x2200
    name = "3S50AN"

    total_size  =     135168   # bytes
    page_size   =        264   # bytes
    total_pages =        512

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class X3S700AN(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.ATMEL
    device_id = 0x2500
    name = "3S700AN"

    total_size  =    1081344   # bytes
    page_size   =        264   # bytes
    total_pages =       4096

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class X640S33B(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.INTEL
    device_id = 0x8913
    name = "640s33b"

    total_size  =    8388608   # bytes
    page_size   =        256   # bytes
    total_pages =      32768

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
    ]
    dummy_bits = 8


class XM25QH128A(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.ST
    device_id = 0x7018
    name = "XM25QH128A"

    total_size  =   16777216   # bytes
    page_size   =        256   # bytes
    total_pages =      65536

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
        SpiNorFlashOpCodes.READ_1_1_2,
        SpiNorFlashOpCodes.PP_1_1_2,
        SpiNorFlashOpCodes.READ_1_1_4,
        SpiNorFlashOpCodes.PP_1_1_4,
    ]
    dummy_bits = 8


class XM25QH64A(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.ST
    device_id = 0x7017
    name = "XM25QH64A"

    total_size  =    8388608   # bytes
    page_size   =        256   # bytes
    total_pages =      32768

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
        SpiNorFlashOpCodes.READ_1_1_2,
        SpiNorFlashOpCodes.PP_1_1_2,
        SpiNorFlashOpCodes.READ_1_1_4,
        SpiNorFlashOpCodes.PP_1_1_4,
    ]
    dummy_bits = 8


class A25L010(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.AMIC
    device_id = 0x3011
    name = "a25l010"

    total_size  =     131072   # bytes
    page_size   =        256   # bytes
    total_pages =        512

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class A25L016(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.AMIC
    device_id = 0x3015
    name = "a25l016"

    total_size  =    2097152   # bytes
    page_size   =        256   # bytes
    total_pages =       8192

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class A25L020(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.AMIC
    device_id = 0x3012
    name = "a25l020"

    total_size  =     262144   # bytes
    page_size   =        256   # bytes
    total_pages =       1024

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class A25L032(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.AMIC
    device_id = 0x3016
    name = "a25l032"

    total_size  =    4194304   # bytes
    page_size   =        256   # bytes
    total_pages =      16384

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class A25L040(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.AMIC
    device_id = 0x3013
    name = "a25l040"

    total_size  =     524288   # bytes
    page_size   =        256   # bytes
    total_pages =       2048

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class A25L05PT(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.AMIC
    device_id = 0x2020
    name = "a25l05pt"

    total_size  =      65536   # bytes
    page_size   =        256   # bytes
    total_pages =        256

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class A25L05PU(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.AMIC
    device_id = 0x2010
    name = "a25l05pu"

    total_size  =      65536   # bytes
    page_size   =        256   # bytes
    total_pages =        256

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class A25L080(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.AMIC
    device_id = 0x3014
    name = "a25l080"

    total_size  =    1048576   # bytes
    page_size   =        256   # bytes
    total_pages =       4096

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class A25L10PT(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.AMIC
    device_id = 0x2021
    name = "a25l10pt"

    total_size  =     131072   # bytes
    page_size   =        256   # bytes
    total_pages =        512

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class A25L10PU(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.AMIC
    device_id = 0x2011
    name = "a25l10pu"

    total_size  =     131072   # bytes
    page_size   =        256   # bytes
    total_pages =        512

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class A25L16PT(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.AMIC
    device_id = 0x2025
    name = "a25l16pt"

    total_size  =    2097152   # bytes
    page_size   =        256   # bytes
    total_pages =       8192

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class A25L16PU(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.AMIC
    device_id = 0x2015
    name = "a25l16pu"

    total_size  =    2097152   # bytes
    page_size   =        256   # bytes
    total_pages =       8192

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class A25L20PT(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.AMIC
    device_id = 0x2022
    name = "a25l20pt"

    total_size  =     262144   # bytes
    page_size   =        256   # bytes
    total_pages =       1024

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class A25L20PU(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.AMIC
    device_id = 0x2012
    name = "a25l20pu"

    total_size  =     262144   # bytes
    page_size   =        256   # bytes
    total_pages =       1024

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class A25L40PU(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.AMIC
    device_id = 0x2013
    name = "a25l40pu"

    total_size  =     524288   # bytes
    page_size   =        256   # bytes
    total_pages =       2048

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class A25L512(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.AMIC
    device_id = 0x3010
    name = "a25l512"

    total_size  =      65536   # bytes
    page_size   =        256   # bytes
    total_pages =        256

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class A25L80P(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.AMIC
    device_id = 0x2014
    name = "a25l80p"

    total_size  =    1048576   # bytes
    page_size   =        256   # bytes
    total_pages =       4096

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class A25LQ032(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.AMIC
    device_id = 0x4016
    name = "a25lq032"

    total_size  =    4194304   # bytes
    page_size   =        256   # bytes
    total_pages =      16384

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class A25LQ16(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.AMIC
    device_id = 0x4015
    name = "a25lq16"

    total_size  =    2097152   # bytes
    page_size   =        256   # bytes
    total_pages =       8192

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class A25LQ32A(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.AMIC
    device_id = 0x4016
    name = "a25lq32a"

    total_size  =    4194304   # bytes
    page_size   =        256   # bytes
    total_pages =      16384

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class A25LQ64(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.AMIC
    device_id = 0x4017
    name = "a25lq64"

    total_size  =    8388608   # bytes
    page_size   =        256   # bytes
    total_pages =      32768

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_4,
        SpiNorFlashOpCodes.PP_1_1_4,
    ]
    dummy_bits = 8


class AT25DF021(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.ATMEL
    device_id = 0x4300
    name = "at25df021"

    total_size  =     262144   # bytes
    page_size   =        256   # bytes
    total_pages =       1024

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class AT25DF021A(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.ATMEL
    device_id = 0x4301
    name = "at25df021a"

    total_size  =     262144   # bytes
    page_size   =        256   # bytes
    total_pages =       1024

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class AT25DF041A(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.ATMEL
    device_id = 0x4401
    name = "at25df041a"

    total_size  =     524288   # bytes
    page_size   =        256   # bytes
    total_pages =       2048

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
    ]
    dummy_bits = 8


class AT25DF081A(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.ATMEL
    device_id = 0x4501
    name = "at25df081a"

    total_size  =    1048576   # bytes
    page_size   =        256   # bytes
    total_pages =       4096

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class AT25DF161(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.ATMEL
    device_id = 0x4602
    name = "at25df161"

    total_size  =    2097152   # bytes
    page_size   =        256   # bytes
    total_pages =       8192

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class AT25DF321(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.ATMEL
    device_id = 0x4700
    name = "at25df321"

    total_size  =    4194304   # bytes
    page_size   =        256   # bytes
    total_pages =      16384

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
    ]
    dummy_bits = 8


class AT25DF321A(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.ATMEL
    device_id = 0x4701
    name = "at25df321a"

    total_size  =    4194304   # bytes
    page_size   =        256   # bytes
    total_pages =      16384

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
    ]
    dummy_bits = 8


class AT25DF641(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.ATMEL
    device_id = 0x4800
    name = "at25df641"

    total_size  =    8388608   # bytes
    page_size   =        256   # bytes
    total_pages =      32768

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
    ]
    dummy_bits = 8


class AT25DF641A(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.ATMEL
    device_id = 0x4800
    name = "at25df641a"

    total_size  =    8388608   # bytes
    page_size   =        256   # bytes
    total_pages =      32768

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class AT25DL081(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.ATMEL
    device_id = 0x4502
    name = "at25dl081"

    total_size  =    1048576   # bytes
    page_size   =        256   # bytes
    total_pages =       4096

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class AT25DL161(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.ATMEL
    device_id = 0x4603
    name = "at25dl161"

    total_size  =    2097152   # bytes
    page_size   =        256   # bytes
    total_pages =       8192

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class AT25DQ161(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.ATMEL
    device_id = 0x8600
    name = "at25dq161"

    total_size  =    2097152   # bytes
    page_size   =        256   # bytes
    total_pages =       8192

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class AT25F1024(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.ATMEL
    device_id = 0x0060
    name = "at25f1024"

    total_size  =     131072   # bytes
    page_size   =        256   # bytes
    total_pages =        512

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class AT25F1024A(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.ATMEL
    device_id = 0x0060
    name = "at25f1024a"

    total_size  =     131072   # bytes
    page_size   =        256   # bytes
    total_pages =        512

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class AT25F2048(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.ATMEL
    device_id = 0x0063
    name = "at25f2048"

    total_size  =     262144   # bytes
    page_size   =        256   # bytes
    total_pages =       1024

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class AT25F4096(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.ATMEL
    device_id = 0x0064
    name = "at25f4096"

    total_size  =     524288   # bytes
    page_size   =        256   # bytes
    total_pages =       2048

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class AT25F512(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.ATMEL
    device_id = 0x0060
    name = "at25f512"

    total_size  =      65536   # bytes
    page_size   =        256   # bytes
    total_pages =        256

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class AT25F512A(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.ATMEL
    device_id = 0x0065
    name = "at25f512a"

    total_size  =      65536   # bytes
    page_size   =        128   # bytes
    total_pages =        512

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class AT25F512B(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.ATMEL
    device_id = 0x6500
    name = "at25f512b"

    total_size  =      65536   # bytes
    page_size   =        256   # bytes
    total_pages =        256

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class AT25FS010(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.ATMEL
    device_id = 0x6601
    name = "at25fs010"

    total_size  =     131072   # bytes
    page_size   =        256   # bytes
    total_pages =        512

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
    ]
    dummy_bits = 8


class AT25FS040(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.ATMEL
    device_id = 0x6604
    name = "at25fs040"

    total_size  =     524288   # bytes
    page_size   =        256   # bytes
    total_pages =       2048

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
    ]
    dummy_bits = 8


class AT25SF041(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.ATMEL
    device_id = 0x8401
    name = "at25sf041"

    total_size  =     524288   # bytes
    page_size   =        256   # bytes
    total_pages =       2048

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class AT25SF081(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.ATMEL
    device_id = 0x8501
    name = "at25sf081"

    total_size  =    1048576   # bytes
    page_size   =        256   # bytes
    total_pages =       4096

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class AT25SF161(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.ATMEL
    device_id = 0x8601
    name = "at25sf161"

    total_size  =    2097152   # bytes
    page_size   =        256   # bytes
    total_pages =       8192

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class AT25SF321(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.ATMEL
    device_id = 0x8701
    name = "at25sf321"

    total_size  =    4194304   # bytes
    page_size   =        256   # bytes
    total_pages =      16384

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class AT25SL128A(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.ATMEL
    device_id = 0x4218
    name = "at25sl128a"

    total_size  =   16777216   # bytes
    page_size   =        256   # bytes
    total_pages =      65536

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_4,
        SpiNorFlashOpCodes.PP_1_1_4,
    ]
    dummy_bits = 8


class AT25SL321(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.ATMEL
    device_id = 0x4216
    name = "at25sl321"

    total_size  =    4194304   # bytes
    page_size   =        256   # bytes
    total_pages =      16384

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
        SpiNorFlashOpCodes.READ_1_1_2,
        SpiNorFlashOpCodes.PP_1_1_2,
        SpiNorFlashOpCodes.READ_1_1_4,
        SpiNorFlashOpCodes.PP_1_1_4,
    ]
    dummy_bits = 8


class AT26DF041(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.ATMEL
    device_id = 0x4400
    name = "at26df041"

    total_size  =     524288   # bytes
    page_size   =        256   # bytes
    total_pages =       2048

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class AT26DF081A(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.ATMEL
    device_id = 0x4501
    name = "at26df081a"

    total_size  =    1048576   # bytes
    page_size   =        256   # bytes
    total_pages =       4096

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
    ]
    dummy_bits = 8


class AT26DF161(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.ATMEL
    device_id = 0x4600
    name = "at26df161"

    total_size  =    2097152   # bytes
    page_size   =        256   # bytes
    total_pages =       8192

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class AT26DF161A(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.ATMEL
    device_id = 0x4601
    name = "at26df161a"

    total_size  =    2097152   # bytes
    page_size   =        256   # bytes
    total_pages =       8192

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
    ]
    dummy_bits = 8


class AT26DF321(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.ATMEL
    device_id = 0x4700
    name = "at26df321"

    total_size  =    4194304   # bytes
    page_size   =        256   # bytes
    total_pages =      16384

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
    ]
    dummy_bits = 8


class AT26F004(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.ATMEL
    device_id = 0x0400
    name = "at26f004"

    total_size  =     524288   # bytes
    page_size   =        256   # bytes
    total_pages =       2048

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
    ]
    dummy_bits = 8


class AT45DB011D(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.ATMEL
    device_id = 0x2200
    name = "at45db011d"

    total_size  =     131072   # bytes
    page_size   =        256   # bytes
    total_pages =        512

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class AT45DB021D(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.ATMEL
    device_id = 0x2300
    name = "at45db021d"

    total_size  =     262144   # bytes
    page_size   =        256   # bytes
    total_pages =       1024

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class AT45DB041D(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.ATMEL
    device_id = 0x2400
    name = "at45db041d"

    total_size  =     524288   # bytes
    page_size   =        256   # bytes
    total_pages =       2048

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class AT45DB081D(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.ATMEL
    device_id = 0x2500
    name = "at45db081d"

    total_size  =    1048576   # bytes
    page_size   =        256   # bytes
    total_pages =       4096

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
    ]
    dummy_bits = 8


class AT45DB161D(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.ATMEL
    device_id = 0x2600
    name = "at45db161d"

    total_size  =    2097152   # bytes
    page_size   =        512   # bytes
    total_pages =       4096

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class AT45DB321D(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.ATMEL
    device_id = 0x2701
    name = "at45db321d"

    total_size  =    4194304   # bytes
    page_size   =        512   # bytes
    total_pages =       8192

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class AT45DB321E(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.ATMEL
    device_id = 0x2700
    name = "at45db321e"

    total_size  =    4194304   # bytes
    page_size   =        512   # bytes
    total_pages =       8192

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class AT45DB642D(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.ATMEL
    device_id = 0x2800
    name = "at45db642d"

    total_size  =    8388608   # bytes
    page_size   =       1024   # bytes
    total_pages =       8192

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class CAT25128(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.NONJEDEC
    device_id = 0x0000
    name = "cat25128"

    total_size  =      16384   # bytes
    page_size   =         64   # bytes
    total_pages =        256

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class CAT25C03(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.NONJEDEC
    device_id = 0x0000
    name = "cat25c03"

    total_size  =        256   # bytes
    page_size   =         16   # bytes
    total_pages =         16

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class CAT25C09(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.NONJEDEC
    device_id = 0x0000
    name = "cat25c09"

    total_size  =       1024   # bytes
    page_size   =         32   # bytes
    total_pages =         32

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class CAT25C11(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.NONJEDEC
    device_id = 0x0000
    name = "cat25c11"

    total_size  =        128   # bytes
    page_size   =         16   # bytes
    total_pages =          8

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class CAT25C17(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.NONJEDEC
    device_id = 0x0000
    name = "cat25c17"

    total_size  =       2048   # bytes
    page_size   =         32   # bytes
    total_pages =         64

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class EN25F32(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.EON
    device_id = 0x3116
    name = "en25f32"

    total_size  =    4194304   # bytes
    page_size   =        256   # bytes
    total_pages =      16384

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
    ]
    dummy_bits = 8


class EN25P32(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.EON
    device_id = 0x2016
    name = "en25p32"

    total_size  =    4194304   # bytes
    page_size   =        256   # bytes
    total_pages =      16384

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
    ]
    dummy_bits = 8


class EN25P64(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.EON
    device_id = 0x2017
    name = "en25p64"

    total_size  =    8388608   # bytes
    page_size   =        256   # bytes
    total_pages =      32768

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
    ]
    dummy_bits = 8


class EN25Q32B(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.EON
    device_id = 0x3016
    name = "en25q32b"

    total_size  =    4194304   # bytes
    page_size   =        256   # bytes
    total_pages =      16384

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
    ]
    dummy_bits = 8


class EN25Q64(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.EON
    device_id = 0x3017
    name = "en25q64"

    total_size  =    8388608   # bytes
    page_size   =        256   # bytes
    total_pages =      32768

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
    ]
    dummy_bits = 8


class EN25Q80A(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.EON
    device_id = 0x3014
    name = "en25q80a"

    total_size  =    1048576   # bytes
    page_size   =        256   # bytes
    total_pages =       4096

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
        SpiNorFlashOpCodes.READ_1_1_2,
        SpiNorFlashOpCodes.PP_1_1_2,
    ]
    dummy_bits = 8


class EN25QH128(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.EON
    device_id = 0x7018
    name = "en25qh128"

    total_size  =   16777216   # bytes
    page_size   =        256   # bytes
    total_pages =      65536

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
    ]
    dummy_bits = 8


class EN25QH16(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.EON
    device_id = 0x7015
    name = "en25qh16"

    total_size  =    2097152   # bytes
    page_size   =        256   # bytes
    total_pages =       8192

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
        SpiNorFlashOpCodes.READ_1_1_2,
        SpiNorFlashOpCodes.PP_1_1_2,
    ]
    dummy_bits = 8


class EN25QH256(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.EON
    device_id = 0x7019
    name = "en25qh256"

    total_size  =   33554432   # bytes
    page_size   =        256   # bytes
    total_pages =     131072

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
    ]
    dummy_bits = 8


class EN25QH32(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.EON
    device_id = 0x7016
    name = "en25qh32"

    total_size  =    4194304   # bytes
    page_size   =        256   # bytes
    total_pages =      16384

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
    ]
    dummy_bits = 8


class EN25QH64(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.EON
    device_id = 0x7017
    name = "en25qh64"

    total_size  =    8388608   # bytes
    page_size   =        256   # bytes
    total_pages =      32768

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
        SpiNorFlashOpCodes.READ_1_1_2,
        SpiNorFlashOpCodes.PP_1_1_2,
    ]
    dummy_bits = 8


class EN25S64(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.EON
    device_id = 0x3817
    name = "en25s64"

    total_size  =    8388608   # bytes
    page_size   =        256   # bytes
    total_pages =      32768

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
    ]
    dummy_bits = 8


class F25L008A(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.ESMT
    device_id = 0x2014
    name = "f25l008a"

    total_size  =    1048576   # bytes
    page_size   =        256   # bytes
    total_pages =       4096

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class F25L32PA(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.ESMT
    device_id = 0x2016
    name = "f25l32pa"

    total_size  =    4194304   # bytes
    page_size   =        256   # bytes
    total_pages =      16384

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
    ]
    dummy_bits = 8


class F25L32QA(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.ESMT
    device_id = 0x4116
    name = "f25l32qa"

    total_size  =    4194304   # bytes
    page_size   =        256   # bytes
    total_pages =      16384

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
    ]
    dummy_bits = 8


class F25L64QA(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.ESMT
    device_id = 0x4117
    name = "f25l64qa"

    total_size  =    8388608   # bytes
    page_size   =        256   # bytes
    total_pages =      32768

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
    ]
    dummy_bits = 8


class GD25LQ128C(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.GIGADEVICE
    device_id = 0x6018
    name = "gd25lq128c"

    total_size  =   16777216   # bytes
    page_size   =        256   # bytes
    total_pages =      65536

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class GD25LQ128D(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.GIGADEVICE
    device_id = 0x6018
    name = "gd25lq128d"

    total_size  =   16777216   # bytes
    page_size   =        256   # bytes
    total_pages =      65536

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
        SpiNorFlashOpCodes.READ_1_1_2,
        SpiNorFlashOpCodes.PP_1_1_2,
        SpiNorFlashOpCodes.READ_1_1_4,
        SpiNorFlashOpCodes.PP_1_1_4,
    ]
    dummy_bits = 8


class GD25LQ16(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.GIGADEVICE
    device_id = 0x6015
    name = "gd25lq16"

    total_size  =    2097152   # bytes
    page_size   =        256   # bytes
    total_pages =       8192

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class GD25LQ32(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.GIGADEVICE
    device_id = 0x6016
    name = "gd25lq32"

    total_size  =    4194304   # bytes
    page_size   =        256   # bytes
    total_pages =      16384

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
        SpiNorFlashOpCodes.READ_1_1_2,
        SpiNorFlashOpCodes.PP_1_1_2,
        SpiNorFlashOpCodes.READ_1_1_4,
        SpiNorFlashOpCodes.PP_1_1_4,
    ]
    dummy_bits = 8


class GD25LQ40(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.GIGADEVICE
    device_id = 0x6013
    name = "gd25lq40"

    total_size  =     524288   # bytes
    page_size   =        256   # bytes
    total_pages =       2048

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class GD25LQ64(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.GIGADEVICE
    device_id = 0x6017
    name = "gd25lq64"

    total_size  =    8388608   # bytes
    page_size   =        256   # bytes
    total_pages =      32768

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class GD25LQ64B(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.GIGADEVICE
    device_id = 0x6017
    name = "gd25lq64b"

    total_size  =    8388608   # bytes
    page_size   =        256   # bytes
    total_pages =      32768

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class GD25LQ64C(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.GIGADEVICE
    device_id = 0x6017
    name = "gd25lq64c"

    total_size  =    8388608   # bytes
    page_size   =        256   # bytes
    total_pages =      32768

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
        SpiNorFlashOpCodes.READ_1_1_2,
        SpiNorFlashOpCodes.PP_1_1_2,
        SpiNorFlashOpCodes.READ_1_1_4,
        SpiNorFlashOpCodes.PP_1_1_4,
    ]
    dummy_bits = 8


class GD25LQ80(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.GIGADEVICE
    device_id = 0x6014
    name = "gd25lq80"

    total_size  =    1048576   # bytes
    page_size   =        256   # bytes
    total_pages =       4096

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class GD25Q10(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.GIGADEVICE
    device_id = 0x4011
    name = "gd25q10"

    total_size  =     131072   # bytes
    page_size   =        256   # bytes
    total_pages =        512

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class GD25Q127C(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.GIGADEVICE
    device_id = 0x4018
    name = "gd25q127c"

    total_size  =   16777216   # bytes
    page_size   =        256   # bytes
    total_pages =      65536

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_4,
        SpiNorFlashOpCodes.PP_1_1_4,
    ]
    dummy_bits = 8


class GD25Q128(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.GIGADEVICE
    device_id = 0x4018
    name = "gd25q128"

    total_size  =   16777216   # bytes
    page_size   =        256   # bytes
    total_pages =      65536

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
        SpiNorFlashOpCodes.READ_1_1_2,
        SpiNorFlashOpCodes.PP_1_1_2,
        SpiNorFlashOpCodes.READ_1_1_4,
        SpiNorFlashOpCodes.PP_1_1_4,
    ]
    dummy_bits = 8


class GD25Q128C(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.GIGADEVICE
    device_id = 0x4018
    name = "gd25q128c"

    total_size  =   16777216   # bytes
    page_size   =        256   # bytes
    total_pages =      65536

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_4,
        SpiNorFlashOpCodes.PP_1_1_4,
    ]
    dummy_bits = 8


class GD25Q16(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.GIGADEVICE
    device_id = 0x4015
    name = "gd25q16"

    total_size  =    2097152   # bytes
    page_size   =        256   # bytes
    total_pages =       8192

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
        SpiNorFlashOpCodes.READ_1_1_2,
        SpiNorFlashOpCodes.PP_1_1_2,
        SpiNorFlashOpCodes.READ_1_1_4,
        SpiNorFlashOpCodes.PP_1_1_4,
    ]
    dummy_bits = 8


class GD25Q16B(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.GIGADEVICE
    device_id = 0x4015
    name = "gd25q16b"

    total_size  =    2097152   # bytes
    page_size   =        256   # bytes
    total_pages =       8192

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class GD25Q16C(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.GIGADEVICE
    device_id = 0x4015
    name = "gd25q16c"

    total_size  =    2097152   # bytes
    page_size   =        256   # bytes
    total_pages =       8192

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class GD25Q20(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.GIGADEVICE
    device_id = 0x4012
    name = "gd25q20"

    total_size  =     262144   # bytes
    page_size   =        256   # bytes
    total_pages =       1024

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class GD25Q20B(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.GIGADEVICE
    device_id = 0x4012
    name = "gd25q20b"

    total_size  =     262144   # bytes
    page_size   =        256   # bytes
    total_pages =       1024

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class GD25Q256(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.GIGADEVICE
    device_id = 0x4019
    name = "gd25q256"

    total_size  =   33554432   # bytes
    page_size   =        256   # bytes
    total_pages =     131072

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
        SpiNorFlashOpCodes.READ_1_1_2,
        SpiNorFlashOpCodes.PP_1_1_2,
        SpiNorFlashOpCodes.READ_1_1_4,
        SpiNorFlashOpCodes.PP_1_1_4,
        SpiNorFlashOpCodes.READ_1_1_1_4B,
        SpiNorFlashOpCodes.PP_1_1_1_4B,
        SpiNorFlashOpCodes.READ_1_1_1_FAST_4B,
        SpiNorFlashOpCodes.READ_1_1_2_4B,
        SpiNorFlashOpCodes.READ_1_1_4_4B,
        SpiNorFlashOpCodes.PP_1_1_4_4B,
    ]
    dummy_bits = 8


class GD25Q256C(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.GIGADEVICE
    device_id = 0x4019
    name = "gd25q256c"

    total_size  =   33554432   # bytes
    page_size   =        256   # bytes
    total_pages =     131072

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class GD25Q256D(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.GIGADEVICE
    device_id = 0x4019
    name = "gd25q256d"

    total_size  =   33554432   # bytes
    page_size   =        256   # bytes
    total_pages =     131072

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
        SpiNorFlashOpCodes.READ_1_1_1_4B,
        SpiNorFlashOpCodes.PP_1_1_1_4B,
        SpiNorFlashOpCodes.READ_1_1_1_FAST_4B,
    ]
    dummy_bits = 8


class GD25Q32(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.GIGADEVICE
    device_id = 0x4016
    name = "gd25q32"

    total_size  =    4194304   # bytes
    page_size   =        256   # bytes
    total_pages =      16384

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
        SpiNorFlashOpCodes.READ_1_1_2,
        SpiNorFlashOpCodes.PP_1_1_2,
        SpiNorFlashOpCodes.READ_1_1_4,
        SpiNorFlashOpCodes.PP_1_1_4,
    ]
    dummy_bits = 8


class GD25Q32B(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.GIGADEVICE
    device_id = 0x4016
    name = "gd25q32b"

    total_size  =    4194304   # bytes
    page_size   =        256   # bytes
    total_pages =      16384

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class GD25Q32C(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.GIGADEVICE
    device_id = 0x4016
    name = "gd25q32c"

    total_size  =    4194304   # bytes
    page_size   =        256   # bytes
    total_pages =      16384

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class GD25Q40(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.GIGADEVICE
    device_id = 0x4013
    name = "gd25q40"

    total_size  =     524288   # bytes
    page_size   =        256   # bytes
    total_pages =       2048

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class GD25Q40B(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.GIGADEVICE
    device_id = 0x4013
    name = "gd25q40b"

    total_size  =     524288   # bytes
    page_size   =        256   # bytes
    total_pages =       2048

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class GD25Q512(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.GIGADEVICE
    device_id = 0x4010
    name = "gd25q512"

    total_size  =      65536   # bytes
    page_size   =        256   # bytes
    total_pages =        256

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class GD25Q512MC(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.GIGADEVICE
    device_id = 0x4020
    name = "gd25q512mc"

    total_size  =   67108864   # bytes
    page_size   =        256   # bytes
    total_pages =     262144

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_2,
        SpiNorFlashOpCodes.PP_1_1_2,
        SpiNorFlashOpCodes.READ_1_1_4,
        SpiNorFlashOpCodes.PP_1_1_4,
    ]
    dummy_bits = 8


class GD25Q64(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.GIGADEVICE
    device_id = 0x4017
    name = "gd25q64"

    total_size  =    8388608   # bytes
    page_size   =        256   # bytes
    total_pages =      32768

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
        SpiNorFlashOpCodes.READ_1_1_2,
        SpiNorFlashOpCodes.PP_1_1_2,
        SpiNorFlashOpCodes.READ_1_1_4,
        SpiNorFlashOpCodes.PP_1_1_4,
    ]
    dummy_bits = 8


class GD25Q64B(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.GIGADEVICE
    device_id = 0x4017
    name = "gd25q64b"

    total_size  =    8388608   # bytes
    page_size   =        256   # bytes
    total_pages =      32768

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class GD25Q64C(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.GIGADEVICE
    device_id = 0x4017
    name = "gd25q64c"

    total_size  =    8388608   # bytes
    page_size   =        256   # bytes
    total_pages =      32768

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class GD25Q80(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.GIGADEVICE
    device_id = 0x4014
    name = "gd25q80"

    total_size  =    1048576   # bytes
    page_size   =        256   # bytes
    total_pages =       4096

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class GD25Q80B(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.GIGADEVICE
    device_id = 0x4014
    name = "gd25q80b"

    total_size  =    1048576   # bytes
    page_size   =        256   # bytes
    total_pages =       4096

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class GD25T80(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.GIGADEVICE
    device_id = 0x3114
    name = "gd25t80"

    total_size  =    1048576   # bytes
    page_size   =        256   # bytes
    total_pages =       4096

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class GD25VQ16C(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.GIGADEVICE
    device_id = 0x4215
    name = "gd25vq16c"

    total_size  =    2097152   # bytes
    page_size   =        256   # bytes
    total_pages =       8192

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_4,
        SpiNorFlashOpCodes.PP_1_1_4,
    ]
    dummy_bits = 8


class GD25VQ21B(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.GIGADEVICE
    device_id = 0x4212
    name = "gd25vq21b"

    total_size  =     262144   # bytes
    page_size   =        256   # bytes
    total_pages =       1024

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_4,
        SpiNorFlashOpCodes.PP_1_1_4,
    ]
    dummy_bits = 8


class GD25VQ41B(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.GIGADEVICE
    device_id = 0x4213
    name = "gd25vq41b"

    total_size  =     524288   # bytes
    page_size   =        256   # bytes
    total_pages =       2048

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_4,
        SpiNorFlashOpCodes.PP_1_1_4,
    ]
    dummy_bits = 8


class GD25VQ80C(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.GIGADEVICE
    device_id = 0x4214
    name = "gd25vq80c"

    total_size  =    1048576   # bytes
    page_size   =        256   # bytes
    total_pages =       4096

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_4,
        SpiNorFlashOpCodes.PP_1_1_4,
    ]
    dummy_bits = 8


class GD25WQ80E(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.GIGADEVICE
    device_id = 0x6514
    name = "gd25wq80e"

    total_size  =    1048576   # bytes
    page_size   =        256   # bytes
    total_pages =       4096

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class IS25CD512(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.NONJEDEC
    device_id = 0x0020
    name = "is25cd512"

    total_size  =      65536   # bytes
    page_size   =        256   # bytes
    total_pages =        256

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
    ]
    dummy_bits = 8


class IS25LP016D(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.ISSI
    device_id = 0x6015
    name = "is25lp016d"

    total_size  =    2097152   # bytes
    page_size   =        256   # bytes
    total_pages =       8192

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
        SpiNorFlashOpCodes.READ_1_1_2,
        SpiNorFlashOpCodes.PP_1_1_2,
        SpiNorFlashOpCodes.READ_1_1_4,
        SpiNorFlashOpCodes.PP_1_1_4,
    ]
    dummy_bits = 8


class IS25LP032(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.ISSI
    device_id = 0x6016
    name = "is25lp032"

    total_size  =    4194304   # bytes
    page_size   =        256   # bytes
    total_pages =      16384

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
        SpiNorFlashOpCodes.READ_1_1_2,
        SpiNorFlashOpCodes.PP_1_1_2,
    ]
    dummy_bits = 8


class IS25LP064(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.ISSI
    device_id = 0x6017
    name = "is25lp064"

    total_size  =    8388608   # bytes
    page_size   =        256   # bytes
    total_pages =      32768

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
        SpiNorFlashOpCodes.READ_1_1_2,
        SpiNorFlashOpCodes.PP_1_1_2,
    ]
    dummy_bits = 8


class IS25LP080D(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.ISSI
    device_id = 0x6014
    name = "is25lp080d"

    total_size  =    1048576   # bytes
    page_size   =        256   # bytes
    total_pages =       4096

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
        SpiNorFlashOpCodes.READ_1_1_2,
        SpiNorFlashOpCodes.PP_1_1_2,
        SpiNorFlashOpCodes.READ_1_1_4,
        SpiNorFlashOpCodes.PP_1_1_4,
    ]
    dummy_bits = 8


class IS25LP128(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.ISSI
    device_id = 0x6018
    name = "is25lp128"

    total_size  =   16777216   # bytes
    page_size   =        256   # bytes
    total_pages =      65536

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
        SpiNorFlashOpCodes.READ_1_1_2,
        SpiNorFlashOpCodes.PP_1_1_2,
    ]
    dummy_bits = 8


class IS25LP128D(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.ISSI
    device_id = 0x6018
    name = "is25lp128d"

    total_size  =   16777216   # bytes
    page_size   =        256   # bytes
    total_pages =      65536

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class IS25LP256(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.ISSI
    device_id = 0x6019
    name = "is25lp256"

    total_size  =   33554432   # bytes
    page_size   =        256   # bytes
    total_pages =     131072

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
        SpiNorFlashOpCodes.READ_1_1_2,
        SpiNorFlashOpCodes.PP_1_1_2,
        SpiNorFlashOpCodes.READ_1_1_4,
        SpiNorFlashOpCodes.PP_1_1_4,
        SpiNorFlashOpCodes.READ_1_1_1_4B,
        SpiNorFlashOpCodes.PP_1_1_1_4B,
        SpiNorFlashOpCodes.READ_1_1_1_FAST_4B,
        SpiNorFlashOpCodes.READ_1_1_2_4B,
        SpiNorFlashOpCodes.READ_1_1_4_4B,
        SpiNorFlashOpCodes.PP_1_1_4_4B,
    ]
    dummy_bits = 8


class IS25LP256D(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.ISSI
    device_id = 0x6019
    name = "is25lp256d"

    total_size  =   33554432   # bytes
    page_size   =        256   # bytes
    total_pages =     131072

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class IS25LP512M(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.ISSI
    device_id = 0x601a
    name = "is25lp512m"

    total_size  =   67108864   # bytes
    page_size   =        256   # bytes
    total_pages =     262144

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_2,
        SpiNorFlashOpCodes.PP_1_1_2,
        SpiNorFlashOpCodes.READ_1_1_4,
        SpiNorFlashOpCodes.PP_1_1_4,
    ]
    dummy_bits = 8


class IS25LQ040B(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.ISSI
    device_id = 0x4013
    name = "is25lq040b"

    total_size  =     524288   # bytes
    page_size   =        256   # bytes
    total_pages =       2048

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
        SpiNorFlashOpCodes.READ_1_1_2,
        SpiNorFlashOpCodes.PP_1_1_2,
        SpiNorFlashOpCodes.READ_1_1_4,
        SpiNorFlashOpCodes.PP_1_1_4,
    ]
    dummy_bits = 8


class IS25WP032(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.ISSI
    device_id = 0x7016
    name = "is25wp032"

    total_size  =    4194304   # bytes
    page_size   =        256   # bytes
    total_pages =      16384

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
        SpiNorFlashOpCodes.READ_1_1_2,
        SpiNorFlashOpCodes.PP_1_1_2,
        SpiNorFlashOpCodes.READ_1_1_4,
        SpiNorFlashOpCodes.PP_1_1_4,
    ]
    dummy_bits = 8


class IS25WP064(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.ISSI
    device_id = 0x7017
    name = "is25wp064"

    total_size  =    8388608   # bytes
    page_size   =        256   # bytes
    total_pages =      32768

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
        SpiNorFlashOpCodes.READ_1_1_2,
        SpiNorFlashOpCodes.PP_1_1_2,
        SpiNorFlashOpCodes.READ_1_1_4,
        SpiNorFlashOpCodes.PP_1_1_4,
    ]
    dummy_bits = 8


class IS25WP128(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.ISSI
    device_id = 0x7018
    name = "is25wp128"

    total_size  =   16777216   # bytes
    page_size   =        256   # bytes
    total_pages =      65536

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
        SpiNorFlashOpCodes.READ_1_1_2,
        SpiNorFlashOpCodes.PP_1_1_2,
        SpiNorFlashOpCodes.READ_1_1_4,
        SpiNorFlashOpCodes.PP_1_1_4,
    ]
    dummy_bits = 8


class IS25WP128D(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.ISSI
    device_id = 0x7018
    name = "is25wp128d"

    total_size  =   16777216   # bytes
    page_size   =        256   # bytes
    total_pages =      65536

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class IS25WP256(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.ISSI
    device_id = 0x7019
    name = "is25wp256"

    total_size  =   33554432   # bytes
    page_size   =        256   # bytes
    total_pages =     131072

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
        SpiNorFlashOpCodes.READ_1_1_2,
        SpiNorFlashOpCodes.PP_1_1_2,
        SpiNorFlashOpCodes.READ_1_1_4,
        SpiNorFlashOpCodes.PP_1_1_4,
        SpiNorFlashOpCodes.READ_1_1_1_4B,
        SpiNorFlashOpCodes.PP_1_1_1_4B,
        SpiNorFlashOpCodes.READ_1_1_1_FAST_4B,
        SpiNorFlashOpCodes.READ_1_1_2_4B,
        SpiNorFlashOpCodes.READ_1_1_4_4B,
        SpiNorFlashOpCodes.PP_1_1_4_4B,
    ]
    dummy_bits = 8


class IS25WP256D(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.ISSI
    device_id = 0x7019
    name = "is25wp256d"

    total_size  =   33554432   # bytes
    page_size   =        256   # bytes
    total_pages =     131072

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class IS25WP512M(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.ISSI
    device_id = 0x701a
    name = "is25wp512m"

    total_size  =   67108864   # bytes
    page_size   =        256   # bytes
    total_pages =     262144

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_2,
        SpiNorFlashOpCodes.PP_1_1_2,
        SpiNorFlashOpCodes.READ_1_1_4,
        SpiNorFlashOpCodes.PP_1_1_4,
    ]
    dummy_bits = 8


class LE25FU106B(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.SANYO
    device_id = 0x001d
    name = "le25fu106b"

    total_size  =     131072   # bytes
    page_size   =        256   # bytes
    total_pages =        512

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class LE25FU206(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.SANYO
    device_id = 0x0044
    name = "le25fu206"

    total_size  =     262144   # bytes
    page_size   =        256   # bytes
    total_pages =       1024

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class LE25FU206A(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.SANYO
    device_id = 0x0612
    name = "le25fu206a"

    total_size  =     262144   # bytes
    page_size   =        256   # bytes
    total_pages =       1024

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class LE25FU406B(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.SANYO
    device_id = 0x001e
    name = "le25fu406b"

    total_size  =     524288   # bytes
    page_size   =        256   # bytes
    total_pages =       2048

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class LE25FU406C(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.SANYO
    device_id = 0x0613
    name = "le25fu406c"

    total_size  =     524288   # bytes
    page_size   =        256   # bytes
    total_pages =       2048

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class LE25FW106(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.SANYO
    device_id = 0x0015
    name = "le25fw106"

    total_size  =     131072   # bytes
    page_size   =        256   # bytes
    total_pages =        512

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class LE25FW203A(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.SANYO
    device_id = 0x1600
    name = "le25fw203a"

    total_size  =     262144   # bytes
    page_size   =        256   # bytes
    total_pages =       1024

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class LE25FW403A(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.SANYO
    device_id = 0x1100
    name = "le25fw403a"

    total_size  =     524288   # bytes
    page_size   =        256   # bytes
    total_pages =       2048

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class LE25FW406A(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.SANYO
    device_id = 0x001a
    name = "le25fw406a"

    total_size  =     524288   # bytes
    page_size   =        256   # bytes
    total_pages =       2048

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class LE25FW418A(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.SANYO
    device_id = 0x0010
    name = "le25fw418a"

    total_size  =     524288   # bytes
    page_size   =        256   # bytes
    total_pages =       2048

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class LE25FW806(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.SANYO
    device_id = 0x0026
    name = "le25fw806"

    total_size  =    1048576   # bytes
    page_size   =        256   # bytes
    total_pages =       4096

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class LE25FW808(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.SANYO
    device_id = 0x0020
    name = "le25fw808"

    total_size  =    1048576   # bytes
    page_size   =        256   # bytes
    total_pages =       4096

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class LE25U40CMC(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.SANYO
    device_id = 0x0613
    name = "le25u40cmc"

    total_size  =     524288   # bytes
    page_size   =        256   # bytes
    total_pages =       2048

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class M25P05(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.ST
    device_id = 0x2010
    name = "m25p05"

    total_size  =      65536   # bytes
    page_size   =        256   # bytes
    total_pages =        256

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
    ]
    dummy_bits = 8


class M25P05_A(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.ST
    device_id = 0x2010
    name = "m25p05-a"

    total_size  =      65536   # bytes
    page_size   =        256   # bytes
    total_pages =        256

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class M25P05_NONJEDEC(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.NONJEDEC
    device_id = 0x0000
    name = "m25p05-nonjedec"

    total_size  =      65536   # bytes
    page_size   =        256   # bytes
    total_pages =        256

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
    ]
    dummy_bits = 8


class M25P10(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.ST
    device_id = 0x2011
    name = "m25p10"

    total_size  =     131072   # bytes
    page_size   =        256   # bytes
    total_pages =        512

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
    ]
    dummy_bits = 8


class M25P10_A(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.ST
    device_id = 0x2011
    name = "m25p10-a"

    total_size  =     131072   # bytes
    page_size   =        256   # bytes
    total_pages =        512

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class M25P10_NONJEDEC(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.NONJEDEC
    device_id = 0x0000
    name = "m25p10-nonjedec"

    total_size  =     131072   # bytes
    page_size   =        256   # bytes
    total_pages =        512

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
    ]
    dummy_bits = 8


class M25P128(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.ST
    device_id = 0x2018
    name = "m25p128"

    total_size  =   16777216   # bytes
    page_size   =        256   # bytes
    total_pages =      65536

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
    ]
    dummy_bits = 8


class M25P128_NONJEDEC(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.NONJEDEC
    device_id = 0x0000
    name = "m25p128-nonjedec"

    total_size  =   16777216   # bytes
    page_size   =        256   # bytes
    total_pages =      65536

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
    ]
    dummy_bits = 8


class M25P16(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.ST
    device_id = 0x2015
    name = "m25p16"

    total_size  =    2097152   # bytes
    page_size   =        256   # bytes
    total_pages =       8192

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
    ]
    dummy_bits = 8


class M25P16_NONJEDEC(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.NONJEDEC
    device_id = 0x0000
    name = "m25p16-nonjedec"

    total_size  =    2097152   # bytes
    page_size   =        256   # bytes
    total_pages =       8192

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
    ]
    dummy_bits = 8


class M25P20(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.ST
    device_id = 0x2012
    name = "m25p20"

    total_size  =     262144   # bytes
    page_size   =        256   # bytes
    total_pages =       1024

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
    ]
    dummy_bits = 8


class M25P20_NONJEDEC(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.NONJEDEC
    device_id = 0x0000
    name = "m25p20-nonjedec"

    total_size  =     262144   # bytes
    page_size   =        256   # bytes
    total_pages =       1024

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
    ]
    dummy_bits = 8


class M25P20_OLD(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.ST
    device_id = 0x0011
    name = "m25p20-old"

    total_size  =     262144   # bytes
    page_size   =        256   # bytes
    total_pages =       1024

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class M25P32(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.ST
    device_id = 0x2016
    name = "m25p32"

    total_size  =    4194304   # bytes
    page_size   =        256   # bytes
    total_pages =      16384

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
    ]
    dummy_bits = 8


class M25P32_NONJEDEC(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.NONJEDEC
    device_id = 0x0000
    name = "m25p32-nonjedec"

    total_size  =    4194304   # bytes
    page_size   =        256   # bytes
    total_pages =      16384

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
    ]
    dummy_bits = 8


class M25P40(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.ST
    device_id = 0x2013
    name = "m25p40"

    total_size  =     524288   # bytes
    page_size   =        256   # bytes
    total_pages =       2048

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
    ]
    dummy_bits = 8


class M25P40_NONJEDEC(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.NONJEDEC
    device_id = 0x0000
    name = "m25p40-nonjedec"

    total_size  =     524288   # bytes
    page_size   =        256   # bytes
    total_pages =       2048

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
    ]
    dummy_bits = 8


class M25P40_OLD(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.ST
    device_id = 0x0012
    name = "m25p40-old"

    total_size  =     524288   # bytes
    page_size   =        256   # bytes
    total_pages =       2048

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class M25P64(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.ST
    device_id = 0x2017
    name = "m25p64"

    total_size  =    8388608   # bytes
    page_size   =        256   # bytes
    total_pages =      32768

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
    ]
    dummy_bits = 8


class M25P64_NONJEDEC(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.NONJEDEC
    device_id = 0x0000
    name = "m25p64-nonjedec"

    total_size  =    8388608   # bytes
    page_size   =        256   # bytes
    total_pages =      32768

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
    ]
    dummy_bits = 8


class M25P80(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.ST
    device_id = 0x2014
    name = "m25p80"

    total_size  =    1048576   # bytes
    page_size   =        256   # bytes
    total_pages =       4096

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
    ]
    dummy_bits = 8


class M25P80_NONJEDEC(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.NONJEDEC
    device_id = 0x0000
    name = "m25p80-nonjedec"

    total_size  =    1048576   # bytes
    page_size   =        256   # bytes
    total_pages =       4096

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
    ]
    dummy_bits = 8


class M25PE10(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.ST
    device_id = 0x8011
    name = "m25pe10"

    total_size  =     131072   # bytes
    page_size   =        256   # bytes
    total_pages =        512

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class M25PE16(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.ST
    device_id = 0x8015
    name = "m25pe16"

    total_size  =    2097152   # bytes
    page_size   =        256   # bytes
    total_pages =       8192

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
    ]
    dummy_bits = 8


class M25PE20(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.ST
    device_id = 0x8012
    name = "m25pe20"

    total_size  =     262144   # bytes
    page_size   =        256   # bytes
    total_pages =       1024

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
    ]
    dummy_bits = 8


class M25PE40(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.ST
    device_id = 0x8013
    name = "m25pe40"

    total_size  =     524288   # bytes
    page_size   =        256   # bytes
    total_pages =       2048

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class M25PE80(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.ST
    device_id = 0x8014
    name = "m25pe80"

    total_size  =    1048576   # bytes
    page_size   =        256   # bytes
    total_pages =       4096

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
    ]
    dummy_bits = 8


class M25PX16(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.ST
    device_id = 0x7115
    name = "m25px16"

    total_size  =    2097152   # bytes
    page_size   =        256   # bytes
    total_pages =       8192

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
    ]
    dummy_bits = 8


class M25PX32(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.ST
    device_id = 0x7116
    name = "m25px32"

    total_size  =    4194304   # bytes
    page_size   =        256   # bytes
    total_pages =      16384

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
    ]
    dummy_bits = 8


class M25PX32_S0(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.ST
    device_id = 0x7316
    name = "m25px32-s0"

    total_size  =    4194304   # bytes
    page_size   =        256   # bytes
    total_pages =      16384

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
    ]
    dummy_bits = 8


class M25PX32_S1(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.ST
    device_id = 0x6316
    name = "m25px32-s1"

    total_size  =    4194304   # bytes
    page_size   =        256   # bytes
    total_pages =      16384

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
    ]
    dummy_bits = 8


class M25PX64(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.ST
    device_id = 0x7117
    name = "m25px64"

    total_size  =    8388608   # bytes
    page_size   =        256   # bytes
    total_pages =      32768

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
    ]
    dummy_bits = 8


class M25PX80(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.ST
    device_id = 0x7114
    name = "m25px80"

    total_size  =    1048576   # bytes
    page_size   =        256   # bytes
    total_pages =       4096

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
    ]
    dummy_bits = 8


class M45PE10(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.ST
    device_id = 0x4011
    name = "m45pe10"

    total_size  =     131072   # bytes
    page_size   =        256   # bytes
    total_pages =        512

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
    ]
    dummy_bits = 8


class M45PE16(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.ST
    device_id = 0x4015
    name = "m45pe16"

    total_size  =    2097152   # bytes
    page_size   =        256   # bytes
    total_pages =       8192

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
    ]
    dummy_bits = 8


class M45PE20(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.ST
    device_id = 0x4012
    name = "m45pe20"

    total_size  =     262144   # bytes
    page_size   =        256   # bytes
    total_pages =       1024

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class M45PE40(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.ST
    device_id = 0x4013
    name = "m45pe40"

    total_size  =     524288   # bytes
    page_size   =        256   # bytes
    total_pages =       2048

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class M45PE80(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.ST
    device_id = 0x4014
    name = "m45pe80"

    total_size  =    1048576   # bytes
    page_size   =        256   # bytes
    total_pages =       4096

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
    ]
    dummy_bits = 8


class M95M02(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.ST
    device_id = 0x0012
    name = "m95m02"

    total_size  =     262144   # bytes
    page_size   =        256   # bytes
    total_pages =       1024

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class MB85RS1MT(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.FUJITSU
    device_id = 0x7f27
    name = "mb85rs1mt"

    total_size  =     131072   # bytes
    page_size   =        256   # bytes
    total_pages =        512

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
    ]
    dummy_bits = 8


class MR25H10(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.NONJEDEC
    device_id = 0x0000
    name = "mr25h10"

    total_size  =     131072   # bytes
    page_size   =        256   # bytes
    total_pages =        512

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class MR25H128(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.NONJEDEC
    device_id = 0x0000
    name = "mr25h128"

    total_size  =      16384   # bytes
    page_size   =        256   # bytes
    total_pages =         64

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class MR25H256(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.NONJEDEC
    device_id = 0x0000
    name = "mr25h256"

    total_size  =      32768   # bytes
    page_size   =        256   # bytes
    total_pages =        128

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class MR25H40(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.NONJEDEC
    device_id = 0x0000
    name = "mr25h40"

    total_size  =     524288   # bytes
    page_size   =        256   # bytes
    total_pages =       2048

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class MT25QL01(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.ST
    device_id = 0xba21
    name = "mt25ql01"

    total_size  =  134217728   # bytes
    page_size   =        256   # bytes
    total_pages =     524288

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class MT25QL01G(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.ST
    device_id = 0xba21
    name = "mt25ql01g"

    total_size  =  134217728   # bytes
    page_size   =        256   # bytes
    total_pages =     524288

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
        SpiNorFlashOpCodes.READ_1_1_1_4B,
        SpiNorFlashOpCodes.PP_1_1_1_4B,
        SpiNorFlashOpCodes.READ_1_1_1_FAST_4B,
    ]
    dummy_bits = 8


class MT25QL02(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.ST
    device_id = 0xba22
    name = "mt25ql02"

    total_size  =  268435456   # bytes
    page_size   =        256   # bytes
    total_pages =    1048576

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class MT25QL02G(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.ST
    device_id = 0xba22
    name = "mt25ql02g"

    total_size  =  268435456   # bytes
    page_size   =        256   # bytes
    total_pages =    1048576

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
        SpiNorFlashOpCodes.READ_1_1_4,
        SpiNorFlashOpCodes.PP_1_1_4,
    ]
    dummy_bits = 8


class MT25QL128(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.ST
    device_id = 0xba18
    name = "mt25ql128"

    total_size  =   16777216   # bytes
    page_size   =        256   # bytes
    total_pages =      65536

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
        SpiNorFlashOpCodes.READ_1_1_1_4B,
        SpiNorFlashOpCodes.PP_1_1_1_4B,
        SpiNorFlashOpCodes.READ_1_1_1_FAST_4B,
    ]
    dummy_bits = 8


class MT25QL256(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.ST
    device_id = 0xba19
    name = "mt25ql256"

    total_size  =   33554432   # bytes
    page_size   =        256   # bytes
    total_pages =     131072

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
        SpiNorFlashOpCodes.READ_1_1_1_4B,
        SpiNorFlashOpCodes.PP_1_1_1_4B,
        SpiNorFlashOpCodes.READ_1_1_1_FAST_4B,
    ]
    dummy_bits = 8


class MT25QL256A(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.ST
    device_id = 0xba19
    name = "mt25ql256a"

    total_size  =   33554432   # bytes
    page_size   =        256   # bytes
    total_pages =     131072

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
        SpiNorFlashOpCodes.READ_1_1_2,
        SpiNorFlashOpCodes.PP_1_1_2,
        SpiNorFlashOpCodes.READ_1_1_4,
        SpiNorFlashOpCodes.PP_1_1_4,
        SpiNorFlashOpCodes.READ_1_1_1_4B,
        SpiNorFlashOpCodes.PP_1_1_1_4B,
        SpiNorFlashOpCodes.READ_1_1_1_FAST_4B,
        SpiNorFlashOpCodes.READ_1_1_2_4B,
        SpiNorFlashOpCodes.READ_1_1_4_4B,
        SpiNorFlashOpCodes.PP_1_1_4_4B,
    ]
    dummy_bits = 8


class MT25QL512(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.ST
    device_id = 0xba20
    name = "mt25ql512"

    total_size  =   67108864   # bytes
    page_size   =        256   # bytes
    total_pages =     262144

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
        SpiNorFlashOpCodes.READ_1_1_1_4B,
        SpiNorFlashOpCodes.PP_1_1_1_4B,
        SpiNorFlashOpCodes.READ_1_1_1_FAST_4B,
    ]
    dummy_bits = 8


class MT25QL512A(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.ST
    device_id = 0xba20
    name = "mt25ql512a"

    total_size  =   67108864   # bytes
    page_size   =        256   # bytes
    total_pages =     262144

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
        SpiNorFlashOpCodes.READ_1_1_2,
        SpiNorFlashOpCodes.PP_1_1_2,
        SpiNorFlashOpCodes.READ_1_1_4,
        SpiNorFlashOpCodes.PP_1_1_4,
        SpiNorFlashOpCodes.READ_1_1_1_4B,
        SpiNorFlashOpCodes.PP_1_1_1_4B,
        SpiNorFlashOpCodes.READ_1_1_1_FAST_4B,
        SpiNorFlashOpCodes.READ_1_1_2_4B,
        SpiNorFlashOpCodes.READ_1_1_4_4B,
        SpiNorFlashOpCodes.PP_1_1_4_4B,
    ]
    dummy_bits = 8


class MT25QU01G(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.ST
    device_id = 0xbb21
    name = "mt25qu01g"

    total_size  =  134217728   # bytes
    page_size   =        256   # bytes
    total_pages =     524288

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
        SpiNorFlashOpCodes.READ_1_1_1_4B,
        SpiNorFlashOpCodes.PP_1_1_1_4B,
        SpiNorFlashOpCodes.READ_1_1_1_FAST_4B,
    ]
    dummy_bits = 8


class MT25QU02G(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.ST
    device_id = 0xbb22
    name = "mt25qu02g"

    total_size  =  268435456   # bytes
    page_size   =        256   # bytes
    total_pages =    1048576

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
        SpiNorFlashOpCodes.READ_1_1_4,
        SpiNorFlashOpCodes.PP_1_1_4,
    ]
    dummy_bits = 8


class MT25QU128(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.ST
    device_id = 0xbb18
    name = "mt25qu128"

    total_size  =   16777216   # bytes
    page_size   =        256   # bytes
    total_pages =      65536

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
        SpiNorFlashOpCodes.READ_1_1_1_4B,
        SpiNorFlashOpCodes.PP_1_1_1_4B,
        SpiNorFlashOpCodes.READ_1_1_1_FAST_4B,
    ]
    dummy_bits = 8


class MT25QU256(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.ST
    device_id = 0xbb19
    name = "mt25qu256"

    total_size  =   33554432   # bytes
    page_size   =        256   # bytes
    total_pages =     131072

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
        SpiNorFlashOpCodes.READ_1_1_1_4B,
        SpiNorFlashOpCodes.PP_1_1_1_4B,
        SpiNorFlashOpCodes.READ_1_1_1_FAST_4B,
    ]
    dummy_bits = 8


class MT25QU256A(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.ST
    device_id = 0xbb19
    name = "mt25qu256a"

    total_size  =   33554432   # bytes
    page_size   =        256   # bytes
    total_pages =     131072

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
        SpiNorFlashOpCodes.READ_1_1_2,
        SpiNorFlashOpCodes.PP_1_1_2,
        SpiNorFlashOpCodes.READ_1_1_4,
        SpiNorFlashOpCodes.PP_1_1_4,
        SpiNorFlashOpCodes.READ_1_1_1_4B,
        SpiNorFlashOpCodes.PP_1_1_1_4B,
        SpiNorFlashOpCodes.READ_1_1_1_FAST_4B,
        SpiNorFlashOpCodes.READ_1_1_2_4B,
        SpiNorFlashOpCodes.READ_1_1_4_4B,
        SpiNorFlashOpCodes.PP_1_1_4_4B,
    ]
    dummy_bits = 8


class MT25QU512(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.ST
    device_id = 0xbb20
    name = "mt25qu512"

    total_size  =   67108864   # bytes
    page_size   =        256   # bytes
    total_pages =     262144

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
        SpiNorFlashOpCodes.READ_1_1_1_4B,
        SpiNorFlashOpCodes.PP_1_1_1_4B,
        SpiNorFlashOpCodes.READ_1_1_1_FAST_4B,
    ]
    dummy_bits = 8


class MT25QU512A(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.ST
    device_id = 0xbb20
    name = "mt25qu512a"

    total_size  =   67108864   # bytes
    page_size   =        256   # bytes
    total_pages =     262144

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
        SpiNorFlashOpCodes.READ_1_1_2,
        SpiNorFlashOpCodes.PP_1_1_2,
        SpiNorFlashOpCodes.READ_1_1_4,
        SpiNorFlashOpCodes.PP_1_1_4,
        SpiNorFlashOpCodes.READ_1_1_1_4B,
        SpiNorFlashOpCodes.PP_1_1_1_4B,
        SpiNorFlashOpCodes.READ_1_1_1_FAST_4B,
        SpiNorFlashOpCodes.READ_1_1_2_4B,
        SpiNorFlashOpCodes.READ_1_1_4_4B,
        SpiNorFlashOpCodes.PP_1_1_4_4B,
    ]
    dummy_bits = 8


class MT35XU02G(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.MICRON
    device_id = 0x5b1c
    name = "mt35xu02g"

    total_size  =  268435456   # bytes
    page_size   =        256   # bytes
    total_pages =    1048576

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
        SpiNorFlashOpCodes.READ_1_1_8,
        SpiNorFlashOpCodes.PP_1_1_8,
        SpiNorFlashOpCodes.READ_1_1_1_4B,
        SpiNorFlashOpCodes.PP_1_1_1_4B,
        SpiNorFlashOpCodes.READ_1_1_1_FAST_4B,
        SpiNorFlashOpCodes.READ_1_1_8_4B,
        SpiNorFlashOpCodes.PP_1_1_8_4B,
    ]
    dummy_bits = 8


class MT35XU512ABA(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.MICRON
    device_id = 0x5b1a
    name = "mt35xu512aba"

    total_size  =   67108864   # bytes
    page_size   =        256   # bytes
    total_pages =     262144

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
        SpiNorFlashOpCodes.READ_1_1_8,
        SpiNorFlashOpCodes.PP_1_1_8,
        SpiNorFlashOpCodes.READ_1_1_1_4B,
        SpiNorFlashOpCodes.PP_1_1_1_4B,
        SpiNorFlashOpCodes.READ_1_1_1_FAST_4B,
        SpiNorFlashOpCodes.READ_1_1_8_4B,
        SpiNorFlashOpCodes.PP_1_1_8_4B,
    ]
    dummy_bits = 8


class MX23L12854(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.MACRONIX
    device_id = 0x0518
    name = "mx23l12854"

    total_size  =   16777216   # bytes
    page_size   =        256   # bytes
    total_pages =      65536

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class MX23L1654(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.MACRONIX
    device_id = 0x0515
    name = "mx23l1654"

    total_size  =    2097152   # bytes
    page_size   =        256   # bytes
    total_pages =       8192

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class MX23L3254(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.MACRONIX
    device_id = 0x0516
    name = "mx23l3254"

    total_size  =    4194304   # bytes
    page_size   =        256   # bytes
    total_pages =      16384

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class MX23L6454(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.MACRONIX
    device_id = 0x0517
    name = "mx23l6454"

    total_size  =    8388608   # bytes
    page_size   =        256   # bytes
    total_pages =      32768

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class MX25L1005(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.MACRONIX
    device_id = 0x2011
    name = "mx25l1005"

    total_size  =     131072   # bytes
    page_size   =        256   # bytes
    total_pages =        512

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class MX25L1005C(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.MACRONIX
    device_id = 0x2011
    name = "mx25l1005c"

    total_size  =     131072   # bytes
    page_size   =        256   # bytes
    total_pages =        512

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class MX25L1006E(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.MACRONIX
    device_id = 0x2011
    name = "mx25l1006e"

    total_size  =     131072   # bytes
    page_size   =        256   # bytes
    total_pages =        512

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class MX25L12805D(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.MACRONIX
    device_id = 0x2018
    name = "mx25l12805d"

    total_size  =   16777216   # bytes
    page_size   =        256   # bytes
    total_pages =      65536

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
    ]
    dummy_bits = 8


class MX25L12835F(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.MACRONIX
    device_id = 0x2018
    name = "mx25l12835f"

    total_size  =   16777216   # bytes
    page_size   =        256   # bytes
    total_pages =      65536

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class MX25L12845(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.MACRONIX
    device_id = 0x2018
    name = "mx25l12845"

    total_size  =   16777216   # bytes
    page_size   =        256   # bytes
    total_pages =      65536

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class MX25L12845E(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.MACRONIX
    device_id = 0x2018
    name = "mx25l12845e"

    total_size  =   16777216   # bytes
    page_size   =        256   # bytes
    total_pages =      65536

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class MX25L12855E(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.MACRONIX
    device_id = 0x2618
    name = "mx25l12855e"

    total_size  =   16777216   # bytes
    page_size   =        256   # bytes
    total_pages =      65536

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
    ]
    dummy_bits = 8


class MX25L12865E(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.MACRONIX
    device_id = 0x2018
    name = "mx25l12865e"

    total_size  =   16777216   # bytes
    page_size   =        256   # bytes
    total_pages =      65536

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class MX25L1605(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.MACRONIX
    device_id = 0x2015
    name = "mx25l1605"

    total_size  =    2097152   # bytes
    page_size   =        256   # bytes
    total_pages =       8192

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class MX25L1605D(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.MACRONIX
    device_id = 0x2015
    name = "mx25l1605d"

    total_size  =    2097152   # bytes
    page_size   =        256   # bytes
    total_pages =       8192

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class MX25L1606E(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.MACRONIX
    device_id = 0x2015
    name = "mx25l1606e"

    total_size  =    2097152   # bytes
    page_size   =        256   # bytes
    total_pages =       8192

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
    ]
    dummy_bits = 8


class MX25L1608D(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.MACRONIX
    device_id = 0x2015
    name = "mx25l1608d"

    total_size  =    2097152   # bytes
    page_size   =        256   # bytes
    total_pages =       8192

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class MX25L1635D(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.MACRONIX
    device_id = 0x2415
    name = "mx25l1635d"

    total_size  =    2097152   # bytes
    page_size   =        256   # bytes
    total_pages =       8192

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class MX25L1635E(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.MACRONIX
    device_id = 0x2515
    name = "mx25l1635e"

    total_size  =    2097152   # bytes
    page_size   =        256   # bytes
    total_pages =       8192

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class MX25L1673E(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.MACRONIX
    device_id = 0x2015
    name = "mx25l1673e"

    total_size  =    2097152   # bytes
    page_size   =        256   # bytes
    total_pages =       8192

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class MX25L2005(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.MACRONIX
    device_id = 0x2012
    name = "mx25l2005"

    total_size  =     262144   # bytes
    page_size   =        256   # bytes
    total_pages =       1024

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class MX25L2005A(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.MACRONIX
    device_id = 0x2012
    name = "mx25l2005a"

    total_size  =     262144   # bytes
    page_size   =        256   # bytes
    total_pages =       1024

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
    ]
    dummy_bits = 8


class MX25L2005C(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.MACRONIX
    device_id = 0x2012
    name = "mx25l2005c"

    total_size  =     262144   # bytes
    page_size   =        256   # bytes
    total_pages =       1024

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class MX25L2006E(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.MACRONIX
    device_id = 0x2012
    name = "mx25l2006e"

    total_size  =     262144   # bytes
    page_size   =        256   # bytes
    total_pages =       1024

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class MX25L25635E(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.MACRONIX
    device_id = 0x2019
    name = "mx25l25635e"

    total_size  =   33554432   # bytes
    page_size   =        256   # bytes
    total_pages =     131072

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
        SpiNorFlashOpCodes.READ_1_1_2,
        SpiNorFlashOpCodes.PP_1_1_2,
        SpiNorFlashOpCodes.READ_1_1_4,
        SpiNorFlashOpCodes.PP_1_1_4,
    ]
    dummy_bits = 8


class MX25L25635F(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.MACRONIX
    device_id = 0x2019
    name = "mx25l25635f"

    total_size  =   33554432   # bytes
    page_size   =        256   # bytes
    total_pages =     131072

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
        SpiNorFlashOpCodes.READ_1_1_1_4B,
        SpiNorFlashOpCodes.PP_1_1_1_4B,
        SpiNorFlashOpCodes.READ_1_1_1_FAST_4B,
    ]
    dummy_bits = 8


class MX25L25645(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.MACRONIX
    device_id = 0x2019
    name = "mx25l25645"

    total_size  =   33554432   # bytes
    page_size   =        256   # bytes
    total_pages =     131072

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class MX25L25645G(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.MACRONIX
    device_id = 0x2019
    name = "mx25l25645g"

    total_size  =   33554432   # bytes
    page_size   =        256   # bytes
    total_pages =     131072

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
        SpiNorFlashOpCodes.READ_1_1_1_4B,
        SpiNorFlashOpCodes.PP_1_1_1_4B,
        SpiNorFlashOpCodes.READ_1_1_1_FAST_4B,
    ]
    dummy_bits = 8


class MX25L25655E(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.MACRONIX
    device_id = 0x2619
    name = "mx25l25655e"

    total_size  =   33554432   # bytes
    page_size   =        256   # bytes
    total_pages =     131072

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
    ]
    dummy_bits = 8


class MX25L3205(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.MACRONIX
    device_id = 0x2016
    name = "mx25l3205"

    total_size  =    4194304   # bytes
    page_size   =        256   # bytes
    total_pages =      16384

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class MX25L3205D(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.MACRONIX
    device_id = 0x2016
    name = "mx25l3205d"

    total_size  =    4194304   # bytes
    page_size   =        256   # bytes
    total_pages =      16384

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
    ]
    dummy_bits = 8


class MX25L3235D(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.MACRONIX
    device_id = 0x5e16
    name = "mx25l3235d"

    total_size  =    4194304   # bytes
    page_size   =        256   # bytes
    total_pages =      16384

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class MX25L3255E(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.MACRONIX
    device_id = 0x9e16
    name = "mx25l3255e"

    total_size  =    4194304   # bytes
    page_size   =        256   # bytes
    total_pages =      16384

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
    ]
    dummy_bits = 8


class MX25L3273E(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.MACRONIX
    device_id = 0x2016
    name = "mx25l3273e"

    total_size  =    4194304   # bytes
    page_size   =        256   # bytes
    total_pages =      16384

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class MX25L4005(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.MACRONIX
    device_id = 0x2013
    name = "mx25l4005"

    total_size  =     524288   # bytes
    page_size   =        256   # bytes
    total_pages =       2048

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class MX25L4005A(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.MACRONIX
    device_id = 0x2013
    name = "mx25l4005a"

    total_size  =     524288   # bytes
    page_size   =        256   # bytes
    total_pages =       2048

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
    ]
    dummy_bits = 8


class MX25L4005C(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.MACRONIX
    device_id = 0x2013
    name = "mx25l4005c"

    total_size  =     524288   # bytes
    page_size   =        256   # bytes
    total_pages =       2048

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class MX25L4006E(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.MACRONIX
    device_id = 0x2013
    name = "mx25l4006e"

    total_size  =     524288   # bytes
    page_size   =        256   # bytes
    total_pages =       2048

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class MX25L512(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.MACRONIX
    device_id = 0x2010
    name = "mx25l512"

    total_size  =      65536   # bytes
    page_size   =        256   # bytes
    total_pages =        256

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class MX25L51245(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.MACRONIX
    device_id = 0x201a
    name = "mx25l51245"

    total_size  =   67108864   # bytes
    page_size   =        256   # bytes
    total_pages =     262144

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class MX25L51245G(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.MACRONIX
    device_id = 0x201a
    name = "mx25l51245g"

    total_size  =   67108864   # bytes
    page_size   =        256   # bytes
    total_pages =     262144

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
        SpiNorFlashOpCodes.READ_1_1_1_4B,
        SpiNorFlashOpCodes.PP_1_1_1_4B,
        SpiNorFlashOpCodes.READ_1_1_1_FAST_4B,
    ]
    dummy_bits = 8


class MX25L512E(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.MACRONIX
    device_id = 0x2010
    name = "mx25l512e"

    total_size  =      65536   # bytes
    page_size   =        256   # bytes
    total_pages =        256

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
    ]
    dummy_bits = 8


class MX25L6405(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.MACRONIX
    device_id = 0x2017
    name = "mx25l6405"

    total_size  =    8388608   # bytes
    page_size   =        256   # bytes
    total_pages =      32768

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class MX25L6405D(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.MACRONIX
    device_id = 0x2017
    name = "mx25l6405d"

    total_size  =    8388608   # bytes
    page_size   =        256   # bytes
    total_pages =      32768

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
    ]
    dummy_bits = 8


class MX25L6436E(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.MACRONIX
    device_id = 0x2017
    name = "mx25l6436e"

    total_size  =    8388608   # bytes
    page_size   =        256   # bytes
    total_pages =      32768

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class MX25L6445E(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.MACRONIX
    device_id = 0x2017
    name = "mx25l6445e"

    total_size  =    8388608   # bytes
    page_size   =        256   # bytes
    total_pages =      32768

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class MX25L6465E(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.MACRONIX
    device_id = 0x2017
    name = "mx25l6465e"

    total_size  =    8388608   # bytes
    page_size   =        256   # bytes
    total_pages =      32768

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class MX25L6473E(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.MACRONIX
    device_id = 0x2017
    name = "mx25l6473e"

    total_size  =    8388608   # bytes
    page_size   =        256   # bytes
    total_pages =      32768

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class MX25L6473F(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.MACRONIX
    device_id = 0x2017
    name = "mx25l6473f"

    total_size  =    8388608   # bytes
    page_size   =        256   # bytes
    total_pages =      32768

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class MX25L6495F(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.MACRONIX
    device_id = 0x9517
    name = "mx25l6495f"

    total_size  =    8388608   # bytes
    page_size   =        256   # bytes
    total_pages =      32768

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class MX25L8005(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.MACRONIX
    device_id = 0x2014
    name = "mx25l8005"

    total_size  =    1048576   # bytes
    page_size   =        256   # bytes
    total_pages =       4096

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
    ]
    dummy_bits = 8


class MX25L8006E(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.MACRONIX
    device_id = 0x2014
    name = "mx25l8006e"

    total_size  =    1048576   # bytes
    page_size   =        256   # bytes
    total_pages =       4096

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class MX25L8008E(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.MACRONIX
    device_id = 0x2014
    name = "mx25l8008e"

    total_size  =    1048576   # bytes
    page_size   =        256   # bytes
    total_pages =       4096

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class MX25LM51245(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.MACRONIX
    device_id = 0x853a
    name = "mx25lm51245"

    total_size  =   67108864   # bytes
    page_size   =        256   # bytes
    total_pages =     262144

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_8,
        SpiNorFlashOpCodes.PP_1_1_8,
    ]
    dummy_bits = 8


class MX25R1035F(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.MACRONIX
    device_id = 0x2811
    name = "mx25r1035f"

    total_size  =     131072   # bytes
    page_size   =        256   # bytes
    total_pages =        512

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_2,
        SpiNorFlashOpCodes.PP_1_1_2,
        SpiNorFlashOpCodes.READ_1_1_4,
        SpiNorFlashOpCodes.PP_1_1_4,
    ]
    dummy_bits = 8


class MX25R1635F(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.MACRONIX
    device_id = 0x2815
    name = "mx25r1635f"

    total_size  =    2097152   # bytes
    page_size   =        256   # bytes
    total_pages =       8192

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_2,
        SpiNorFlashOpCodes.PP_1_1_2,
        SpiNorFlashOpCodes.READ_1_1_4,
        SpiNorFlashOpCodes.PP_1_1_4,
    ]
    dummy_bits = 8


class MX25R2035F(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.MACRONIX
    device_id = 0x2812
    name = "mx25r2035f"

    total_size  =     262144   # bytes
    page_size   =        256   # bytes
    total_pages =       1024

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_2,
        SpiNorFlashOpCodes.PP_1_1_2,
        SpiNorFlashOpCodes.READ_1_1_4,
        SpiNorFlashOpCodes.PP_1_1_4,
    ]
    dummy_bits = 8


class MX25R3235F(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.MACRONIX
    device_id = 0x2816
    name = "mx25r3235f"

    total_size  =    4194304   # bytes
    page_size   =        256   # bytes
    total_pages =      16384

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
        SpiNorFlashOpCodes.READ_1_1_2,
        SpiNorFlashOpCodes.PP_1_1_2,
        SpiNorFlashOpCodes.READ_1_1_4,
        SpiNorFlashOpCodes.PP_1_1_4,
    ]
    dummy_bits = 8


class MX25R4035F(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.MACRONIX
    device_id = 0x2813
    name = "mx25r4035f"

    total_size  =     524288   # bytes
    page_size   =        256   # bytes
    total_pages =       2048

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_2,
        SpiNorFlashOpCodes.PP_1_1_2,
        SpiNorFlashOpCodes.READ_1_1_4,
        SpiNorFlashOpCodes.PP_1_1_4,
    ]
    dummy_bits = 8


class MX25R512F(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.MACRONIX
    device_id = 0x2810
    name = "mx25r512f"

    total_size  =      65536   # bytes
    page_size   =        256   # bytes
    total_pages =        256

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_2,
        SpiNorFlashOpCodes.PP_1_1_2,
        SpiNorFlashOpCodes.READ_1_1_4,
        SpiNorFlashOpCodes.PP_1_1_4,
    ]
    dummy_bits = 8


class MX25R6435F(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.MACRONIX
    device_id = 0x2817
    name = "mx25r6435f"

    total_size  =    8388608   # bytes
    page_size   =        256   # bytes
    total_pages =      32768

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class MX25R8035F(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.MACRONIX
    device_id = 0x2814
    name = "mx25r8035f"

    total_size  =    1048576   # bytes
    page_size   =        256   # bytes
    total_pages =       4096

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_2,
        SpiNorFlashOpCodes.PP_1_1_2,
        SpiNorFlashOpCodes.READ_1_1_4,
        SpiNorFlashOpCodes.PP_1_1_4,
    ]
    dummy_bits = 8


class MX25U12835F(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.MACRONIX
    device_id = 0x2538
    name = "mx25u12835f"

    total_size  =   16777216   # bytes
    page_size   =        256   # bytes
    total_pages =      65536

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
        SpiNorFlashOpCodes.READ_1_1_2,
        SpiNorFlashOpCodes.PP_1_1_2,
        SpiNorFlashOpCodes.READ_1_1_4,
        SpiNorFlashOpCodes.PP_1_1_4,
    ]
    dummy_bits = 8


class MX25U1635E(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.MACRONIX
    device_id = 0x2535
    name = "mx25u1635e"

    total_size  =    2097152   # bytes
    page_size   =        256   # bytes
    total_pages =       8192

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_4,
        SpiNorFlashOpCodes.PP_1_1_4,
    ]
    dummy_bits = 8


class MX25U2033E(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.MACRONIX
    device_id = 0x2532
    name = "mx25u2033e"

    total_size  =     262144   # bytes
    page_size   =        256   # bytes
    total_pages =       1024

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
    ]
    dummy_bits = 8


class MX25U25635F(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.MACRONIX
    device_id = 0x2539
    name = "mx25u25635f"

    total_size  =   33554432   # bytes
    page_size   =        256   # bytes
    total_pages =     131072

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
        SpiNorFlashOpCodes.READ_1_1_1_4B,
        SpiNorFlashOpCodes.PP_1_1_1_4B,
        SpiNorFlashOpCodes.READ_1_1_1_FAST_4B,
    ]
    dummy_bits = 8


class MX25U3235E(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.MACRONIX
    device_id = 0x2536
    name = "mx25u3235e"

    total_size  =    4194304   # bytes
    page_size   =        256   # bytes
    total_pages =      16384

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_4,
        SpiNorFlashOpCodes.PP_1_1_4,
    ]
    dummy_bits = 8


class MX25U3235F(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.MACRONIX
    device_id = 0x2536
    name = "mx25u3235f"

    total_size  =    4194304   # bytes
    page_size   =        256   # bytes
    total_pages =      16384

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
        SpiNorFlashOpCodes.READ_1_1_2,
        SpiNorFlashOpCodes.PP_1_1_2,
        SpiNorFlashOpCodes.READ_1_1_4,
        SpiNorFlashOpCodes.PP_1_1_4,
    ]
    dummy_bits = 8


class MX25U4035(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.MACRONIX
    device_id = 0x2533
    name = "mx25u4035"

    total_size  =     524288   # bytes
    page_size   =        256   # bytes
    total_pages =       2048

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
    ]
    dummy_bits = 8


class MX25U51245G(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.MACRONIX
    device_id = 0x253a
    name = "mx25u51245g"

    total_size  =   67108864   # bytes
    page_size   =        256   # bytes
    total_pages =     262144

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
        SpiNorFlashOpCodes.READ_1_1_4,
        SpiNorFlashOpCodes.PP_1_1_4,
        SpiNorFlashOpCodes.READ_1_1_1_4B,
        SpiNorFlashOpCodes.PP_1_1_1_4B,
        SpiNorFlashOpCodes.READ_1_1_1_FAST_4B,
        SpiNorFlashOpCodes.READ_1_1_4_4B,
        SpiNorFlashOpCodes.PP_1_1_4_4B,
    ]
    dummy_bits = 8


class MX25U6435E(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.MACRONIX
    device_id = 0x2537
    name = "mx25u6435e"

    total_size  =    8388608   # bytes
    page_size   =        256   # bytes
    total_pages =      32768

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_4,
        SpiNorFlashOpCodes.PP_1_1_4,
    ]
    dummy_bits = 8


class MX25U6435F(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.MACRONIX
    device_id = 0x2537
    name = "mx25u6435f"

    total_size  =    8388608   # bytes
    page_size   =        256   # bytes
    total_pages =      32768

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
    ]
    dummy_bits = 8


class MX25U8032E(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.MACRONIX
    device_id = 0x2534
    name = "mx25u8032e"

    total_size  =    1048576   # bytes
    page_size   =        256   # bytes
    total_pages =       4096

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class MX25U8035(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.MACRONIX
    device_id = 0x2534
    name = "mx25u8035"

    total_size  =    1048576   # bytes
    page_size   =        256   # bytes
    total_pages =       4096

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
    ]
    dummy_bits = 8


class MX25V512(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.MACRONIX
    device_id = 0x2010
    name = "mx25v512"

    total_size  =      65536   # bytes
    page_size   =        256   # bytes
    total_pages =        256

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class MX25V512C(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.MACRONIX
    device_id = 0x2010
    name = "mx25v512c"

    total_size  =      65536   # bytes
    page_size   =        256   # bytes
    total_pages =        256

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class MX25V8005(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.MACRONIX
    device_id = 0x2014
    name = "mx25v8005"

    total_size  =    1048576   # bytes
    page_size   =        256   # bytes
    total_pages =       4096

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class MX25V8035F(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.MACRONIX
    device_id = 0x2314
    name = "mx25v8035f"

    total_size  =    1048576   # bytes
    page_size   =        256   # bytes
    total_pages =       4096

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
        SpiNorFlashOpCodes.READ_1_1_2,
        SpiNorFlashOpCodes.PP_1_1_2,
        SpiNorFlashOpCodes.READ_1_1_4,
        SpiNorFlashOpCodes.PP_1_1_4,
    ]
    dummy_bits = 8


class MX66L1G45G(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.MACRONIX
    device_id = 0x201b
    name = "mx66l1g45g"

    total_size  =  134217728   # bytes
    page_size   =        256   # bytes
    total_pages =     524288

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
        SpiNorFlashOpCodes.READ_1_1_2,
        SpiNorFlashOpCodes.PP_1_1_2,
        SpiNorFlashOpCodes.READ_1_1_4,
        SpiNorFlashOpCodes.PP_1_1_4,
    ]
    dummy_bits = 8


class MX66L1G55G(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.MACRONIX
    device_id = 0x261b
    name = "mx66l1g55g"

    total_size  =  134217728   # bytes
    page_size   =        256   # bytes
    total_pages =     524288

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
        SpiNorFlashOpCodes.READ_1_1_4,
        SpiNorFlashOpCodes.PP_1_1_4,
    ]
    dummy_bits = 8


class MX66L51235F(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.MACRONIX
    device_id = 0x201a
    name = "mx66l51235f"

    total_size  =   67108864   # bytes
    page_size   =        256   # bytes
    total_pages =     262144

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
        SpiNorFlashOpCodes.READ_1_1_1_4B,
        SpiNorFlashOpCodes.PP_1_1_1_4B,
        SpiNorFlashOpCodes.READ_1_1_1_FAST_4B,
    ]
    dummy_bits = 8


class MX66L51235L(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.MACRONIX
    device_id = 0x201a
    name = "mx66l51235l"

    total_size  =   67108864   # bytes
    page_size   =        256   # bytes
    total_pages =     262144

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
        SpiNorFlashOpCodes.READ_1_1_2,
        SpiNorFlashOpCodes.PP_1_1_2,
        SpiNorFlashOpCodes.READ_1_1_4,
        SpiNorFlashOpCodes.PP_1_1_4,
        SpiNorFlashOpCodes.READ_1_1_1_4B,
        SpiNorFlashOpCodes.PP_1_1_1_4B,
        SpiNorFlashOpCodes.READ_1_1_1_FAST_4B,
        SpiNorFlashOpCodes.READ_1_1_2_4B,
        SpiNorFlashOpCodes.READ_1_1_4_4B,
        SpiNorFlashOpCodes.PP_1_1_4_4B,
    ]
    dummy_bits = 8


class MX66U51235F(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.MACRONIX
    device_id = 0x253a
    name = "mx66u51235f"

    total_size  =   67108864   # bytes
    page_size   =        256   # bytes
    total_pages =     262144

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
        SpiNorFlashOpCodes.READ_1_1_2,
        SpiNorFlashOpCodes.PP_1_1_2,
        SpiNorFlashOpCodes.READ_1_1_4,
        SpiNorFlashOpCodes.PP_1_1_4,
        SpiNorFlashOpCodes.READ_1_1_1_4B,
        SpiNorFlashOpCodes.PP_1_1_1_4B,
        SpiNorFlashOpCodes.READ_1_1_1_FAST_4B,
        SpiNorFlashOpCodes.READ_1_1_2_4B,
        SpiNorFlashOpCodes.READ_1_1_4_4B,
        SpiNorFlashOpCodes.PP_1_1_4_4B,
    ]
    dummy_bits = 8


class N25Q00(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.ST
    device_id = 0xba21
    name = "n25q00"

    total_size  =  134217728   # bytes
    page_size   =        256   # bytes
    total_pages =     524288

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
        SpiNorFlashOpCodes.READ_1_1_4,
        SpiNorFlashOpCodes.PP_1_1_4,
    ]
    dummy_bits = 8


class N25Q00A(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.ST
    device_id = 0xbb21
    name = "n25q00a"

    total_size  =  134217728   # bytes
    page_size   =        256   # bytes
    total_pages =     524288

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
        SpiNorFlashOpCodes.READ_1_1_4,
        SpiNorFlashOpCodes.PP_1_1_4,
    ]
    dummy_bits = 8


class N25Q016(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.ST
    device_id = 0xbb15
    name = "n25q016"

    total_size  =    2097152   # bytes
    page_size   =        256   # bytes
    total_pages =       8192

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class N25Q016A(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.ST
    device_id = 0xbb15
    name = "n25q016a"

    total_size  =    2097152   # bytes
    page_size   =        256   # bytes
    total_pages =       8192

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
        SpiNorFlashOpCodes.READ_1_1_4,
        SpiNorFlashOpCodes.PP_1_1_4,
    ]
    dummy_bits = 8


class N25Q032(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.ST
    device_id = 0xba16
    name = "n25q032"

    total_size  =    4194304   # bytes
    page_size   =        256   # bytes
    total_pages =      16384

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
        SpiNorFlashOpCodes.READ_1_1_4,
        SpiNorFlashOpCodes.PP_1_1_4,
    ]
    dummy_bits = 8


class N25Q032XX1E(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.ST
    device_id = 0xbb16
    name = "n25q032..1e"

    total_size  =    4194304   # bytes
    page_size   =        256   # bytes
    total_pages =      16384

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class N25Q032XX3E(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.ST
    device_id = 0xba16
    name = "n25q032..3e"

    total_size  =    4194304   # bytes
    page_size   =        256   # bytes
    total_pages =      16384

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class N25Q032A(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.ST
    device_id = 0xbb16
    name = "n25q032a"

    total_size  =    4194304   # bytes
    page_size   =        256   # bytes
    total_pages =      16384

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
        SpiNorFlashOpCodes.READ_1_1_4,
        SpiNorFlashOpCodes.PP_1_1_4,
    ]
    dummy_bits = 8


class N25Q064(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.ST
    device_id = 0xba17
    name = "n25q064"

    total_size  =    8388608   # bytes
    page_size   =        256   # bytes
    total_pages =      32768

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
        SpiNorFlashOpCodes.READ_1_1_4,
        SpiNorFlashOpCodes.PP_1_1_4,
    ]
    dummy_bits = 8


class N25Q064XX1E(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.ST
    device_id = 0xbb17
    name = "n25q064..1e"

    total_size  =    8388608   # bytes
    page_size   =        256   # bytes
    total_pages =      32768

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class N25Q064XX3E(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.ST
    device_id = 0xba17
    name = "n25q064..3e"

    total_size  =    8388608   # bytes
    page_size   =        256   # bytes
    total_pages =      32768

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class N25Q064A(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.ST
    device_id = 0xbb17
    name = "n25q064a"

    total_size  =    8388608   # bytes
    page_size   =        256   # bytes
    total_pages =      32768

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
        SpiNorFlashOpCodes.READ_1_1_4,
        SpiNorFlashOpCodes.PP_1_1_4,
    ]
    dummy_bits = 8


class N25Q128(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.ST
    device_id = 0xba18
    name = "n25q128"

    total_size  =   16777216   # bytes
    page_size   =        256   # bytes
    total_pages =      65536

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class N25Q128A11(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.ST
    device_id = 0xbb18
    name = "n25q128a11"

    total_size  =   16777216   # bytes
    page_size   =        256   # bytes
    total_pages =      65536

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
        SpiNorFlashOpCodes.READ_1_1_4,
        SpiNorFlashOpCodes.PP_1_1_4,
    ]
    dummy_bits = 8


class N25Q128A13(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.ST
    device_id = 0xba18
    name = "n25q128a13"

    total_size  =   16777216   # bytes
    page_size   =        256   # bytes
    total_pages =      65536

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
        SpiNorFlashOpCodes.READ_1_1_4,
        SpiNorFlashOpCodes.PP_1_1_4,
    ]
    dummy_bits = 8


class N25Q256XX1E(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.ST
    device_id = 0xbb19
    name = "n25q256..1e"

    total_size  =   33554432   # bytes
    page_size   =        256   # bytes
    total_pages =     131072

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class N25Q256XX3E(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.ST
    device_id = 0xba19
    name = "n25q256..3e"

    total_size  =   33554432   # bytes
    page_size   =        256   # bytes
    total_pages =     131072

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class N25Q256A(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.ST
    device_id = 0xba19
    name = "n25q256a"

    total_size  =   33554432   # bytes
    page_size   =        256   # bytes
    total_pages =     131072

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
        SpiNorFlashOpCodes.READ_1_1_2,
        SpiNorFlashOpCodes.PP_1_1_2,
        SpiNorFlashOpCodes.READ_1_1_4,
        SpiNorFlashOpCodes.PP_1_1_4,
    ]
    dummy_bits = 8


class N25Q256AX1(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.ST
    device_id = 0xbb19
    name = "n25q256ax1"

    total_size  =   33554432   # bytes
    page_size   =        256   # bytes
    total_pages =     131072

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
        SpiNorFlashOpCodes.READ_1_1_4,
        SpiNorFlashOpCodes.PP_1_1_4,
    ]
    dummy_bits = 8


class N25Q512A(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.ST
    device_id = 0xbb20
    name = "n25q512a"

    total_size  =   67108864   # bytes
    page_size   =        256   # bytes
    total_pages =     262144

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
        SpiNorFlashOpCodes.READ_1_1_4,
        SpiNorFlashOpCodes.PP_1_1_4,
    ]
    dummy_bits = 8


class N25Q512AX3(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.ST
    device_id = 0xba20
    name = "n25q512ax3"

    total_size  =   67108864   # bytes
    page_size   =        256   # bytes
    total_pages =     262144

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
        SpiNorFlashOpCodes.READ_1_1_4,
        SpiNorFlashOpCodes.PP_1_1_4,
    ]
    dummy_bits = 8


class PM25LD010(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.ISSI
    device_id = 0x0021
    name = "pm25ld010"

    total_size  =     131072   # bytes
    page_size   =        256   # bytes
    total_pages =        512

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class PM25LD010C(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.ISSI
    device_id = 0x0021
    name = "pm25ld010c"

    total_size  =     131072   # bytes
    page_size   =        256   # bytes
    total_pages =        512

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class PM25LD020(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.ISSI
    device_id = 0x0022
    name = "pm25ld020"

    total_size  =     262144   # bytes
    page_size   =        256   # bytes
    total_pages =       1024

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class PM25LD020C(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.ISSI
    device_id = 0x0022
    name = "pm25ld020c"

    total_size  =     262144   # bytes
    page_size   =        256   # bytes
    total_pages =       1024

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class PM25LD256C(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.ISSI
    device_id = 0x002f
    name = "pm25ld256c"

    total_size  =      32768   # bytes
    page_size   =        256   # bytes
    total_pages =        128

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class PM25LD512(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.ISSI
    device_id = 0x0020
    name = "pm25ld512"

    total_size  =      65536   # bytes
    page_size   =        256   # bytes
    total_pages =        256

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class PM25LD512C(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.ISSI
    device_id = 0x0020
    name = "pm25ld512c"

    total_size  =      65536   # bytes
    page_size   =        256   # bytes
    total_pages =        256

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class PM25LQ016(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.ISSI
    device_id = 0x0045
    name = "pm25lq016"

    total_size  =    2097152   # bytes
    page_size   =        256   # bytes
    total_pages =       8192

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class PM25LQ020(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.ISSI
    device_id = 0x0042
    name = "pm25lq020"

    total_size  =     262144   # bytes
    page_size   =        256   # bytes
    total_pages =       1024

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class PM25LQ032(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.NONJEDEC
    device_id = 0x0046
    name = "pm25lq032"

    total_size  =    4194304   # bytes
    page_size   =        256   # bytes
    total_pages =      16384

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
    ]
    dummy_bits = 8


class PM25LQ032C(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.ISSI
    device_id = 0x0046
    name = "pm25lq032c"

    total_size  =    4194304   # bytes
    page_size   =        256   # bytes
    total_pages =      16384

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class PM25LQ040(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.ISSI
    device_id = 0x0043
    name = "pm25lq040"

    total_size  =     524288   # bytes
    page_size   =        256   # bytes
    total_pages =       2048

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class PM25LQ080(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.ISSI
    device_id = 0x0044
    name = "pm25lq080"

    total_size  =    1048576   # bytes
    page_size   =        256   # bytes
    total_pages =       4096

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class PM25LV010(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.NONJEDEC
    device_id = 0x0000
    name = "pm25lv010"

    total_size  =     131072   # bytes
    page_size   =        256   # bytes
    total_pages =        512

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
    ]
    dummy_bits = 8


class PM25LV010A(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.ISSI
    device_id = 0x007c
    name = "pm25lv010a"

    total_size  =     131072   # bytes
    page_size   =        256   # bytes
    total_pages =        512

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class PM25LV016B(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.ISSI
    device_id = 0x0014
    name = "pm25lv016b"

    total_size  =    2097152   # bytes
    page_size   =        256   # bytes
    total_pages =       8192

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class PM25LV020(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.ISSI
    device_id = 0x007d
    name = "pm25lv020"

    total_size  =     262144   # bytes
    page_size   =        256   # bytes
    total_pages =       1024

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class PM25LV040(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.ISSI
    device_id = 0x007e
    name = "pm25lv040"

    total_size  =     524288   # bytes
    page_size   =        256   # bytes
    total_pages =       2048

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class PM25LV080B(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.ISSI
    device_id = 0x0013
    name = "pm25lv080b"

    total_size  =    1048576   # bytes
    page_size   =        256   # bytes
    total_pages =       4096

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class PM25LV512(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.NONJEDEC
    device_id = 0x0000
    name = "pm25lv512"

    total_size  =      65536   # bytes
    page_size   =        256   # bytes
    total_pages =        256

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
    ]
    dummy_bits = 8


class PM25LV512A(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.ISSI
    device_id = 0x007b
    name = "pm25lv512a"

    total_size  =      65536   # bytes
    page_size   =        256   # bytes
    total_pages =        256

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class S25FL004(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.SPANSION
    device_id = 0x0212
    name = "s25fl004"

    total_size  =     524288   # bytes
    page_size   =        256   # bytes
    total_pages =       2048

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class S25FL004A(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.SPANSION
    device_id = 0x0212
    name = "s25fl004a"

    total_size  =     524288   # bytes
    page_size   =        256   # bytes
    total_pages =       2048

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class S25FL004K(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.WINBOND
    device_id = 0x4013
    name = "s25fl004k"

    total_size  =     524288   # bytes
    page_size   =        256   # bytes
    total_pages =       2048

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
        SpiNorFlashOpCodes.READ_1_1_2,
        SpiNorFlashOpCodes.PP_1_1_2,
        SpiNorFlashOpCodes.READ_1_1_4,
        SpiNorFlashOpCodes.PP_1_1_4,
    ]
    dummy_bits = 8


class S25FL008(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.SPANSION
    device_id = 0x0213
    name = "s25fl008"

    total_size  =    1048576   # bytes
    page_size   =        256   # bytes
    total_pages =       4096

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class S25FL008A(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.SPANSION
    device_id = 0x0213
    name = "s25fl008a"

    total_size  =    1048576   # bytes
    page_size   =        256   # bytes
    total_pages =       4096

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class S25FL008K(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.WINBOND
    device_id = 0x4014
    name = "s25fl008k"

    total_size  =    1048576   # bytes
    page_size   =        256   # bytes
    total_pages =       4096

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
        SpiNorFlashOpCodes.READ_1_1_2,
        SpiNorFlashOpCodes.PP_1_1_2,
        SpiNorFlashOpCodes.READ_1_1_4,
        SpiNorFlashOpCodes.PP_1_1_4,
    ]
    dummy_bits = 8


class S25FL016(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.SPANSION
    device_id = 0x0214
    name = "s25fl016"

    total_size  =    2097152   # bytes
    page_size   =        256   # bytes
    total_pages =       8192

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class S25FL016A(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.SPANSION
    device_id = 0x0214
    name = "s25fl016a"

    total_size  =    2097152   # bytes
    page_size   =        256   # bytes
    total_pages =       8192

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class S25FL016K(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.WINBOND
    device_id = 0x4015
    name = "s25fl016k"

    total_size  =    2097152   # bytes
    page_size   =        256   # bytes
    total_pages =       8192

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
        SpiNorFlashOpCodes.READ_1_1_2,
        SpiNorFlashOpCodes.PP_1_1_2,
        SpiNorFlashOpCodes.READ_1_1_4,
        SpiNorFlashOpCodes.PP_1_1_4,
    ]
    dummy_bits = 8


class S25FL032(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.SPANSION
    device_id = 0x0215
    name = "s25fl032"

    total_size  =    4194304   # bytes
    page_size   =        256   # bytes
    total_pages =      16384

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class S25FL032A(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.SPANSION
    device_id = 0x0215
    name = "s25fl032a"

    total_size  =    4194304   # bytes
    page_size   =        256   # bytes
    total_pages =      16384

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class S25FL032P(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.SPANSION
    device_id = 0x0215
    name = "s25fl032p"

    total_size  =    4194304   # bytes
    page_size   =        256   # bytes
    total_pages =      16384

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class S25FL064(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.SPANSION
    device_id = 0x0216
    name = "s25fl064"

    total_size  =    8388608   # bytes
    page_size   =        256   # bytes
    total_pages =      32768

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class S25FL064A(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.SPANSION
    device_id = 0x0216
    name = "s25fl064a"

    total_size  =    8388608   # bytes
    page_size   =        256   # bytes
    total_pages =      32768

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class S25FL064K(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.WINBOND
    device_id = 0x4017
    name = "s25fl064k"

    total_size  =    8388608   # bytes
    page_size   =        256   # bytes
    total_pages =      32768

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
    ]
    dummy_bits = 8


class S25FL064L(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.SPANSION
    device_id = 0x6017
    name = "s25fl064l"

    total_size  =    8388608   # bytes
    page_size   =        256   # bytes
    total_pages =      32768

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
        SpiNorFlashOpCodes.READ_1_1_2,
        SpiNorFlashOpCodes.PP_1_1_2,
        SpiNorFlashOpCodes.READ_1_1_4,
        SpiNorFlashOpCodes.PP_1_1_4,
        SpiNorFlashOpCodes.READ_1_1_1_4B,
        SpiNorFlashOpCodes.PP_1_1_1_4B,
        SpiNorFlashOpCodes.READ_1_1_1_FAST_4B,
        SpiNorFlashOpCodes.READ_1_1_2_4B,
        SpiNorFlashOpCodes.READ_1_1_4_4B,
        SpiNorFlashOpCodes.PP_1_1_4_4B,
    ]
    dummy_bits = 8


class S25FL064P(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.SPANSION
    device_id = 0x0216
    name = "s25fl064p"

    total_size  =    8388608   # bytes
    page_size   =        256   # bytes
    total_pages =      32768

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class S25FL116K(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.SPANSION
    device_id = 0x4015
    name = "s25fl116k"

    total_size  =    2097152   # bytes
    page_size   =        256   # bytes
    total_pages =       8192

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
        SpiNorFlashOpCodes.READ_1_1_2,
        SpiNorFlashOpCodes.PP_1_1_2,
        SpiNorFlashOpCodes.READ_1_1_4,
        SpiNorFlashOpCodes.PP_1_1_4,
    ]
    dummy_bits = 8


class S25FL128L(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.SPANSION
    device_id = 0x6018
    name = "s25fl128l"

    total_size  =   16777216   # bytes
    page_size   =        256   # bytes
    total_pages =      65536

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
        SpiNorFlashOpCodes.READ_1_1_2,
        SpiNorFlashOpCodes.PP_1_1_2,
        SpiNorFlashOpCodes.READ_1_1_4,
        SpiNorFlashOpCodes.PP_1_1_4,
        SpiNorFlashOpCodes.READ_1_1_1_4B,
        SpiNorFlashOpCodes.PP_1_1_1_4B,
        SpiNorFlashOpCodes.READ_1_1_1_FAST_4B,
        SpiNorFlashOpCodes.READ_1_1_2_4B,
        SpiNorFlashOpCodes.READ_1_1_4_4B,
        SpiNorFlashOpCodes.PP_1_1_4_4B,
    ]
    dummy_bits = 8


class S25FL128S(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.SPANSION
    device_id = 0x2018
    name = "s25fl128s"

    total_size  =   16777216   # bytes
    page_size   =        256   # bytes
    total_pages =      65536

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class S25FL128S0(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.SPANSION
    device_id = 0x2018
    name = "s25fl128s0"

    total_size  =   16777216   # bytes
    page_size   =        256   # bytes
    total_pages =      65536

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
        SpiNorFlashOpCodes.READ_1_1_2,
        SpiNorFlashOpCodes.PP_1_1_2,
        SpiNorFlashOpCodes.READ_1_1_4,
        SpiNorFlashOpCodes.PP_1_1_4,
    ]
    dummy_bits = 8


class S25FL128S1(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.SPANSION
    device_id = 0x2018
    name = "s25fl128s1"

    total_size  =   16777216   # bytes
    page_size   =        256   # bytes
    total_pages =      65536

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
        SpiNorFlashOpCodes.READ_1_1_2,
        SpiNorFlashOpCodes.PP_1_1_2,
        SpiNorFlashOpCodes.READ_1_1_4,
        SpiNorFlashOpCodes.PP_1_1_4,
    ]
    dummy_bits = 8


class S25FL129PXXXXXX1(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.SPANSION
    device_id = 0x2018
    name = "s25fl129p......1"

    total_size  =   16777216   # bytes
    page_size   =        256   # bytes
    total_pages =      65536

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class S25FL129P0(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.SPANSION
    device_id = 0x2018
    name = "s25fl129p0"

    total_size  =   16777216   # bytes
    page_size   =        256   # bytes
    total_pages =      65536

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
        SpiNorFlashOpCodes.READ_1_1_2,
        SpiNorFlashOpCodes.PP_1_1_2,
        SpiNorFlashOpCodes.READ_1_1_4,
        SpiNorFlashOpCodes.PP_1_1_4,
    ]
    dummy_bits = 8


class S25FL129P1(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.SPANSION
    device_id = 0x2018
    name = "s25fl129p1"

    total_size  =   16777216   # bytes
    page_size   =        256   # bytes
    total_pages =      65536

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
        SpiNorFlashOpCodes.READ_1_1_2,
        SpiNorFlashOpCodes.PP_1_1_2,
        SpiNorFlashOpCodes.READ_1_1_4,
        SpiNorFlashOpCodes.PP_1_1_4,
    ]
    dummy_bits = 8


class S25FL132K(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.SPANSION
    device_id = 0x4016
    name = "s25fl132k"

    total_size  =    4194304   # bytes
    page_size   =        256   # bytes
    total_pages =      16384

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
    ]
    dummy_bits = 8


class S25FL164K(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.SPANSION
    device_id = 0x4017
    name = "s25fl164k"

    total_size  =    8388608   # bytes
    page_size   =        256   # bytes
    total_pages =      32768

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
    ]
    dummy_bits = 8


class S25FL204K(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.SPANSION
    device_id = 0x4013
    name = "s25fl204k"

    total_size  =     524288   # bytes
    page_size   =        256   # bytes
    total_pages =       2048

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
        SpiNorFlashOpCodes.READ_1_1_2,
        SpiNorFlashOpCodes.PP_1_1_2,
    ]
    dummy_bits = 8


class S25FL208K(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.SPANSION
    device_id = 0x4014
    name = "s25fl208k"

    total_size  =    1048576   # bytes
    page_size   =        256   # bytes
    total_pages =       4096

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
        SpiNorFlashOpCodes.READ_1_1_2,
        SpiNorFlashOpCodes.PP_1_1_2,
    ]
    dummy_bits = 8


class S25FL216K(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.SPANSION
    device_id = 0x4015
    name = "s25fl216k"

    total_size  =    2097152   # bytes
    page_size   =        256   # bytes
    total_pages =       8192

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class S25FL256L(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.SPANSION
    device_id = 0x6019
    name = "s25fl256l"

    total_size  =   33554432   # bytes
    page_size   =        256   # bytes
    total_pages =     131072

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
        SpiNorFlashOpCodes.READ_1_1_2,
        SpiNorFlashOpCodes.PP_1_1_2,
        SpiNorFlashOpCodes.READ_1_1_4,
        SpiNorFlashOpCodes.PP_1_1_4,
        SpiNorFlashOpCodes.READ_1_1_1_4B,
        SpiNorFlashOpCodes.PP_1_1_1_4B,
        SpiNorFlashOpCodes.READ_1_1_1_FAST_4B,
        SpiNorFlashOpCodes.READ_1_1_2_4B,
        SpiNorFlashOpCodes.READ_1_1_4_4B,
        SpiNorFlashOpCodes.PP_1_1_4_4B,
    ]
    dummy_bits = 8


class S25FL256S(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.SPANSION
    device_id = 0x0219
    name = "s25fl256s"

    total_size  =   33554432   # bytes
    page_size   =        256   # bytes
    total_pages =     131072

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class S25FL256SXXXXXX0(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.SPANSION
    device_id = 0x0219
    name = "s25fl256s......0"

    total_size  =   33554432   # bytes
    page_size   =        256   # bytes
    total_pages =     131072

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
        SpiNorFlashOpCodes.READ_1_1_1_4B,
        SpiNorFlashOpCodes.PP_1_1_1_4B,
        SpiNorFlashOpCodes.READ_1_1_1_FAST_4B,
    ]
    dummy_bits = 8


class S25FL256S0(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.SPANSION
    device_id = 0x0219
    name = "s25fl256s0"

    total_size  =   33554432   # bytes
    page_size   =        256   # bytes
    total_pages =     131072

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
    ]
    dummy_bits = 8


class S25FL256S1(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.SPANSION
    device_id = 0x0219
    name = "s25fl256s1"

    total_size  =   33554432   # bytes
    page_size   =        256   # bytes
    total_pages =     131072

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
        SpiNorFlashOpCodes.READ_1_1_2,
        SpiNorFlashOpCodes.PP_1_1_2,
        SpiNorFlashOpCodes.READ_1_1_4,
        SpiNorFlashOpCodes.PP_1_1_4,
    ]
    dummy_bits = 8


class S25FL512S(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.SPANSION
    device_id = 0x0220
    name = "s25fl512s"

    total_size  =   67108864   # bytes
    page_size   =        256   # bytes
    total_pages =     262144

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
        SpiNorFlashOpCodes.READ_1_1_2,
        SpiNorFlashOpCodes.PP_1_1_2,
        SpiNorFlashOpCodes.READ_1_1_4,
        SpiNorFlashOpCodes.PP_1_1_4,
    ]
    dummy_bits = 8


class S25FS512S(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.SPANSION
    device_id = 0x0220
    name = "s25fs512s"

    total_size  =   67108864   # bytes
    page_size   =        256   # bytes
    total_pages =     262144

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
        SpiNorFlashOpCodes.READ_1_1_2,
        SpiNorFlashOpCodes.PP_1_1_2,
        SpiNorFlashOpCodes.READ_1_1_4,
        SpiNorFlashOpCodes.PP_1_1_4,
    ]
    dummy_bits = 8


class S25SL004A(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.SPANSION
    device_id = 0x0212
    name = "s25sl004a"

    total_size  =     524288   # bytes
    page_size   =        256   # bytes
    total_pages =       2048

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
    ]
    dummy_bits = 8


class S25SL008A(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.SPANSION
    device_id = 0x0213
    name = "s25sl008a"

    total_size  =    1048576   # bytes
    page_size   =        256   # bytes
    total_pages =       4096

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
    ]
    dummy_bits = 8


class S25SL016A(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.SPANSION
    device_id = 0x0214
    name = "s25sl016a"

    total_size  =    2097152   # bytes
    page_size   =        256   # bytes
    total_pages =       8192

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
    ]
    dummy_bits = 8


class S25SL032A(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.SPANSION
    device_id = 0x0215
    name = "s25sl032a"

    total_size  =    4194304   # bytes
    page_size   =        256   # bytes
    total_pages =      16384

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
    ]
    dummy_bits = 8


class S25SL032P(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.SPANSION
    device_id = 0x0215
    name = "s25sl032p"

    total_size  =    4194304   # bytes
    page_size   =        256   # bytes
    total_pages =      16384

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
        SpiNorFlashOpCodes.READ_1_1_2,
        SpiNorFlashOpCodes.PP_1_1_2,
        SpiNorFlashOpCodes.READ_1_1_4,
        SpiNorFlashOpCodes.PP_1_1_4,
    ]
    dummy_bits = 8


class S25SL064A(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.SPANSION
    device_id = 0x0216
    name = "s25sl064a"

    total_size  =    8388608   # bytes
    page_size   =        256   # bytes
    total_pages =      32768

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
    ]
    dummy_bits = 8


class S25SL064P(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.SPANSION
    device_id = 0x0216
    name = "s25sl064p"

    total_size  =    8388608   # bytes
    page_size   =        256   # bytes
    total_pages =      32768

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
        SpiNorFlashOpCodes.READ_1_1_2,
        SpiNorFlashOpCodes.PP_1_1_2,
        SpiNorFlashOpCodes.READ_1_1_4,
        SpiNorFlashOpCodes.PP_1_1_4,
    ]
    dummy_bits = 8


class S25SL12800(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.SPANSION
    device_id = 0x2018
    name = "s25sl12800"

    total_size  =   16777216   # bytes
    page_size   =        256   # bytes
    total_pages =      65536

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
    ]
    dummy_bits = 8


class S25SL12801(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.SPANSION
    device_id = 0x2018
    name = "s25sl12801"

    total_size  =   16777216   # bytes
    page_size   =        256   # bytes
    total_pages =      65536

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
    ]
    dummy_bits = 8


class S70FL01GS(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.SPANSION
    device_id = 0x0221
    name = "s70fl01gs"

    total_size  =   67108864   # bytes
    page_size   =        256   # bytes
    total_pages =     262144

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
    ]
    dummy_bits = 8


class SST25LF080(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.SST
    device_id = 0x0080
    name = "sst25lf080"

    total_size  =    1048576   # bytes
    page_size   =        256   # bytes
    total_pages =       4096

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class SST25LF080A(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.SST
    device_id = 0x0080
    name = "sst25lf080a"

    total_size  =    1048576   # bytes
    page_size   =        256   # bytes
    total_pages =       4096

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class SST25VF010(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.SST
    device_id = 0x0049
    name = "sst25vf010"

    total_size  =     131072   # bytes
    page_size   =        256   # bytes
    total_pages =        512

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class SST25VF010A(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.SST
    device_id = 0x0049
    name = "sst25vf010a"

    total_size  =     131072   # bytes
    page_size   =        256   # bytes
    total_pages =        512

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class SST25VF016B(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.SST
    device_id = 0x2541
    name = "sst25vf016b"

    total_size  =    2097152   # bytes
    page_size   =        256   # bytes
    total_pages =       8192

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
    ]
    dummy_bits = 8


class SST25VF020(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.SST
    device_id = 0x0043
    name = "sst25vf020"

    total_size  =     262144   # bytes
    page_size   =        256   # bytes
    total_pages =       1024

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class SST25VF020B(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.SST
    device_id = 0x258c
    name = "sst25vf020b"

    total_size  =     262144   # bytes
    page_size   =        256   # bytes
    total_pages =       1024

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class SST25VF032B(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.SST
    device_id = 0x254a
    name = "sst25vf032b"

    total_size  =    4194304   # bytes
    page_size   =        256   # bytes
    total_pages =      16384

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
    ]
    dummy_bits = 8


class SST25VF040(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.SST
    device_id = 0x0044
    name = "sst25vf040"

    total_size  =     524288   # bytes
    page_size   =        256   # bytes
    total_pages =       2048

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class SST25VF040B(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.SST
    device_id = 0x258d
    name = "sst25vf040b"

    total_size  =     524288   # bytes
    page_size   =        256   # bytes
    total_pages =       2048

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
    ]
    dummy_bits = 8


class SST25VF040BXREMS(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.SST
    device_id = 0x008d
    name = "sst25vf040b.rems"

    total_size  =     524288   # bytes
    page_size   =        256   # bytes
    total_pages =       2048

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class SST25VF064C(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.SST
    device_id = 0x254b
    name = "sst25vf064c"

    total_size  =    8388608   # bytes
    page_size   =        256   # bytes
    total_pages =      32768

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
    ]
    dummy_bits = 8


class SST25VF080B(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.SST
    device_id = 0x258e
    name = "sst25vf080b"

    total_size  =    1048576   # bytes
    page_size   =        256   # bytes
    total_pages =       4096

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
    ]
    dummy_bits = 8


class SST25VF512(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.SST
    device_id = 0x0048
    name = "sst25vf512"

    total_size  =      65536   # bytes
    page_size   =        256   # bytes
    total_pages =        256

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class SST25VF512A(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.SST
    device_id = 0x0048
    name = "sst25vf512a"

    total_size  =      65536   # bytes
    page_size   =        256   # bytes
    total_pages =        256

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class SST25WF010(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.SST
    device_id = 0x2502
    name = "sst25wf010"

    total_size  =     131072   # bytes
    page_size   =        256   # bytes
    total_pages =        512

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
    ]
    dummy_bits = 8


class SST25WF020(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.SST
    device_id = 0x2503
    name = "sst25wf020"

    total_size  =     262144   # bytes
    page_size   =        256   # bytes
    total_pages =       1024

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
    ]
    dummy_bits = 8


class SST25WF020A(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.SANYO
    device_id = 0x1612
    name = "sst25wf020a"

    total_size  =     262144   # bytes
    page_size   =        256   # bytes
    total_pages =       1024

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
    ]
    dummy_bits = 8


class SST25WF040(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.SST
    device_id = 0x2504
    name = "sst25wf040"

    total_size  =     524288   # bytes
    page_size   =        256   # bytes
    total_pages =       2048

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
    ]
    dummy_bits = 8


class SST25WF040B(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.SANYO
    device_id = 0x1613
    name = "sst25wf040b"

    total_size  =     524288   # bytes
    page_size   =        256   # bytes
    total_pages =       2048

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
    ]
    dummy_bits = 8


class SST25WF080(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.SST
    device_id = 0x2505
    name = "sst25wf080"

    total_size  =    1048576   # bytes
    page_size   =        256   # bytes
    total_pages =       4096

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
    ]
    dummy_bits = 8


class SST25WF080B(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.SST
    device_id = 0x1614
    name = "sst25wf080b"

    total_size  =    1048576   # bytes
    page_size   =        256   # bytes
    total_pages =       4096

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class SST25WF512(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.SST
    device_id = 0x2501
    name = "sst25wf512"

    total_size  =      65536   # bytes
    page_size   =        256   # bytes
    total_pages =        256

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
    ]
    dummy_bits = 8


class SST26VF016B(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.SST
    device_id = 0x2641
    name = "sst26vf016b"

    total_size  =    2097152   # bytes
    page_size   =        256   # bytes
    total_pages =       8192

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
        SpiNorFlashOpCodes.READ_1_1_2,
        SpiNorFlashOpCodes.PP_1_1_2,
    ]
    dummy_bits = 8


class SST26VF016BA(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.SST
    device_id = 0x2641
    name = "sst26vf016ba"

    total_size  =    2097152   # bytes
    page_size   =        256   # bytes
    total_pages =       8192

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class SST26VF032B(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.SST
    device_id = 0x2642
    name = "sst26vf032b"

    total_size  =    4194304   # bytes
    page_size   =        256   # bytes
    total_pages =      16384

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class SST26VF032BA(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.SST
    device_id = 0x2642
    name = "sst26vf032ba"

    total_size  =    4194304   # bytes
    page_size   =        256   # bytes
    total_pages =      16384

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class SST26VF064B(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.SST
    device_id = 0x2643
    name = "sst26vf064b"

    total_size  =    8388608   # bytes
    page_size   =        256   # bytes
    total_pages =      32768

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
        SpiNorFlashOpCodes.READ_1_1_2,
        SpiNorFlashOpCodes.PP_1_1_2,
        SpiNorFlashOpCodes.READ_1_1_4,
        SpiNorFlashOpCodes.PP_1_1_4,
    ]
    dummy_bits = 8


class SST26VF064BA(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.SST
    device_id = 0x2643
    name = "sst26vf064ba"

    total_size  =    8388608   # bytes
    page_size   =        256   # bytes
    total_pages =      32768

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class SST26WF016B(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.SST
    device_id = 0x2651
    name = "sst26wf016b"

    total_size  =    2097152   # bytes
    page_size   =        256   # bytes
    total_pages =       8192

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
        SpiNorFlashOpCodes.READ_1_1_2,
        SpiNorFlashOpCodes.PP_1_1_2,
        SpiNorFlashOpCodes.READ_1_1_4,
        SpiNorFlashOpCodes.PP_1_1_4,
    ]
    dummy_bits = 8


class W25M512JV(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.WINBOND
    device_id = 0x7119
    name = "w25m512jv"

    total_size  =   67108864   # bytes
    page_size   =        256   # bytes
    total_pages =     262144

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
        SpiNorFlashOpCodes.READ_1_1_2,
        SpiNorFlashOpCodes.PP_1_1_2,
        SpiNorFlashOpCodes.READ_1_1_4,
        SpiNorFlashOpCodes.PP_1_1_4,
    ]
    dummy_bits = 8


class W25Q128(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.WINBOND
    device_id = 0x4018
    name = "w25q128"

    total_size  =   16777216   # bytes
    page_size   =        256   # bytes
    total_pages =      65536

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
    ]
    dummy_bits = 8


class W25Q128FV(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.WINBOND
    device_id = 0x4018
    name = "w25q128fv"

    total_size  =   16777216   # bytes
    page_size   =        256   # bytes
    total_pages =      65536

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class W25Q128FW(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.WINBOND
    device_id = 0x6018
    name = "w25q128fw"

    total_size  =   16777216   # bytes
    page_size   =        256   # bytes
    total_pages =      65536

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
        SpiNorFlashOpCodes.READ_1_1_2,
        SpiNorFlashOpCodes.PP_1_1_2,
        SpiNorFlashOpCodes.READ_1_1_4,
        SpiNorFlashOpCodes.PP_1_1_4,
    ]
    dummy_bits = 8


class W25Q128JV(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.WINBOND
    device_id = 0x7018
    name = "w25q128jv"

    total_size  =   16777216   # bytes
    page_size   =        256   # bytes
    total_pages =      65536

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
        SpiNorFlashOpCodes.READ_1_1_2,
        SpiNorFlashOpCodes.PP_1_1_2,
        SpiNorFlashOpCodes.READ_1_1_4,
        SpiNorFlashOpCodes.PP_1_1_4,
    ]
    dummy_bits = 8


class W25Q16DW(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.WINBOND
    device_id = 0x6015
    name = "w25q16dw"

    total_size  =    2097152   # bytes
    page_size   =        256   # bytes
    total_pages =       8192

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
        SpiNorFlashOpCodes.READ_1_1_2,
        SpiNorFlashOpCodes.PP_1_1_2,
        SpiNorFlashOpCodes.READ_1_1_4,
        SpiNorFlashOpCodes.PP_1_1_4,
    ]
    dummy_bits = 8


class W25Q16JV(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.WINBOND
    device_id = 0x4015
    name = "w25q16jv"

    total_size  =    2097152   # bytes
    page_size   =        256   # bytes
    total_pages =       8192

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class W25Q16JV_IM(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.WINBOND
    device_id = 0x7015
    name = "w25q16jv-im"

    total_size  =    2097152   # bytes
    page_size   =        256   # bytes
    total_pages =       8192

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
        SpiNorFlashOpCodes.READ_1_1_2,
        SpiNorFlashOpCodes.PP_1_1_2,
        SpiNorFlashOpCodes.READ_1_1_4,
        SpiNorFlashOpCodes.PP_1_1_4,
    ]
    dummy_bits = 8


class W25Q16JV_JM(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.WINBOND
    device_id = 0x7015
    name = "w25q16jv-jm"

    total_size  =    2097152   # bytes
    page_size   =        256   # bytes
    total_pages =       8192

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
        SpiNorFlashOpCodes.READ_1_1_2,
        SpiNorFlashOpCodes.PP_1_1_2,
        SpiNorFlashOpCodes.READ_1_1_4,
        SpiNorFlashOpCodes.PP_1_1_4,
    ]
    dummy_bits = 8


class W25Q20BW(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.WINBOND
    device_id = 0x5012
    name = "w25q20bw"

    total_size  =     262144   # bytes
    page_size   =        256   # bytes
    total_pages =       1024

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
    ]
    dummy_bits = 8


class W25Q20CL(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.WINBOND
    device_id = 0x4012
    name = "w25q20cl"

    total_size  =     262144   # bytes
    page_size   =        256   # bytes
    total_pages =       1024

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
    ]
    dummy_bits = 8


class W25Q20EW(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.WINBOND
    device_id = 0x6012
    name = "w25q20ew"

    total_size  =     262144   # bytes
    page_size   =        256   # bytes
    total_pages =       1024

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
    ]
    dummy_bits = 8


class W25Q256(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.WINBOND
    device_id = 0x4019
    name = "w25q256"

    total_size  =   33554432   # bytes
    page_size   =        256   # bytes
    total_pages =     131072

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
        SpiNorFlashOpCodes.READ_1_1_2,
        SpiNorFlashOpCodes.PP_1_1_2,
        SpiNorFlashOpCodes.READ_1_1_4,
        SpiNorFlashOpCodes.PP_1_1_4,
        SpiNorFlashOpCodes.READ_1_1_1_4B,
        SpiNorFlashOpCodes.PP_1_1_1_4B,
        SpiNorFlashOpCodes.READ_1_1_1_FAST_4B,
        SpiNorFlashOpCodes.READ_1_1_2_4B,
        SpiNorFlashOpCodes.READ_1_1_4_4B,
        SpiNorFlashOpCodes.PP_1_1_4_4B,
    ]
    dummy_bits = 8


class W25Q256FV(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.WINBOND
    device_id = 0x4019
    name = "w25q256fv"

    total_size  =   33554432   # bytes
    page_size   =        256   # bytes
    total_pages =     131072

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class W25Q256JV(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.WINBOND
    device_id = 0x4019
    name = "w25q256jv"

    total_size  =   33554432   # bytes
    page_size   =        256   # bytes
    total_pages =     131072

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class W25Q256JVM(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.WINBOND
    device_id = 0x7019
    name = "w25q256jvm"

    total_size  =   33554432   # bytes
    page_size   =        256   # bytes
    total_pages =     131072

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
        SpiNorFlashOpCodes.READ_1_1_2,
        SpiNorFlashOpCodes.PP_1_1_2,
        SpiNorFlashOpCodes.READ_1_1_4,
        SpiNorFlashOpCodes.PP_1_1_4,
    ]
    dummy_bits = 8


class W25Q256JW(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.WINBOND
    device_id = 0x6019
    name = "w25q256jw"

    total_size  =   33554432   # bytes
    page_size   =        256   # bytes
    total_pages =     131072

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
        SpiNorFlashOpCodes.READ_1_1_2,
        SpiNorFlashOpCodes.PP_1_1_2,
        SpiNorFlashOpCodes.READ_1_1_4,
        SpiNorFlashOpCodes.PP_1_1_4,
    ]
    dummy_bits = 8


class W25Q32(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.WINBOND
    device_id = 0x4016
    name = "w25q32"

    total_size  =    4194304   # bytes
    page_size   =        256   # bytes
    total_pages =      16384

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
    ]
    dummy_bits = 8


class W25Q32DW(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.WINBOND
    device_id = 0x6016
    name = "w25q32dw"

    total_size  =    4194304   # bytes
    page_size   =        256   # bytes
    total_pages =      16384

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
        SpiNorFlashOpCodes.READ_1_1_2,
        SpiNorFlashOpCodes.PP_1_1_2,
        SpiNorFlashOpCodes.READ_1_1_4,
        SpiNorFlashOpCodes.PP_1_1_4,
    ]
    dummy_bits = 8


class W25Q32FV(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.WINBOND
    device_id = 0x4016
    name = "w25q32fv"

    total_size  =    4194304   # bytes
    page_size   =        256   # bytes
    total_pages =      16384

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class W25Q32JV(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.WINBOND
    device_id = 0x7016
    name = "w25q32jv"

    total_size  =    4194304   # bytes
    page_size   =        256   # bytes
    total_pages =      16384

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
        SpiNorFlashOpCodes.READ_1_1_2,
        SpiNorFlashOpCodes.PP_1_1_2,
        SpiNorFlashOpCodes.READ_1_1_4,
        SpiNorFlashOpCodes.PP_1_1_4,
    ]
    dummy_bits = 8


class W25Q32JWM(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.WINBOND
    device_id = 0x8016
    name = "w25q32jwm"

    total_size  =    4194304   # bytes
    page_size   =        256   # bytes
    total_pages =      16384

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
        SpiNorFlashOpCodes.READ_1_1_2,
        SpiNorFlashOpCodes.PP_1_1_2,
        SpiNorFlashOpCodes.READ_1_1_4,
        SpiNorFlashOpCodes.PP_1_1_4,
    ]
    dummy_bits = 8


class W25Q64(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.WINBOND
    device_id = 0x4017
    name = "w25q64"

    total_size  =    8388608   # bytes
    page_size   =        256   # bytes
    total_pages =      32768

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
    ]
    dummy_bits = 8


class W25Q64DW(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.WINBOND
    device_id = 0x6017
    name = "w25q64dw"

    total_size  =    8388608   # bytes
    page_size   =        256   # bytes
    total_pages =      32768

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
        SpiNorFlashOpCodes.READ_1_1_2,
        SpiNorFlashOpCodes.PP_1_1_2,
        SpiNorFlashOpCodes.READ_1_1_4,
        SpiNorFlashOpCodes.PP_1_1_4,
    ]
    dummy_bits = 8


class W25Q64FV(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.WINBOND
    device_id = 0x4017
    name = "w25q64fv"

    total_size  =    8388608   # bytes
    page_size   =        256   # bytes
    total_pages =      32768

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class W25Q64JV(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.WINBOND
    device_id = 0x4017
    name = "w25q64jv"

    total_size  =    8388608   # bytes
    page_size   =        256   # bytes
    total_pages =      32768

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_2,
        SpiNorFlashOpCodes.PP_1_1_2,
        SpiNorFlashOpCodes.READ_1_1_4,
        SpiNorFlashOpCodes.PP_1_1_4,
    ]
    dummy_bits = 8


class W25Q80(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.WINBOND
    device_id = 0x5014
    name = "w25q80"

    total_size  =    1048576   # bytes
    page_size   =        256   # bytes
    total_pages =       4096

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
    ]
    dummy_bits = 8


class W25Q80BL(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.WINBOND
    device_id = 0x4014
    name = "w25q80bl"

    total_size  =    1048576   # bytes
    page_size   =        256   # bytes
    total_pages =       4096

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
    ]
    dummy_bits = 8


class W25Q80BV(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.WINBOND
    device_id = 0x4014
    name = "w25q80bv"

    total_size  =    1048576   # bytes
    page_size   =        256   # bytes
    total_pages =       4096

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class W25X05(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.WINBOND
    device_id = 0x3010
    name = "w25x05"

    total_size  =      65536   # bytes
    page_size   =        256   # bytes
    total_pages =        256

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
    ]
    dummy_bits = 8


class W25X10(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.WINBOND
    device_id = 0x3011
    name = "w25x10"

    total_size  =     131072   # bytes
    page_size   =        256   # bytes
    total_pages =        512

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
    ]
    dummy_bits = 8


class W25X16(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.WINBOND
    device_id = 0x3015
    name = "w25x16"

    total_size  =    2097152   # bytes
    page_size   =        256   # bytes
    total_pages =       8192

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
    ]
    dummy_bits = 8


class W25X20(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.WINBOND
    device_id = 0x3012
    name = "w25x20"

    total_size  =     262144   # bytes
    page_size   =        256   # bytes
    total_pages =       1024

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
    ]
    dummy_bits = 8


class W25X32(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.WINBOND
    device_id = 0x3016
    name = "w25x32"

    total_size  =    4194304   # bytes
    page_size   =        256   # bytes
    total_pages =      16384

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
    ]
    dummy_bits = 8


class W25X40(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.WINBOND
    device_id = 0x3013
    name = "w25x40"

    total_size  =     524288   # bytes
    page_size   =        256   # bytes
    total_pages =       2048

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
    ]
    dummy_bits = 8


class W25X64(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.WINBOND
    device_id = 0x3017
    name = "w25x64"

    total_size  =    8388608   # bytes
    page_size   =        256   # bytes
    total_pages =      32768

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
    ]
    dummy_bits = 8


class W25X80(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.WINBOND
    device_id = 0x3014
    name = "w25x80"

    total_size  =    1048576   # bytes
    page_size   =        256   # bytes
    total_pages =       4096

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
    ]
    dummy_bits = 8


class ZD25D20(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.THOMSON
    device_id = 0x2012
    name = "zd25d20"

    total_size  =     262144   # bytes
    page_size   =        256   # bytes
    total_pages =       1024

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


class ZD25D40(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.THOMSON
    device_id = 0x2013
    name = "zd25d40"

    total_size  =     524288   # bytes
    page_size   =        256   # bytes
    total_pages =       2048

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits = 8


