#
# This file is part of LiteSPI
#
# Copyright (c) 2020 Antmicro <www.antmicro.com>
# SPDX-License-Identifier: BSD-2-Clause


class MetaSizes(type):
    """Meta Sizes

    The ``MetaSizes`` class makes sure that all provided size parameters
    in chip are consistent which are:
        * total size
        * size per unit
        * number of units
    """

    def _table(self, mod_name, name):
        size_name  = "{}_size".format(name)
        total_name = "total_{}s".format(name)
        ts_name    = "total_size"

        provided_size_per_unit   = getattr(self, "provided_"+size_name)
        provided_number_of_units = getattr(self, "provided_"+total_name)
        provided_total_size      = getattr(self, "provided_total_size")

        size_per_unit   = getattr(self, size_name)
        number_of_units = getattr(self, total_name)
        total_size = self.total_size

        calc_size_per_unit   = int(total_size / number_of_units)
        calc_number_of_units = int(total_size / size_per_unit)
        calc_total_size      = int(size_per_unit * number_of_units)

        def check(a, b):
            if a is not None and a != b:
                return '!='
            return '=='

        def si(a, f=str):
            if a is None:
                return ''
            else:
                return f(int(a))

        return """
| {mod_name:14s}                 |     Provided == Calculated   |     Hex    |
|-----------------|--------------|------------------------------|------------|
|   size_per_unit | {size_name_:>12s} | {p_size_:>12s} {size__check} {c_size_:<12s} | {h_size_:>10s} | {p_tsize:>10s} / {p_units:10s} ({ts_name___:>10s} / {total_name:10s})
| number_of_units | {total_name:>12s} | {p_units:>12s} {units_check} {c_units:<12s} | {h_units:>10s} | {p_tsize:>10s} / {p_size_:10s} ({ts_name___:>10s} / {size_name_:10s})
|      total_size | {ts_name___:>12s} | {p_tsize:>12s} {tsize_check} {c_tsize:<12s} | {h_tsize:>10s} | {p_size_:>10s} * {p_units:10s} ({size_name_:>10s} * {ts_name___:10s})
""".format(
    mod_name = mod_name,
    name = name,
    size_name_ = size_name,
    total_name = total_name,
    ts_name___ = ts_name,
    size__check = check(provided_size_per_unit,   calc_size_per_unit  ),
    units_check = check(provided_number_of_units, calc_number_of_units),
    tsize_check = check(provided_total_size,      calc_total_size     ),
    p_size_ = si(provided_size_per_unit),
    p_units = si(provided_number_of_units),
    p_tsize = si(provided_total_size),
    c_size_ = si(calc_size_per_unit),
    c_units = si(calc_number_of_units),
    c_tsize = si(calc_total_size),
    h_size_ = si(calc_size_per_unit, hex),
    h_units = si(calc_number_of_units, hex),
    h_tsize = si(calc_total_size, hex),
)

    def _fix_and_check_sized(self, mod_name, name):
        """Makes sure that XXX_size, XXX_total and total_size match.
        IE If XXX == pages then, page_size * total_pages == total_size
        """
        size_name  = "{}_size".format(name)
        total_name = "total_{}s".format(name)

        provided_size_per_unit   = getattr(self, size_name,    None)
        provided_number_of_units = getattr(self, total_name,   None)
        provided_total_size      = getattr(self, "total_size", None)
        setattr(self, "provided_"+size_name,   provided_size_per_unit)
        setattr(self, "provided_"+total_name,  provided_number_of_units)

        provided = 0
        if provided_size_per_unit is not None:
            provided += 1
        if provided_number_of_units is not None:
            provided += 1
        if provided_total_size is not None:
            provided += 1

        assert provided >= 2, """\
{mod_name}: Must provide two of {name}_size={} (size_per_unit), total_{name}s={} (number_of_units), total_size={}
""".format(provided_size_per_unit, provided_number_of_units, provided_total_size, mod_name=mod_name, name=name)

        if provided_size_per_unit is None:
            size_per_unit = int(provided_total_size / provided_number_of_units)
        else:
            size_per_unit = int(provided_size_per_unit)

        if provided_number_of_units is None:
            number_of_units = int(provided_total_size / provided_size_per_unit)
        else:
            number_of_units = int(provided_number_of_units)

        if provided_total_size is None:
            total_size = int(provided_size_per_unit * provided_number_of_units)
        else:
            total_size = int(provided_total_size)

        setattr(self, size_name,  size_per_unit)
        setattr(self, total_name, number_of_units)

        assert   size_per_unit ==    total_size / number_of_units, self._table(mod_name, name)
        assert number_of_units ==    total_size / size_per_unit,   self._table(mod_name, name)
        assert      total_size == size_per_unit * number_of_units, self._table(mod_name, name)
        if provided_total_size is not None:
            assert provided_total_size == total_size, """\
{mod_name}: Tried to set size to {} but size was already set to {}
""".format(provided_total_size, self.total_size, mod_name=mod_name)

    def __init__(self, name, *args, **kw):
        if name == "SpiNorFlashModule":
           return
        setattr(self, "provided_total_size", getattr(self, "total_size", None))
        self._fix_and_check_sized(name, "page")
        #self._fix_and_check_sized(name, "sector")
        self.total_size = self.page_size * self.total_pages
        self.table = lambda x: self._table(name, x)

