請運行 `build.bat` 或 `build.sh` 以製作字體。需要安裝 [`fontmake`](https://github.com/googlefonts/fontmake)：`pip3 install fontmake` 和 [`fontTools`](https://github.com/fonttools/fonttools)：`pip3 install fonttools`。

目前原始檔案使用 [UFO 3 ZIP 格式（`.ufoz`）](https://unifiedfontobject.org/versions/ufo3/)，礙於 `fontmake` 暫不支援 `.ufoz` 格式，因此運行 `extract_ufoz.py` 解壓縮後使用其 `.ufo` 資料夾製作字體。

`fix_mono.py` 是特別用於調整等寬字元版本（Mono）的字元平均寬度 `xAvgCharWidth`，使其西文與漢字可以以 1:2 比例對應。




Please run `build.bat` or  `build.sh` to build font. [`fontmake`](https://github.com/googlefonts/fontmake) (`pip3 install fontmake`) and [`fontTools`](https://github.com/fonttools/fonttools)（`pip3 install fonttools`） are required.

The source files are provided in [UFO 3 ZIP format (`.ufoz`)](https://unifiedfontobject.org/versions/ufo3/). As `fontmake` does not support `.ufoz` files yet, the script will run `extract_ufoz.py` to extract the `.ufo` folders before running `fontmake` on the `.ufo` folders to build the fonts.

`fix_mono.py` is used for fixing the `xAvgCharWidth` of monospaced fonts.

