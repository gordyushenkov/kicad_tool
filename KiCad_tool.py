# File name: main.py
# Created on: 12/25/2023
# Created by: Oleg Gordiushenkov

import tkinter as tk
from tkinter import filedialog, Scrollbar
import traceback
from config_provider import read_config

from kicad_processing_tools import kicad_process_project, kicad_pack_documentation


project_fn=""#"C:\\Gordiushenkov\\Manufacturing\\Outsourcing\\EV48.01_11339_M.zip"
# kicad_cli_path = r"C:\Program Files\KiCad\7.0\bin\kicad-cli"
bom_paths = [f'bom_csv_grouped_and_separate_dnp.py']
    # r"C:\Gordiushenkov\SlopeHelper\kicad5_libs\Scripts\bom_csv_eurocircuits_grouped_dnp.py",
    # r"C:\Gordiushenkov\SlopeHelper\kicad5_libs\Scripts\bom_csv_KiCad_grouped_by_pn_and_fp_semicol.py"]
CAM_folder_name = "CAMOutputs"
PDF_folder_name = 'PDFs'
step_folder_name = '3d models'
version = "1.4"
date = "2024.08.10"

def open_project():
    global project_fn
    project_fn = filedialog.askopenfilename(filetypes=[("KiCad project file", "*.kicad_pro")])
    label_file.config(text=project_fn)

def process():
    try:
        if project_fn:
            msg = f'Generating documentation for\n' \
                  f'{project_fn}\n' \
                  f'Wait for a while'
            text_box_output.delete('1.0', tk.END)
            text_box_output.insert('1.0', msg)
            app.update()
            app.update_idletasks()

            result = 'Documentation created successfully!\n\n'
            result += kicad_process_project(kicad_cli_path, project_fn,
                                            boms=bom_paths,
                                            CAM_folder_name = CAM_folder_name,
                                            pdf_foldername=PDF_folder_name,
                                            step_folder_name=step_folder_name)

            text_box_output.delete('1.0', tk.END)
            text_box_output.insert('1.0', result)
        else:
            msg = 'Choose the KiCad project file by pressing the Open button'
            text_box_output.delete('1.0', tk.END)
            text_box_output.insert('1.0', msg)
    except Exception as e:
        msg = 'Runtime error occured:\n'

        traceback_info = traceback.format_exc()
        msg += f'{traceback_info}'
        text_box_output.delete('1.0', tk.END)
        text_box_output.insert('1.0', msg)

def do_packing():
    try:
        if project_fn:
            msg = f'Packing documentation for\n' \
                  f'{project_fn}\n' \
                  f'Wait for a while'
            text_box_output.delete('1.0', tk.END)
            text_box_output.insert('1.0', msg)
            app.update()
            app.update_idletasks()

            result = 'Documentation archive packed successfully!\n\n'
            result += kicad_pack_documentation(project_fn, CAM_folder_name)

            text_box_output.delete('1.0', tk.END)
            text_box_output.insert('1.0', result)
        else:
            msg = 'Choose the KiCad project file by pressing the Open button'
            text_box_output.delete('1.0', tk.END)
            text_box_output.insert('1.0', msg)
    except Exception as e:
        msg = 'Runtime error occured:\n'

        traceback_info = traceback.format_exc()
        msg += f'{traceback_info}'
        text_box_output.delete('1.0', tk.END)
        text_box_output.insert('1.0', msg)

def on_scroll(*args):
    text_box_output.yview(*args)

app = tk.Tk()
app.title(f"KiCad tool v {version} ({date})")
app.minsize(500, 300)

frame_arch = tk.Frame(app)
frame_arch.pack(fill="x")
frame_erp = tk.Frame(app)
frame_erp.pack(fill="x")
frame_output = tk.Frame(app)
frame_output.pack()

PADX = 5
PADY = 5
TEXTWIDTH = 100

open_button = tk.Button(frame_arch, text="Open", command=open_project)
open_button.pack(padx=PADX, pady=PADY, side='left')
label_file = tk.Label(frame_arch, text="Choose kicad project file")
label_file.pack(pady=PADY, side='left')

frame_buttons = tk.Frame(app)
frame_buttons.pack()

compare_button = tk.Button(frame_buttons, text="Generate", command=process)
compare_button.pack(side=tk.LEFT, padx=PADX, pady=PADY,)

pack_button = tk.Button(frame_buttons, text="Pack", command=do_packing)
pack_button.pack(side=tk.LEFT, padx=PADX, pady=PADY,)

frame_text = tk.Frame(app)
frame_text.pack(fill=tk.BOTH, expand=True, padx=PADX, pady=PADY,)
text_box_output = tk.Text(frame_text, wrap=tk.WORD, height=40, width=TEXTWIDTH)
text_box_output.pack(side="left", fill=tk.BOTH, expand=True)

scrollbar = Scrollbar(frame_text, command=on_scroll)
scrollbar.pack(side="right", fill="y")
text_box_output.config(yscrollcommand=scrollbar.set)

config = read_config('config.yml')
if not config or 'kicad_cli_path' not in config:
    Instruction = """Create the configuration file in YAML format:\n
    1. Create a config.yml file in the executable directory or rename the template provided (config_linux.yml)
    2. Put the following line into config.yml: kicad_cli_path: [path_to_kicad-cli],
    where [path_to_kicad-cli] is the path to the kicad-cli executable distributed with KiCad.
    Default location is within the KiCad installation folder, for example:
       Windows: "C:\\Program Files\\KiCad\\7.0\\bin\\kicad-cli"   (quote paths with spaces)
       Linux:   /bin/kicad-cli
    For the KiCad AppImage, kicad-cli is a subcommand, so give both the AppImage path
    and the subcommand separated by a space, for example:
       /home/user/Applications/KiCad.AppImage kicad-cli
    3. Restart the application
    """
else:
    kicad_cli_path = config['kicad_cli_path']
    Instruction = """Instruction:
    1. Choose the kicad project file by pressing the Open button
    2. Press the generate button to create documentation
    3. Press the pack button to create manufacturing archive"""

text_box_output.insert('1.0', Instruction)

app.mainloop()