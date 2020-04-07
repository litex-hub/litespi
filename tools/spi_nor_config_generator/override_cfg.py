# Some features could be not mentioned in modules we parse from.
# In case there is a chip which supports a feature but it was not
# mentioned, we can override config here.

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
# }

override_chip_cfg = {
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
        'is25wp512m' :  {
            'dual_support' : True,
            'quad_support' : True,
        },
}
