import glob
from pathlib import Path
import os
from fontTools.ttLib import TTFont
from gftools.scripts import update_version

if os.path.exists("fonts"):
    for file in Path("fonts/").glob("**/*.ttf"):
        font = TTFont(file)

        font["OS/2"].panose.bFamilyType = 2
        font["OS/2"].panose.bSerifStyle = 2

        if "Light" in str(file):
            font["OS/2"].panose.bWeight = 4
        elif "Medium" in str(file):
            font["OS/2"].panose.bWeight = 6
        elif "Bold" in str(file):
            font["OS/2"].panose.bWeight = 8
        else:
            font["OS/2"].panose.bWeight = 5

        if "Mono" in str(file):
            font["OS/2"].xAvgCharWidth = 500
            font["OS/2"].panose.bProportion = 9
            font["post"].isFixedPitch = 1
        
        
        version_id = font["name"].getName(5, 3, 1, 0x409)
        font["head"].fontRevision = float(str(version_id).split(";")[0][8:])
        font.save(file, reorderTables=False)
        