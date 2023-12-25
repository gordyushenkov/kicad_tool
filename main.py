# File name: main.py
# Created on: 12/25/2023
# Created by: Oleg Gordiushenkov

import tkinter as tk
from tkinter import filedialog
import traceback
import os
from pathlib import Path
import subprocess


project_fn=""#"C:\\Gordiushenkov\\Manufacturing\\Outsourcing\\EV48.01_11339_M.zip"
kicad_cli_path = r"C:\Program Files\KiCad\7.0\bin\kicad-cli"
CAM_folder_name = "CAMOutputs"

def open_project():
    global project_fn
    project_fn = filedialog.askopenfilename(filetypes=[("KiCad project file", "*.kicad_pro")])
    label_file.config(text=project_fn)

def process():
    try:
        path_obj = Path(project_fn)
        sch_fn = path_obj.with_suffix(".kicad_sch")
        pcb_fn = path_obj.with_suffix(".kicad_pcb")
        root_folder = path_obj.parent.parent
        output_folder = root_folder / CAM_folder_name

        command = f'"{kicad_cli_path}"' + " pcb export gerbers " + str(pcb_fn) + ' -o ' + str(output_folder) \
                  + ' --layers F.Cu,Edge.Cuts,B.Cu,F.Silkscreen,F.Mask,F.Paste --no-x2 --no-protel-ext --subtract-soldermask'
        msg = f'{command}\n'
        print(command)
        result = subprocess.run(command, shell=True, capture_output=True, text=True)

        # Print the output
        msg += result.stdout + '\n'
        if result.returncode:
            msg += result.stderr + '\n'
        print(result)
        text_box_output.delete('1.0', tk.END)
        text_box_output.insert('1.0', msg)
    except Exception as e:
        msg = 'Runtime error occured:\n'

        traceback_info = traceback.format_exc()
        msg += f'{traceback_info}'
        text_box_output.delete('1.0', tk.END)
        text_box_output.insert('1.0', msg)

app = tk.Tk()
app.title("CT creator")

frame_arch = tk.Frame(app)
frame_arch.pack(fill="x")
frame_erp = tk.Frame(app)
frame_erp.pack(fill="x")
frame_output = tk.Frame(app)
frame_output.pack()

PADX = 5
PADY = 5
TEXTWIDTH = 100

open_button = tk.Button(frame_arch, text="KiCad project file", command=open_project)
open_button.pack(padx=PADX, pady=PADY, side='left')
label_file = tk.Label(frame_arch, text="Choose kicad project file")
label_file.pack(pady=PADY, side='left')


compare_button = tk.Button(frame_output, text="Generate", command=process)
compare_button.pack(pady=PADY,)

text_box_output = tk.Text(frame_output, wrap=tk.WORD, height=40, width=TEXTWIDTH)
text_box_output.pack(fill=tk.BOTH, expand=True)

Instruction = """Instruction"""

text_box_output.insert('1.0', Instruction)

app.mainloop()