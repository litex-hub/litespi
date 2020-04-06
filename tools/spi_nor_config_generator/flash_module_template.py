from litespi.spi_nor_features import SpiNorFeatures

def generate_class(vendor_id,
                   device_id,
                   chip_name,
                   total_size,
                   page_size,
                   total_pages,
                   dummy_bits,
                   supported_modes):
    name = chip_name.replace('-', '_').replace('.', 'x')
    # Add 'X' character for chip name starting with digit
    if chip_name[0].isdigit():
        name = 'X' + name

    modes_str = str(supported_modes)
    plain_flags = modes_str[modes_str.find('.') + 1:].split('|')
    modes_builder = '\\\n\t\t'
    for flag in plain_flags:
        modes_builder += ("SpiNorFeatures.%s | \\\n\t\t" %(flag))
    modes_builder = modes_builder[:-6] + '\n'

    genclass = '''class {pn}(SpiNorFlashModule):

    manufacturer_id = {vid}
    device_id = 0x{did:04x}
    name = "{pfn}"

    total_size  = {ts:10d}   # bytes
    page_size   = {ps:10d}   # bytes
    total_pages = {tp:10d}

    supported_modes = {modes}
    dummy_bits = {dbits}


'''.format(
        pn=name.upper(),
        pfn=chip_name,
        vid=vendor_id,
        did=device_id,
        ts=total_size,
        ps=page_size,
        tp=total_pages,
        modes=modes_builder,
        dbits=dummy_bits
    )
    return genclass
