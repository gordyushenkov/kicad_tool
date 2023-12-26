# File name: kicad_sch_tools
# Created on: 12/26/2023
# Created by: Oleg Gordiushenkov

from pathlib import Path
import subprocess
import sys

def kicad_sch_export_bom(kicad_cli_path, sch_fn, output_folder, bom_scripts):
    path_obj = Path(output_folder)
    xml_fn = r'temp.xml'
    bom_fn = path_obj/sch_fn.stem

    commands = [f'"{kicad_cli_path}"' + " sch export python-bom " + str(sch_fn) + ' -o ' + xml_fn]

    python_executable = sys.executable
    for bs in bom_scripts:
        commands.append([python_executable, bs] + [xml_fn, str(bom_fn)])

    return commands

def kicad_sch_export_pdf(kicad_cli_path, sch_fn, output_folder):
    path_obj = Path(output_folder)
    pdf_fn = path_obj/(sch_fn.stem + ' sch')
    pdf_fn = pdf_fn.with_suffix('.pdf')

    commands = [f'"{kicad_cli_path}"' + " sch export pdf " + str(sch_fn) + ' -o ' + f'"{str(pdf_fn)}"']

    return commands
