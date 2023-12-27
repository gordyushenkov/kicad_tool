# File name: kicad_pcb_tools.py
# Created on: 12/26/2023
# Created by: Oleg Gordiushenkov

import subprocess

def kicad_pcb_export_gerber(kicad_cli_path, pcb_fn, output_folder, layers=[]):
    commands = []
    for l in layers:
        commands.append(f'"{kicad_cli_path}"' + " pcb export gerbers " + str(pcb_fn) + ' -o ' + str(output_folder) + \
            ' --layers ' + l + ' --subtract-soldermask --no-x2 --no-protel-ext')
    return commands

def kicad_pcb_export_drill(kicad_cli_path, pcb_fn, output_folder):
    return [f'"{kicad_cli_path}"' + " pcb export drill " + str(pcb_fn) + ' -u mm -o ' + str(output_folder) + \
        '\ --excellon-separate-th']

def kicad_pcb_export_pnp(kicad_cli_path, pcb_fn, output_folder):
    pos_fn = output_folder / pcb_fn.stem
    pos_fn = pos_fn.with_stem(pos_fn.stem + '-all-pos').with_suffix('.csv')
    return [f'"{kicad_cli_path}"' + " pcb export pos " + str(pcb_fn) + ' -o ' + str(pos_fn) + \
        ' --side both --format csv --units mm']

def kicad_pcb_export_3d(kicad_cli_path, pcb_fn, output_folder):
    step_fn = output_folder / pcb_fn.stem
    step_fn = step_fn.with_suffix('.step')
    print(step_fn)
    return [f'"{kicad_cli_path}"' + " pcb export step " + str(pcb_fn) + ' --force -o ' + f'"{str(step_fn)}"']
