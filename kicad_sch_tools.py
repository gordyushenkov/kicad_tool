# File name: kicad_sch_tools
# Created on: 12/26/2023
# Created by: Oleg Gordiushenkov

from pathlib import Path
import subprocess
import sys

def kicad_sch_export_netlist(kicad_cli_path, sch_fn, output_fn):
    commands = [f'"{kicad_cli_path}"' + " sch export python-bom " + str(sch_fn) + ' -o ' + output_fn]
    return commands

def kicad_sch_export_pdf(kicad_cli_path, sch_fn, output_folder):
    path_obj = Path(output_folder)
    pdf_fn = path_obj/(sch_fn.stem + ' sch')
    pdf_fn = pdf_fn.with_suffix('.pdf')

    commands = [f'"{kicad_cli_path}"' + " sch export pdf " + str(sch_fn) + ' -o ' + f'"{str(pdf_fn)}"']

    return commands


