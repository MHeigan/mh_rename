echo off

python -m PyInstaller --onedir --windowed --noconsole --icon ./mh_tools_icon.ico --version-file=version.txt ./mh_rename.py

Pause