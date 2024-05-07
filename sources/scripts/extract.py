import glob
import zipfile
from pathlib import Path
import os, shutil

if os.path.exists("sources/temp"):
    shutil.rmtree("sources/temp")
os.mkdir("sources/temp")
for ufo in Path("sources/").glob("*.ufoz"):
    with zipfile.ZipFile(ufo, 'r') as zip_ref:
        zip_ref.extractall("sources/temp")
