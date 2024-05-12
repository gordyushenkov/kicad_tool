# File name: kicad_pcb_tools.py
# Created on: 12/26/2023
# Created by: Oleg Gordiushenkov

def kicad_pcb_export_gerber(kicad_cli_path, pcb_fn, output_folder, layers=[]):
    commands = []
    for l in layers:
        commands.append(f'"{kicad_cli_path}"' + " pcb export gerbers " + f'"{str(pcb_fn)}"' + ' -o ' + f'"{str(output_folder)}"' + \
            ' --layers ' + l + ' --subtract-soldermask --no-x2 --no-protel-ext')
    return commands

def kicad_pcb_export_drill(kicad_cli_path, pcb_fn, output_folder):
    return [f'"{kicad_cli_path}"' + " pcb export drill " + f'"{str(pcb_fn)}"' + ' -u mm -o ' + f'"{str(output_folder)}"' + \
        '\ --excellon-separate-th']

def kicad_pcb_export_pnp(kicad_cli_path, pcb_fn, output_folder):
    pos_fn = output_folder / pcb_fn.stem
    pos_fn = pos_fn.with_stem(pos_fn.stem + '-all-pos').with_suffix('.csv')
    return [f'"{kicad_cli_path}"' + " pcb export pos " + f'"{str(pcb_fn)}"' + ' -o ' + f'"{str(pos_fn)}"' + \
        ' --side both --format csv --units mm']

def kicad_pcb_export_3d(kicad_cli_path, pcb_fn, output_folder):
    step_fn = output_folder / pcb_fn.stem
    step_fn = step_fn.with_suffix('.step')
    return [f'"{kicad_cli_path}"' + " pcb export step " + f'"{str(pcb_fn)}"' + ' --force -o ' + f'"{str(step_fn)}"']

def kicad_pcb_export_drawings(kicad_cli_path, pcb_fn, filename, layers):
    layer_list = ", ".join(layers)
    mirror = ''
    for l in layers:
        if 'B' in l:
            mirror = ' --mirror'
    command = f'"{kicad_cli_path}"' + " pcb export pdf " + f'"{str(pcb_fn)}"' + ' -o ' + f'"{filename}"' + \
        ' --layers ' + layer_list + ',Edge.Cuts' + mirror + ' --exclude-value --black-and-white'
    return [command]