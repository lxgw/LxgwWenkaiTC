import glob
from pathlib import Path
import os
from fontTools.ttLib import TTFont


if os.path.exists("fonts"):
    for file in Path("fonts/").glob("**/*.ttf"):
        if "Mono" in str(file):
            font = TTFont(file)
            font["OS/2"].xAvgCharWidth = 500
            font.save(file, reorderTables=False)