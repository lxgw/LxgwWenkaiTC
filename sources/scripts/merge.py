import glob
import shutil
from pathlib import Path
import os
import ufoLib2
from ufomerge import merge_ufos

if os.path.exists("sources/build"):
    shutil.rmtree("sources/build")
os.mkdir("sources/build")

SOURCE = Path("sources")
EXPORT = Path("sources/build")

for file in SOURCE.glob("*.ufo"):
    coreUFO = ufoLib2.Font.open(file)
    if "Regular" in str(file):
        commonUFO = ufoLib2.Font.open("sources/temp/LXGWWenKaiTC_common-Regular.ufo")
    elif "Bold" in str(file):
        commonUFO = ufoLib2.Font.open("sources/temp/LXGWWenKaiTC_common-Bold.ufo")
    else:
        commonUFO = ufoLib2.Font.open("sources/temp/LXGWWenKaiTC_common-Light.ufo")

    print ("Merging "+ str(file).split("/")[1])

    merge_ufos(
        coreUFO,
        commonUFO,
        layout_handling="ignore",
        existing_handling="skip",
    )
    coreUFO.save(EXPORT/str(file).split("/")[1],overwrite=True,validate=False)