import glob
from pathlib import Path
import os
from fontTools.ttLib import TTFont
from gftools.scripts import update_version

if os.path.exists("fonts"):
    for file in Path("fonts/").glob("**/*.ttf"):
        font = TTFont(file)
        if "Mono" in str(file):
            font["OS/2"].xAvgCharWidth = 500
        
        version_id = font["name"].getName(5, 3, 1, 0x409)
        font["head"].fontRevision = float(str(version_id).split(";")[0][8:])
        font.save(file, reorderTables=False)
        