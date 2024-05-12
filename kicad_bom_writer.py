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
    'footprint': 'getFootprint',
    'libname': 'getLibName',
    'partname': 'getPartName',
}

def component_eq(self, other):
    if hasattr(self, 'part_num') and hasattr(other, 'part_num'):
        return not self.getField('part_num') != other.getField('part_num') \
        and not self.getPartName() != other.getPartName()
    else:
        return not self.getPartName() != other.getPartName()


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
            fields = [x.lower() for x in comp.getFieldNames()]
            if p in fields:
                val = comp.getField(p)
                if val == '':
                    val = '+'
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


def component_to_skip(component, include_filters = None, exclude_filters=None):
    if exclude_filters is None:
        exclude_filters = []
    field_names = component.getFieldNames()
    if include_filters is None:
        filter = [f.lower() for f in field_names]
    else:
        filter = [f.lower() for f in include_filters]
    skip = False
    include = False
    # For the case if no attributes are set
    if not field_names:
        include = True

    for n in field_names:
        lowercase = str(n).lower()
        if lowercase in exclude_filters:
            skip = True
        if lowercase in filter:
            include = True
    # print(f'Skip: {skip}, include: {include}, component: {component.getRef()}')
    # if not include:
    #     print(f'{field_names}')
    return skip or not include


def write_grouped_bom(writer, net, columns_dict, include_filters = None, exclude_filters=None, obligatory=None):
    msg = ''
    groups = net.groupComponents()
    for group in groups:
        qty = 0
        props = {}

        for component in group:
            if not component_to_skip(component, include_filters, exclude_filters):
                if obligatory is not None:
                    for o in obligatory:
                        if o not in p.keys() or not p[o]:
                            msg += f'Component {component.getRef()} does not have property "{o}"\n'
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
    return msg

def write_flat_bom(writer, net, columns_dict, include_filters = None, exclude_filters=None, obligatory=None):
    msg = ''
    components = net.getInterestingComponents()
    for c in components:
        if not component_to_skip(c, include_filters, exclude_filters):
            p = get_properties(c, columns_dict)
            p = convert_dict_vals_to_lists(p)
            if obligatory is not None:
                for o in obligatory:
                    if o not in p.keys() or not p[o]:
                        msg += f'Component {c.getRef()} does not have property "{o}"\n'
            writerow(writer, get_props_list(p, columns_dict))
    return msg


def make_bom(xml_fn, filename, grouped=True, columns_dict=None, include_filters = None, exclude_filters=None, delimiter=';', obligatory=None):
    '''

    :param xml_fn: input xml filename
    :param filename: output filename
    :param grouped: True if components should be grouped
    :param columns_dict: dictionary with columns in format property: title
    :return: report as a string
    '''
    msg = ''
    try:
        net = kicad_netlist_reader.netlist(xml_fn)
        with open(filename, 'w') as csv_file:
            writer = csv.writer(csv_file, lineterminator='\n', delimiter=delimiter, quotechar="\"", quoting=csv.QUOTE_ALL)
            writerow(writer, columns_dict.values())
            if grouped:
                msg += write_grouped_bom(writer, net, columns_dict, include_filters, exclude_filters, obligatory)
            else:
                msg += write_flat_bom(writer, net, columns_dict, include_filters, exclude_filters, obligatory)


    except IOError:
        e = "Can't open output file for writing: " + filename
        print(__file__, ":", e, sys.stderr)
        msg += sys.stdout
    return msg

def make_bom_default(xml_fn, output_fn):
    msg = ''
    msg += make_bom(xml_fn, str(output_fn) + " flat BOM.csv", grouped=False,
             columns_dict={
                 'ref': 'Ref.Des.',
                 'part_num': 'Manufacturer part number',
                 'description': 'Description',
                 'manufacturer': 'Manufacturer',
                 'mouser': 'Mouser',
                 'digikey': 'Digikey',
                 'farnell': 'Farnell',
                 'footprint': 'Footprint'
             },
             exclude_filters=['dnp', 'virtual'],
             obligatory=['part_num'])
    msg += make_bom(xml_fn, str(output_fn) + " grouped BOM.csv", grouped=True,
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
             },
             exclude_filters=['dnp', 'virtual'])
    msg += make_bom(xml_fn, str(output_fn) + " not installed.csv", grouped=False,
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
    return msg

if __name__ == '__main__':
    xml_fn = 'temp.xml'
    output_fn = 'test'
    make_bom_default(xml_fn, output_fn)
