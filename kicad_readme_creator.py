# File name: kicad_readme_creator.py
# Created on: 12/27/2023
# Created by: Oleg Gordiushenkov

from pathlib import Path
from kicad_pcb_parser import kicad_pcb_parse

GERBER_LAYERS = {
    'F_Paste':'Top Paste',
    'F_Silkscreen':'Top Silk',
    'F_Mask':'Top Mask',
    'F_Cu':'Top',
    'Edge_Cuts': 'Board',
    'B_Cu': 'Bottom',
    'B_Mask': 'Bot Mask',
    'B_Silkscreen': 'Bot Silk',
    'B_Paste': 'Bot Paste',
    'NPTH': 'Non-plated holes',
    '-PTH': 'Plated holes',
}

def get_readme_fn(project_fn):
    project_path = Path(project_fn)
    return str(project_path.parent.parent / project_path.stem) + ' readme.txt'

def get_gerber_section(project_name, CAM_path):
    text = '-- Gerbers\n'
    selected_files = list(Path(CAM_path).glob(f'{project_name}*.gbr')) + list(Path(CAM_path).glob(f'{project_name}*.drl'))
    for key, value in GERBER_LAYERS.items():
        for f in selected_files:
            if key in f.name:
                text += f'{value}: {f.name}\n'
                break

    return text

def get_components_locations(project_name, CAM_path):
    text = '-- Components locations\n'
    selected_files = list(Path(CAM_path).glob(f'{project_name}*-all-pos*.csv'))
    for f in selected_files:
        text += f'{f.name}\n'
    return text

def get_BOMs(project_name, CAM_path):
    text = '-- BOM\n'
    selected_files = list(Path(CAM_path).glob(f'{project_name}*BOM*.csv'))
    for f in selected_files:
        text += f'{f.name}\n'
    return text

def get_readme(project_fn, CAM_path):
    project_name = Path(project_fn).stem
    readme_fn = Path(get_readme_fn(project_fn)).name
    readme_text = ''
    readme_text += f'filename: {readme_fn}\n'
    readme_text += f'\n'

    pcb_fn = Path(project_fn).with_suffix(".kicad_pcb")
    pcb_properties = kicad_pcb_parse(pcb_fn)
    readme_text += (f'-- Stack definition\n'
                    f'Layers: 2\n'
                    f'Material: {pcb_properties["material"]}\n'
                    f'Size: {pcb_properties["dimensions"][0]}x{pcb_properties["dimensions"][1]} mm\n'
                    f'Stack thickness: 1.6mm\n'
                    f'Outer layer thickness: {pcb_properties["thicnkess"] * 1000:.0f} um\n'
                    f'Finishing: {pcb_properties["finishing_layer"]}\n')

    readme_text += f'\n'
    readme_text += get_gerber_section(project_name, CAM_path)

    readme_text += f'\n'
    readme_text += get_components_locations(project_name, CAM_path)

    readme_text += f'\n'
    readme_text += get_BOMs(project_name, CAM_path)

    readme_text += f'\n'
    readme_text += f'-- Notes\n'
    for key, value in pcb_properties["comments"].items():
        if key not in ['comment 1']:
            readme_text += f'{value}\n'

    return readme_text


if __name__ == '__main__':
    project_fn = r"C:\Gordiushenkov\SlopeHelper\Electronics\SH\Units\IntEn\PCBs\power_module_v1_6\Design\power_module_v1_6.kicad_pro"
    CAM_path = Path(project_fn).parent.parent/"CAMOutputs"
    text = get_readme(project_fn, CAM_path)
    print(text)