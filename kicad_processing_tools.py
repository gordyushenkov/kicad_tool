# File name: kicad_processing_tools.py
# Created on: 12/26/2023
# Created by: Oleg Gordiushenkov
from pathlib import Path
import subprocess
from kicad_sch_tools import kicad_sch_export_netlist, kicad_sch_export_pdf
from kicad_pcb_tools import kicad_pcb_export_gerber, kicad_pcb_export_drill, kicad_pcb_export_pnp, \
    kicad_pcb_export_3d, kicad_pcb_export_drawings
from kicad_readme_creator import get_readme, get_readme_fn
from kicad_bom_writer import make_bom_default
import zipfile


ALL_LAYERS = [
    'F.Silkscreen',
    'F.Paste',
    'F.Mask',
    'F.Cu',
    #'In1.Cu' after adding generates a bunch of extra gerber files
    'Edge.Cuts',
    #'In2.Cu'
    'B.Cu',
    'B.Mask',
    'B.Paste',
    'B.Silkscreen']


def create_zip_archive(archive_name, files_to_pack):
    fn = archive_name + ".zip"
    with zipfile.ZipFile(fn, "w", compression=zipfile.ZIP_DEFLATED) as zip_file:
        for file_to_pack in files_to_pack:
            # Calculate the relative path within the archive
            relative_path = Path(file_to_pack).relative_to(Path(files_to_pack[0]).parent)

            # Add the file to the archive with its relative path
            zip_file.write(file_to_pack, arcname=str(relative_path))
    return fn

def run_commands(cmds):
    msg = ''
    for cmd in cmds:
        # msg += f'{cmd}\n'
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        msg += result.stdout
        if result.returncode:
            msg += result.stderr
    return msg

def kicad_process_project(kicad_cli_path, project_fn, boms, CAM_folder_name=None, pdf_foldername=None, step_folder_name=None):
    path_obj = Path(project_fn)
    sch_fn = path_obj.with_suffix(".kicad_sch")
    pcb_fn = path_obj.with_suffix(".kicad_pcb")
    root_folder = path_obj.parent.parent
    folder_names = [CAM_folder_name, pdf_foldername, step_folder_name]
    fld_dict = {}
    for fld in folder_names:
        if fld is not None:
            fld_dict[fld] = root_folder / fld
            Path(fld_dict[fld]).mkdir(parents=True, exist_ok=True)

    if not sch_fn.is_file():
        return f'Error: {sch_fn} does not exist!!!'

    msg = ''

    if CAM_folder_name is not None:
        path_obj = Path(fld_dict[CAM_folder_name])
        xml_fn = r'temp.xml'
        bom_fn = path_obj / sch_fn.stem
        msg += run_commands(kicad_sch_export_netlist(kicad_cli_path, sch_fn, xml_fn))
        bom_out = make_bom_default(xml_fn, bom_fn)
        if len(bom_out):
            msg += '!!!!!!!!!!!!!!!!!!!!!!!!!!\n'
            msg += bom_out
            msg += '!!!!!!!!!!!!!!!!!!!!!!!!!!\n\n'

    if pdf_foldername is not None:
        msg += run_commands(kicad_sch_export_pdf(kicad_cli_path, sch_fn, fld_dict[pdf_foldername]))

    if pcb_fn.is_file():
        if step_folder_name is not None:
            msg += run_commands(kicad_pcb_export_3d(kicad_cli_path, pcb_fn, fld_dict[step_folder_name]))

        if CAM_folder_name is not None:
            msg += run_commands(kicad_pcb_export_gerber(kicad_cli_path, pcb_fn, fld_dict[CAM_folder_name], ALL_LAYERS))
            msg += run_commands(kicad_pcb_export_drill(kicad_cli_path, pcb_fn, fld_dict[CAM_folder_name]))
            msg += run_commands(kicad_pcb_export_pnp(kicad_cli_path, pcb_fn, fld_dict[CAM_folder_name]))
            for l in ['F.Fab','B.Fab']:
                fn = str(Path(fld_dict[CAM_folder_name])/sch_fn.stem) + ' ' + l + ' assy.pdf'
                cmd = kicad_pcb_export_drawings(kicad_cli_path, pcb_fn, fn, layers=[l])
                print(cmd)
                msg += run_commands(cmd)
            readme_fn = get_readme_fn(project_fn)
            readme_text = get_readme(project_fn, fld_dict[CAM_folder_name])

            with open(str(root_folder/readme_fn), 'w') as file:
                file.write(readme_text)
                msg += f'Readme file created:\n{readme_fn}'


                # Packing
            # archive_path = str(fld_dict[CAM_folder_name] / path_obj.stem) + ' gerber'
            # selected_files = list(fld_dict[CAM_folder_name].glob(f'*.gbr')) + list(fld_dict[CAM_folder_name].glob(f'*.drl')) + list(fld_dict[CAM_folder_name].glob(f'*pos*.csv'))
            # gerber_arch_fn = create_zip_archive(archive_path, selected_files)
            # msg += f'Gerber archive created: {gerber_arch_fn}\n'
            #
            # CAM_archive_path = str(fld_dict[CAM_folder_name] / path_obj.stem) + ' CAM'
            # selected_files = list(fld_dict[CAM_folder_name].glob(f'*BOM*.csv')) + [gerber_arch_fn]
            # CAM_arch_fn = create_zip_archive(CAM_archive_path, selected_files)
            # msg += f'CAM archive created: {CAM_arch_fn}\n'
            #
            # manuf_archive_path = str(fld_dict[CAM_folder_name].parent / path_obj.stem) + ' manufacturing'
            # selected_files = list(fld_dict[CAM_folder_name].parent.glob(f'*readme*.txt')) + [CAM_arch_fn]
            # manuf_arch_fn = create_zip_archive(manuf_archive_path, selected_files)
            # msg += f'Manufacturing archive created: {manuf_arch_fn}\n'
            #
            # # Remove temporary archives
            # Path(gerber_arch_fn).unlink()
            # Path(CAM_arch_fn).unlink()

    return msg

