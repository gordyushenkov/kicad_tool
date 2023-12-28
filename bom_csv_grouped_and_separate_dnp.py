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

from __future__ import print_function

# Import the KiCad python helper module
import kicad_netlist_reader
import csv
import sys

def myEqu(self, other):
    """myEqu is a more advanced equivalence function for components which is
    used by component grouping. Normal operation is to group components based
    on their Value and Footprint.

    In this example of a more advanced equivalency operator we also compare the
    custom fields Voltage, Tolerance and Manufacturer as well as the assigned
    footprint. If these fields are not used in some parts they will simply be
    ignored (they will match as both will be empty strings).

    """
    result = True
    if self.getDescription() != other.getDescription():
        result = False

    return result

kicad_netlist_reader.comp.__eq__ = myEqu

# Generate an instance of a generic netlist, and load the netlist tree from
# the command line option. If the file doesn't exist, execution will stop
net = kicad_netlist_reader.netlist(sys.argv[1])

# Open a file to write to, if the file cannot be opened output to stdout
# instead
try:
    f = open( sys.argv[2] + " grouped BOM.csv", 'w')
except IOError:
    e = "Can't open output file for writing: " + sys.argv[2]
    print( __file__, ":", e, sys.stderr )
    f = sys.stdout

# Create a new csv writer object to use as the output formatter
out = csv.writer(f, lineterminator='\n', delimiter=';', quotechar="\"", quoting=csv.QUOTE_ALL)

# override csv.writer's writerow() to support utf8 encoding:
def writerow( acsvwriter, columns ):
    utf8row = []
    for col in columns:
        utf8row.append( str(col) )
    acsvwriter.writerow( utf8row )

components = net.getInterestingComponents()

# Output a field delimited header line
#writerow( out, ['Source:', net.getSource()] )
#writerow( out, ['Date:', net.getDate()] )
#writerow( out, ['Tool:', net.getTool()] )
#writerow( out, ['Component Count:', len(components)] )
writerow( out, ['Manufacturer part number', 
    'Description',
    'Ref', 'Qty', 'Manufacturer',
    'Mouser', 'Digikey', 'Farnell'
    'Footprint'] )

# Get all of the components in groups of matching parts + values
# (see ky_generic_netlist_reader.py)
grouped = net.groupComponents()

# Output all of the component information (One component per row)
for group in grouped:
    refs = ""

    # Add the reference of every component in the group and keep a reference
    # to the component so that the other data can be filled in once per group
    c = None
    n_parts = 0
    for component in group:
        if not component.getField("dnp") and not component.getField("DNP") and not component.getField("virtual"):
            refs += component.getRef() + " "
            c = component
            n_parts += 1
    
    
    
    # Fill in the component groups common data
    if c is not None:
        writerow( out, [c.getField("part_num"), c.getDescription(), 
            refs, n_parts, c.getField("manufacturer"), 
            c.getField("mouser"), c.getField("digikey"), c.getField("farnell"),
            c.getFootprint()])

