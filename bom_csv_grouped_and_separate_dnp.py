#
# Example python script to generate a BOM from a KiCad generic netlist
#
# Example: Ungrouped (One component per row) CSV output
#

"""
    @package
    Generate a csv list file.
    Components are sorted by ref
    One component per line
    Fields are (if exist)
    Ref, displayed value, manufacturer, partnumber, mouser, digikey temperature range, replacement, footprint, datasheet

    Command line:
    python "pathToFile/bom_csv_sorted_by_ref.py" "%I" "%O.csv"
"""

import sys
from kicad_bom_writer import make_bom


xml_fn = sys.argv[1]
output_fn = sys.argv[2]
try:
    make_bom(xml_fn, output_fn + " flat BOM.csv", grouped=False,
             columns_dict={
                 'ref': 'Ref',
                 'manufacturer': 'Manufacturer',
                 'part_num': 'Manufacturer part number',
                 'mouser': 'Mouser',
                 'digikey': 'Digikey',
                 'farnell': 'Farnell',
                 'footprint': 'Footprint',
                 'description': 'Description',
             },
             exclude_filters=['virtual', 'dnp'], delimiter=',')
    make_bom(xml_fn, output_fn + " grouped BOM.csv", grouped=True,
             columns_dict={
                 'ref': 'Ref',
                 'qty': 'Qty',
                 'manufacturer': 'Manufacturer',
                 'part_num': 'Manufacturer part number',
                 'mouser': 'Mouser',
                 'digikey': 'Digikey',
                 'farnell': 'Farnell',
                 'footprint': 'Footprint',
                 'description': 'Description',
             },
             exclude_filters=['virtual', 'dnp'], delimiter=',')
    make_bom(xml_fn, output_fn + " not installed.csv", grouped=False,
             columns_dict={
                 'ref': 'Ref.Des.',
                 'dnp': 'DNP',
                 'virtual': 'virtual',
                 'part_num': 'Manufacturer part number',
                 'description': 'Description',
                 'manufacturer': 'Manufacturer',
                 'mouser': 'Mouser',
                 'digikey': 'Digikey',
                 'farnell': 'Farnell',
                 'footprint': 'Footprint',
             },
             exclude_filters=['virtual'], include_filters=['dnp'])
except Exception as e:
    print( __file__, ":", e, sys.stderr )
    f = sys.stdout

