# File name: test_reg_exp_parser
# Created on: 12/27/2023
# Created by: Oleg Gordiushenkov

import re

pcb_fn = r"C:\Gordiushenkov\SlopeHelper\Electronics\SH\Units\IntEn\PCBs\power_module_v1_6\Design\power_module_v1_6.kicad_pcb"

with open(pcb_fn, 'r') as file:
    # Read the content of the file
    pcb_content = file.read()


pattern = r'comment 1 "(.*?)"'
match = re.search(pattern, pcb_content)
print(match.group(1))

pattern = r'\(layer "F.Cu" (.*) \(thickness (.*?)\)\)'
match = re.search(pattern, pcb_content)
print(match.group(2))

pattern = r'\(copper_finish "(.*?)"\)'
match = re.search(pattern, pcb_content)
print(match.group(1))


# pattern = r'\(gr_line \(start (-?\d+\.?\d*) (-?\d+\.?\d*)\) \(end (-?\d+\.?\d*) (-?\d+\.?\d*)\).*?\n.*?layer "Edge.Cuts".*?'
# match = re.findall(pattern, pcb_content, re.DOTALL)
# print(len(match))
# print(match)
pattern = re.compile(r'.*?layer "Edge.Cuts".*?')
matches = [(match.group(), line_num + 1) for line_num, line in enumerate(pcb_content.splitlines()) if (match := pattern.search(line))]

if matches:
    pattern = re.compile(r'\(gr_line \(start (-?\d+\.?\d*) (-?\d+\.?\d*)\) \(end (-?\d+\.?\d*) (-?\d+\.?\d*)\).*?')
    byline = pcb_content.splitlines()
    for _, line_num in matches:
        match = re.search(pattern, byline[line_num - 2])
        print(match)
        vals = []
        for i in range (1,5):
            vals.append(int(match.group(i)))
        print(vals)
        print(byline[line_num - 2])


if matches:
    print("Matches found:")
    for match, line_num in matches:
        print(f"Line {line_num}: {match}")
else:
    print("No matches found.")