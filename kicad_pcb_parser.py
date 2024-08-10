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
    # pattern = r'\(layer "F.Cu"(.*)\(thickness (.*?)\)\)'
    pattern = r'\(\s*layer\s+"F\.Cu"\s*\(\s*type\s+"copper"\s*\)\s*\(\s*thickness\s+(.*?)\s*\)\s*\)'
    match = re.search(pattern, pcb_content)
    if match:
        val = float(match.group(1))
    # else:
    #     # For KiCAD 8 format
    #     pattern = r'\(layer "F.Cu" (.*) \(thickness (.*?)\)\)'
    #     match = re.search(pattern, pcb_content)
    #     if match:
    #         val = float(match.group(2))

    return val

def get_core_material(pcb_content):
    val = ''
    pattern = r'\(layer "dielectric 1" (.*) \(material "(.*?)"\).*?\)'
    pattern = r'\(\s*layer\s+"dielectric 1"\s*\(\s*type\s+"core"\s*\)\s*\(\s*thickness\s+(.*)\s*\)\s*\(\s*material\s+"(.*?)"\s*\)'
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
    pattern_line = r'\(gr_line\s*\(\s*start\s+(-?\d+\.?\d*)\s+(-?\d+\.?\d*)\s*\)\s*\(\s*end\s+(-?\d+\.?\d*)\s+(-?\d+\.?\d*)\s*\)\s*\(\s*stroke\s*\(\s*width\s+\d+(?:\.\d+)?\s*\)\s*\(\s*type\s+\w+\s*\)\s*\)\s*\(\s*layer\s+"Edge\.Cuts"\s*\)'
    matches_line = re.findall(pattern_line, pcb_content)
    pattern_arc = r'\(gr_arc\s*\(\s*start\s+(-?\d+\.?\d*)\s+(-?\d+\.?\d*)\s*\)\s+\(\s*mid\s+(?:-?\d+\.?\d*)\s+(?:-?\d+\.?\d*)\s*\)\s+\(\s*end\s+(-?\d+\.?\d*)\s+(-?\d+\.?\d*)\s*\)\s+\(\s*stroke\s*\(\s*width\s+\d+(?:\.\d+)?\s*\)\s*\(\s*type\s+\w+\s*\)\s*\)\s*\(\s*layer\s+"Edge\.Cuts"\s*\)'
    matches_arc = re.findall(pattern_arc, pcb_content)
    matches = matches_line + matches_arc
    if matches:
        x_list = []
        y_list = []
        for match in matches:
            for i in [0, 2]:
                x_list.append(float(match[i]))
            for i in [1, 3]:
                y_list.append(float(match[i]))
        if x_list:
            dims[0] = max(x_list) - min(x_list)
        if y_list:
            dims[1] = max(y_list) - min(y_list)
    # pattern = re.compile(r'.*?layer "Edge.Cuts".*?')
    # matches = [(match.group(), line_num + 1) for line_num, line in enumerate(pcb_content.splitlines()) if
    #            (match := pattern.search(line))]
    # print(matches)
    # if matches:
    #     pattern = re.compile(r'\(gr_line \(start (-?\d+\.?\d*) (-?\d+\.?\d*)\) \(end (-?\d+\.?\d*) (-?\d+\.?\d*)\).*?')
    #     byline = pcb_content.splitlines()
    #     x_list = []
    #     y_list = []
    #     for _, line_num in matches:
    #         match = re.search(pattern, byline[line_num - 2])
    #         if match:
    #             for i in [1, 3]:
    #                 x_list.append(float(match.group(i)))
    #             for i in [2, 4]:
    #                 y_list.append(float(match.group(i)))
    #     if x_list:
    #         dims[0] = max(x_list) - min(x_list)
    #     if y_list:
    #         dims[1] = max(y_list) - min(y_list)
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
    pcb_fn = r"C:\Gordiushenkov\Electronics\Units\Radar\PCBs\rad_commutation_v1_0\Design\rad_commutation_v1_0.kicad_pcb"
    # pcb_fn = r"C:\Gordiushenkov\Electronics\Units\Picker controller\PCBs\pk_drv_5kw_pwr_v1_0\Design\pk_drv_5kw_pwr_v1_0.kicad_pcb"
    pcb_rep = kicad_pcb_parse(pcb_fn)
    print(pcb_rep)