# File name: main.py
# Created on: 12/25/2023
# Created by: Oleg Gordiushenkov

import tkinter as tk
from tkinter import filedialog
import traceback
import os

from kicad_processing_tools import kicad_process_project


project_fn=""#"C:\\Gordiushenkov\\Manufacturing\\Outsourcing\\EV48.01_11339_M.zip"
kicad_cli_path = r"C:\Program Files\KiCad\7.0\bin\kicad-cli"
bom_paths = [r"C:\Gordiushenkov\SlopeHelper\kicad5_libs\Scripts\bom_csv_eurocircuits_grouped_dnp.py",
    r"C:\Gordiushenkov\SlopeHelper\kicad5_libs\Scripts\bom_csv_KiCad_grouped_by_pn_and_fp_semicol.py"]
CAM_folder_name = "CAMOutputs"
PDF_folder_name = 'PDFs'

def open_project():
    global project_fn
    project_fn = filedialog.askopenfilename(filetypes=[("KiCad project file", "*.kicad_pro")])
    label_file.config(text=project_fn)

def process():
    try:
        result = kicad_process_project(kicad_cli_path, project_fn, bom_paths, CAM_folder_name, PDF_folder_name)

        text_box_output.delete('1.0', tk.END)
        text_box_output.insert('1.0', result)
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