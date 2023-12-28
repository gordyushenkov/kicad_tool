# File name: test_bom_generator.py
# Created on: 12/27/2023
# Created by: Oleg Gordiushenkov

import subprocess

bom_fn = r"temp.xml"
output_fn = f"temp.csv"

cmd = f'python "bom_csv_grouped_and_separate_dnp.py"' + ' ' + bom_fn + ' '+ output_fn
result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
print(result)