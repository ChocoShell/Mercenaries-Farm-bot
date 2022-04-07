"""
This modules creates the executable folder for this console application.
"""
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
build_options = {
    "build_exe": "merc-farm-bot",
    "packages": [],
    "excludes": [],
    "includes": ["modules"],
    "include_files": ["conf/", "files/", "settings.ini"],
}

BASE = "Console"

executables = [Executable("main.py", base=BASE)]

setup(
    name="main",
    version="0.5",
    description="",
    options={"build_exe": build_options},
    executables=executables,
)
