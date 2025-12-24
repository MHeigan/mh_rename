**mh_rename — File Sequence Renamer (mh_tools)**

A small, practical GUI tool for quickly renaming image sequences (or any batch of files) using simple rules: **replace text**, **renumber**, and/or **change extension**.

Built for day-to-day production use where you just want the job done cleanly and predictably.

**Latest Release: mh_rename v1.2.0**
https://github.com/MHeigan/mh_rename/releases/tag/mh_rename_1_2_0

---

 **Features**

- **Select an Input Directory** containing files to rename
- **Optional Output Directory** (files are **moved** there while renaming)
- **Replace Text** (simple find/replace on the filename)
- **Renumber** with a **start number** and **padding**
  - Adds numbers as a **dot suffix**: `name.0001`
  - Automatically removes an existing trailing `._####` / `_.####` style number first
- **Change Extension** (e.g. `.png` → `.jpg`)
- **Preview Rename** before committing changes

---

## Download & Run (Windows)

1. Download the latest release ZIP from the **Releases** page.
2. Extract the ZIP to a convenient location (e.g. `D:\Tools\mh_rename\`).
3. Run `mh_rename.exe`.

> Tip: Keep a backup of your files. Preview first, rename second. You can also specify a different output directory; the Renamer will then copy and rename for you.

---

## How to Use

1. Click **Select Input Directory**
2. (Optional) Click **Select Output Directory**
3. Enable and fill any of these options:
   - **Text to replace** / **Replace with**
   - **Start number** (enable Renumber)
   - **Padding** (e.g. 4 → `0001`)
   - **New extension** (without the dot is fine)
4. Click **Preview Rename** to check the result
5. Click **Rename Files** to apply

---

## Examples

### Replace text
- `shotA_render_v003.0001.exr` → replace `shotA` with `shotB`

### Renumber (start 10, padding 4)
- `frame_anything.exr` → `frame_anything.0010.exr`, `frame_anything.0011.exr`, ...

### Change extension
- `plate.0100.png` → `plate.0100.jpg`

---

## Notes / Behaviour

- If **Output Directory** is set, files are **moved** into that folder while being renamed.
- If Output is not set, files are renamed **in place**.
- The tool processes the files in **sorted order** (alphabetical).

---

## Troubleshooting

- **Nothing happens / missing files:** make sure you extracted the ZIP completely before running.
- **Rename errors:** can occur if a destination filename already exists or the folder is not writable. Preview and ensure unique output names.

---

## License

CC BY-NC-ND 4.0
See the repository license file(s) included with this project.

---

## Credits

©2025 Martin P. Heigan — mh_tools
