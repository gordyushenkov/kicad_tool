# File name: kicad_pcb_parser
# Created on: 12/27/2023
# Created by: Oleg Gordiushenkov

import re


def get_comments(pcb_content):
    comments = {}
    for comment_n in range(1, 11):
        comment_title = f'comment {comment_n}'
        pattern = rf'{comment_title} "(.*?)"'
        match = re.search(pattern, pcb_content)
        if match:
            comments[comment_title] = match.group(1)
    return comments

def get_OL_thickness(pcb_content):
    val = 0
    pattern = r'\(layer "F.Cu" (.*) \(thickness (.*?)\)\)'
    match = re.search(pattern, pcb_content)
    if match:
        val = float(match.group(2))
    return val

def get_core_material(pcb_content):
    val = ''
    pattern = r'\(layer "dielectric 1" (.*) \(material "(.*?)"\).*?\)'
    match = re.search(pattern, pcb_content)
    if match:
        val = match.group(2)
    return val

def get_finishing_layer(pcb_content):
    val = ''
    pattern = r'\(copper_finish "(.*?)"\)'
    match = re.search(pattern, pcb_content)
    if match:
        val = match.group(1)
    return val

def get_dimensions(pcb_content):
    dims = [0, 0]
    pattern = re.compile(r'.*?layer "Edge.Cuts".*?')
    matches = [(match.group(), line_num + 1) for line_num, line in enumerate(pcb_content.splitlines()) if
               (match := pattern.search(line))]

    if matches:
        pattern = re.compile(r'\(gr_line \(start (-?\d+\.?\d*) (-?\d+\.?\d*)\) \(end (-?\d+\.?\d*) (-?\d+\.?\d*)\).*?')
        byline = pcb_content.splitlines()
        x_list = []
        y_list = []
        for _, line_num in matches:
            match = re.search(pattern, byline[line_num - 2])
            if match:
                for i in [1, 3]:
                    x_list.append(float(match.group(i)))
                for i in [2, 4]:
                    y_list.append(float(match.group(i)))
        if x_list:
            dims[0] = max(x_list) - min(x_list)
        if y_list:
            dims[1] = max(y_list) - min(y_list)
    return dims

def kicad_pcb_parse(pcb_fn):
    result = {}
    with open(pcb_fn, 'r') as file:
        # Read the content of the file
        pcb_content = file.read()

    result['comments'] = get_comments(pcb_content)
    result['thicnkess'] = get_OL_thickness(pcb_content)
    result['finishing_layer'] = get_finishing_layer(pcb_content)
    result['dimensions'] = get_dimensions(pcb_content)
    result['material'] = get_core_material(pcb_content)
    return result

if __name__ == '__main__':
    pcb_fn = r"C:\Gordiushenkov\SlopeHelper\Electronics\SH\Units\IntEn\PCBs\power_module_v1_6\Design\power_module_v1_6.kicad_pcb"
    pcb_rep = kicad_pcb_parse(pcb_fn)
    print(pcb_rep)