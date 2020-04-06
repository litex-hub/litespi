from litespi.spi_nor_features import SpiNorFeatures as Config

# Some features could be not mentioned in modules we parse from.
# In case there is a chip which supports a feature but it was not
# mentioned, we can override config here.
override_chip_cfg = {
        'mx25lm51245' : {
            'supported_modes' : Config.FEATURE_SINGLE
                                | Config.FEATURE_OCTAL
                                | Config.FEATURE_ADDR_WIDTH_1,
        },
        'mx25r512f' : {
            'supported_modes' : Config.FEATURE_SINGLE
                                | Config.FEATURE_DUAL
                                | Config.FEATURE_QPI
                                | Config.FEATURE_ADDR_WIDTH_1,
        },
        'mx25r1035f' :  {
            'supported_modes' : Config.FEATURE_SINGLE
                                | Config.FEATURE_DUAL
                                | Config.FEATURE_QPI
                                | Config.FEATURE_ADDR_WIDTH_1,
        },
        'mx25r2035f' :  {
            'supported_modes' : Config.FEATURE_SINGLE
                                | Config.FEATURE_DUAL
                                | Config.FEATURE_QPI
                                | Config.FEATURE_ADDR_WIDTH_1,
        },
        'mx25r4035f' :  {
            'supported_modes' : Config.FEATURE_SINGLE
                                | Config.FEATURE_DUAL
                                | Config.FEATURE_QPI
                                | Config.FEATURE_ADDR_WIDTH_1,
        },
        'mx25r8035f' :  {
            'supported_modes' : Config.FEATURE_SINGLE
                                | Config.FEATURE_DUAL
                                | Config.FEATURE_QPI
                                | Config.FEATURE_ADDR_WIDTH_1,
        },
        'mx25r1635f' :  {
            'supported_modes' : Config.FEATURE_SINGLE
                                | Config.FEATURE_DUAL
                                | Config.FEATURE_QPI
                                | Config.FEATURE_ADDR_WIDTH_1,
        },
        'w25q64jv' :  {
            'supported_modes' : Config.FEATURE_SINGLE
                                | Config.FEATURE_DUAL
                                | Config.FEATURE_QPI
                                | Config.FEATURE_ADDR_WIDTH_1,
        },
        'gd25q512mc' :  {
            'supported_modes' : Config.FEATURE_SINGLE
                                | Config.FEATURE_DUAL
                                | Config.FEATURE_QPI
                                | Config.FEATURE_ADDR_WIDTH_1,
        },
        'is25lp512m' :  {
            'supported_modes' : Config.FEATURE_SINGLE
                                | Config.FEATURE_DUAL
                                | Config.FEATURE_QPI
                                | Config.FEATURE_ADDR_WIDTH_1,
        },
        'is25wp512m' :  {
            'supported_modes' : Config.FEATURE_SINGLE
                                | Config.FEATURE_DUAL
                                | Config.FEATURE_QPI
                                | Config.FEATURE_ADDR_WIDTH_1,
        },
}