def kicad_pack_documentation(project_fn, CAM_folder_name=None):
    path_obj = Path(project_fn)
    root_folder = path_obj.parent.parent
    CAM_folder_path = root_folder / CAM_folder_name
    archive_path = str(CAM_folder_path / path_obj.stem) + ' gerber'
    selected_files = list(CAM_folder_path.glob(f'*.gbr')) + list(
        CAM_folder_path.glob(f'*.drl')) + list(CAM_folder_path.glob(f'*pos*.csv'))
    gerber_arch_fn = create_zip_archive(archive_path, selected_files)

    CAM_archive_path = str(CAM_folder_path / path_obj.stem) + ' CAM'
    selected_files = list(CAM_folder_path.glob(f'*BOM*.csv')) \
                    + list(CAM_folder_path.glob(f'*assy.pdf')) \
                     + [gerber_arch_fn]
    CAM_arch_fn = create_zip_archive(CAM_archive_path, selected_files)

    manuf_archive_path = str(CAM_folder_path.parent / path_obj.stem) + ' manufacturing'
    selected_files = list(CAM_folder_path.parent.glob(f'*readme*.txt')) + [CAM_arch_fn]
    manuf_arch_fn = create_zip_archive(manuf_archive_path, selected_files)
    msg = f'Manufacturing archive created: {manuf_arch_fn}\n'

    # Remove temporary archives
    # Path(gerber_arch_fn).unlink()
    Path(CAM_arch_fn).unlink()
    return msg

def test_project_processing(kicad_cli_path, project_fn, bom_paths, CAM_folder_name, pdf_foldername, step_folder_name):
    result = kicad_process_project(kicad_cli_path, project_fn, bom_paths, CAM_folder_name, pdf_foldername, step_folder_name)
    print(result)

def test_PCB_pdf(kicad_cli_path, project_fn, CAM_folder_name):
    from kicad_pcb_tools import kicad_pcb_export_drawings
    layers = ['F.Fab','B.Fab']

    path_obj = Path(project_fn)
    pcb_fn = path_obj.with_suffix(".kicad_pcb")
    root_folder = path_obj.parent.parent
    out_folder = root_folder / 'CAMOutputs'

    commands = []
    for l in layers:
        print(l)
        fn = str(out_folder / l) + ".pdf"
        commands.extend(kicad_pcb_export_drawings(kicad_cli_path, pcb_fn, fn, layers=[l]))
    print(commands)
    msg = run_commands(commands)
    print(msg)

if __name__ == '__main__':
    project_fn = r"C:\Gordiushenkov\SlopeHelper\Electronics\SH\Units\BMS\bms_ctrl_v1_1\Design\bms_ctrl_v1_1.kicad_pro"
    kicad_cli_path = r"C:\Program Files\KiCad\7.0\bin\kicad-cli"
    bom_paths = [r"C:\Gordiushenkov\SlopeHelper\kicad5_libs\Scripts\bom_csv_eurocircuits_grouped_dnp.py",
                 r"C:\Gordiushenkov\SlopeHelper\kicad5_libs\Scripts\bom_csv_KiCad_grouped_by_pn_and_fp_semicol.py"]
    CAM_folder_name = "CAMOutputs"
    pdf_foldername = "PDFs"
    step_folder_name = "3d models"
    # test_project_processing(kicad_cli_path, project_fn, bom_paths, CAM_folder_name, pdf_foldername, step_folder_name)
    test_PCB_pdf(kicad_cli_path, project_fn, CAM_folder_name)
