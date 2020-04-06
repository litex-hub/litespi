from litespi.modules.generated_modules import *
from litespi.modules.modules import *
from litespi.spi_nor_flash_module import MetaSizes

def print_modules():
    for name, obj in globals().items():
        if not issubclass(type(obj), MetaSizes):
            continue
        if name == 'SpiNorFlashModule':
            continue
        if name == 'MetaSizes':
            continue
        print(obj.table("page"))
