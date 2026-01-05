import glob
import shutil
from pathlib import Path
import os
import ufoLib2
from ufomerge import merge_ufos

SOURCE = Path("sources")
EXPORT = Path("sources/build")
EXPORT.mkdir(exist_ok=True)

for file in SOURCE.glob("*.ufo"):
    # We keep a single copy of the common Hanzi data, and merge it into the Latins as necessary
    coreUFO = ufoLib2.Font.open(file)
    if "Regular" in str(file):
        commonUFO = ufoLib2.Font.open("sources/temp/LXGWWenKaiTC_common-Regular.ufo")
    elif "Medium" in str(file):
        commonUFO = ufoLib2.Font.open("sources/temp/LXGWWenKaiTC_common-Medium.ufo")
    elif "Bold" in str(file):
        commonUFO = ufoLib2.Font.open("sources/temp/LXGWWenKaiTC_common-Bold.ufo")
    else:
        commonUFO = ufoLib2.Font.open("sources/temp/LXGWWenKaiTC_common-Light.ufo")

    print(f"Merging {file.name}")

    merge_ufos(
        coreUFO,
        commonUFO,
        layout_handling="ignore",
        existing_handling="skip",
    )

    # Override the feature code for consistency
    if "Mono" in str(file):
        f = open("sources/features_mono.fea", "r")
    else:
        f = open("sources/features.fea", "r")
    features = f.read()

    coreUFO.features.text = features
    coreUFO.save(EXPORT / str(file.name), overwrite=True, validate=False)
