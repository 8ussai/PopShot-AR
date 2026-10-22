"""Make the fonts in fonts/*.zip available to the scoreboard.

The .ttf/.otf files are unpacked into fonts/_extracted the first time.
On Windows they're then loaded for this process only (nothing is installed
system-wide). On macOS/Linux, install them yourself; see the README.
If a font can't be loaded, Tkinter falls back to its default font.
"""
import glob
import os
import sys
import zipfile

import config

FR_PRIVATE = 0x10


def _extract_fonts():
    os.makedirs(config.FONTS_CACHE, exist_ok=True)
    paths = []
    for zip_path in glob.glob(os.path.join(config.FONTS_FOLDER, "*.zip")):
        with zipfile.ZipFile(zip_path) as zf:
            for name in zf.namelist():
                base = os.path.basename(name)
                # The variable DynaPuff font clashes with its static versions, so skip it.
                if not base.lower().endswith((".ttf", ".otf")) or "VariableFont" in base:
                    continue
                out = os.path.join(config.FONTS_CACHE, base)
                if not os.path.exists(out):
                    with zf.open(name) as src, open(out, "wb") as dst:
                        dst.write(src.read())
                paths.append(out)
    return paths


def load_fonts():
    try:
        paths = _extract_fonts()
    except (OSError, zipfile.BadZipFile) as e:
        print(f"Couldn't unpack fonts: {e}")
        return
    if sys.platform == "win32":
        import ctypes
        for path in paths:
            ctypes.windll.gdi32.AddFontResourceExW(path, FR_PRIVATE, 0)
