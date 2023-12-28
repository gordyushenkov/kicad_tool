# File name: kicad_bom_writer.py
# Created on: 12/28/2023
# Created by: Oleg Gordiushenkov

import kicad_netlist_reader
import csv
import sys
import re

METHODS = {
    'ref': 'getRef',
    'description': 'getDescription',
    'footprint': 'getFootprint'
}

def component_eq(self, other):
    if hasattr(self, 'part_num') and hasattr(other, 'part_num'):
        return not self.getField('part_num') != other.getField('part_num')
    else:
        return not self.getDescription() != other.getDescription()


kicad_netlist_reader.comp.__eq__ = component_eq

def writerow(acsvwriter, columns):
    utf8row = []
    for col in columns:
        utf8row.append( str(col) )
    acsvwriter.writerow( utf8row )

def get_properties(comp, properties):
    result_dict = {}
    for p in properties:
        if p == "qty" or p == "Qty":
            continue
        elif p in METHODS.keys():
            func = getattr(comp, METHODS[p], None)
            if func is not None:
                val = func()
                result_dict[p] = val
        else:
            val = comp.getField(p)
            result_dict[p] = val
    return result_dict

def get_props_list(prop_dict, properties):
    row = []
    for p in properties.keys():
        if p in prop_dict:
            row.append(' '.join(prop_dict[p]))
        else:
            row.append('')
    return row

def merge_dicts(dict1, dict2):
    for k in dict2.keys():
        if k not in dict1.keys():
            dict1[k] = dict2[k]
        else:
            dict1[k] = list(set(dict1[k]).union(set(dict2[k])))

    return dict1

def convert_dict_vals_to_lists(dict1):
    return {k:[v] for k,v in dict1.items()}

def custom_sort_key(value):
    # Use regular expression to split the value into non-digits and digits parts
    parts = re.split(r'(\d+)', value)
    # Convert the digits part to an integer for sorting
    return (parts[0], int(parts[1]))

def write_grouped_bom(writer, net, columns_dict):
    groups = net.groupComponents()
    for group in groups:
        qty = 0
        props = {}
        for component in group:
            if not component.getField("dnp") and not component.getField("DNP") and not component.getField("virtual"):
                p = get_properties(component, columns_dict)
                p = convert_dict_vals_to_lists(p)
                if not props:
                    props = p
                else:
                    props = merge_dicts(props, p)
                qty += 1
        # To provide explicit sorting
        if qty > 0:
            props['ref'] = sorted(props['ref'], key=custom_sort_key)
            props['qty'] = [str(qty)]
            writerow(writer, get_props_list(props, columns_dict))

def write_flat_bom(writer, net, columns_dict):
    components = net.getInterestingComponents()
    for c in components:
        if not c.getField("dnp") and not c.getField("DNP") and not c.getField("virtual"):
            p = get_properties(c, columns_dict)
            p = convert_dict_vals_to_lists(p)
            writerow(writer, get_props_list(p, columns_dict))


def make_bom(xml_fn, filename, grouped=True, columns_dict=None):
    '''

    :param xml_fn: input xml filename
    :param filename: output filename
    :param grouped: True if components should be grouped
    :param columns_dict: dictionary with columns in format property: title
    :return: report as a string
    '''
    try:
        net = kicad_netlist_reader.netlist(xml_fn)
        with open(filename, 'w') as csv_file:
            writer = csv.writer(csv_file, lineterminator='\n', delimiter=';', quotechar="\"", quoting=csv.QUOTE_ALL)
            writerow(writer, columns_dict.values())
            if grouped:
                write_grouped_bom(writer, net, columns_dict)
            else:
                write_flat_bom(writer, net, columns_dict)


    except IOError:
        e = "Can't open output file for writing: " + filename
        print(__file__, ":", e, sys.stderr)
        f = sys.stdout


if __name__ == '__main__':
    xml_fn = 'temp.xml'
    output_fn = 'test'
    make_bom(xml_fn, output_fn + " flat BOM.csv", grouped=False,
             columns_dict={
                 'ref': 'Ref.Des.',
                 'part_num': 'Manufacturer part number',
                 'description': 'Description',
                 'manufacturer': 'Manufacturer',
                 'mouser': 'Mouser',
                 'digikey': 'Digikey',
                 'farnell': 'Farnell',
                 'footprint': 'Footprint'
             })
    make_bom(xml_fn, output_fn + " grouped BOM.csv", grouped=True,
             columns_dict={
                 'ref': 'Ref.Des.',
                 'part_num': 'Manufacturer part number',
                 'qty': 'Qty',
                 'description': 'Description',
                 'manufacturer': 'Manufacturer',
                 'mouser': 'Mouser',
                 'digikey': 'Digikey',
                 'farnell': 'Farnell',
                 'footprint': 'Footprint',
                 'dnp': 'DNP',
             })