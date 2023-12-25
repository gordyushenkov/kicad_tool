"C:\Program Files\KiCad\7.0\bin\kicad-cli" version
"C:\Program Files\KiCad\7.0\bin\kicad-cli" pcb export drill .\power_module_v1_6\Design\power_module_v1_6.kicad_pcb -u mm -o .\Test\CAMOutputs\ --excellon-separate-th
"C:\Program Files\KiCad\7.0\bin\kicad-cli" pcb export pdf .\power_module_v1_6\Design\power_module_v1_6.kicad_pcb -o .\Test\Docs\power_module_F.Fab.pdf --layers F.Fab,F.Silkscreen,Edge.Cuts
"C:\Program Files\KiCad\7.0\bin\kicad-cli" pcb export pdf .\power_module_v1_6\Design\power_module_v1_6.kicad_pcb -o .\Test\Docs\power_module_B.Fab.pdf -m --layers B.Fab,B.Silkscreen,Edge.Cuts
"C:\Program Files\KiCad\7.0\bin\kicad-cli" sch export python-bom .\power_module_v1_6\Design\power_module_v1_6.kicad_sch -o .\Test\Docs\power_module_BOM.xml
python "C:\Gordiushenkov\SlopeHelper\kicad5_libs\Scripts/bom_csv_eurocircuits_dnp.py" .\Test\Docs\power_module_BOM.xml .\Test\Docs\power_module_BOM.csv

"C:\Program Files\KiCad\7.0\bin\kicad-cli" pcb export gerbers .\power_module_v1_6\Design\power_module_v1_6.kicad_pcb -o .\Test\CAMOutputs\ --layers F.Cu,Edge.Cuts,B.Cu,F.Silkscreen,F.Mask,F.Paste --subtract-soldermask --no-x2

"C:\Program Files\KiCad\7.0\bin\kicad-cli" pcb export pos .\power_module_v1_6\Design\power_module_v1_6.kicad_pcb -o .\Test\CAMOutputs\power_module_pos --side both --format csv --units mm

REM "C:\Program Files\KiCad\7.0\bin\kicad-cli" pcb export step .\power_module_v1_6\Design\power_module_v1_6.kicad_pcb --force -o .\Test\Docs\power_module_step