# mh_rename – File Sequence Renamer

`mh_rename` is a small GUI tool (part of the **mh_tools** suite) for batch-renaming numbered file sequences.
It’s designed for VFX / CGI workflows: renumbering frame sequences, tweaking padding, changing extensions, and doing safe text replacements with a live preview before anything touches disk.

---

## Features

- **Browse-based GUI (no CLI needed)** – point at a folder and work visually.
- **Replace Section**
  - Find text in filenames and replace it with something else.
  - Useful for renaming shots, passes, or tokens without touching the frame numbers.
- **Renumber Sequence**
  - Start at any frame (default: `1001`) and renumber in order.
  - Strips an existing 3–5 digit suffix and appends the new padded frame number.
- **Change Padding**
  - Control the number of digits (e.g. `001`, `0001`, `0100`).
  - Default padding is `4`.
- **Change Extension**
  - Optionally change `.exr` → `.png`, `.tif` → `.jpg`, etc.
- **Preview Rename**
  - Side-by-side list of **original → new** filenames in a scrollable window.
  - Preview mode does **not** modify files.
- **Output Directory (optional)**
  - Rename in-place or send renamed files to a different folder.

The app uses the standard `mh_tools` Tkinter layout, including a labelled frame called `mh_tools` and a centred window with a splash screen on startup.

---

## Getting Started

### Option 1 – Use the EXE (recommended for artists)

On Windows you’ll typically get a packaged executable:

1. Place `mh_Rename.exe` (and the `_internal` folder with `splash.png`, if present) in any writable directory.
2. Double-click **mh_Rename.exe**.
3. The splash screen shows briefly, then the main GUI appears.

You don’t need Python installed for the EXE build.

### Option 2 – Run from source (for developers / tinkerers)

Requirements:

- Python 3.8+ (tested with standard CPython)
- Tkinter (ships with most Python installs on Windows/macOS/Linux)

Run:

```bash
python mh_rename.py
```

The splash + GUI behaviour is the same as the EXE.

---

## UI Overview

All controls live inside a labelled frame called **mh_tools** for consistency with the rest of the mh_tools suite.

### 1. Input & Output Directories

- **Select Input Directory**  
  Folder containing the files you want to rename.
- **Select Output Directory (Optional)**  
  If omitted, files will be renamed **in the input folder**.  
  If set, files are moved/renamed into this output folder instead.

---

### 2. Replace Section

Labelled frame: **Replace Section**.

- Tick **Enable** to activate replacement.
- **Text to replace** – the exact substring you want to remove or change.
- **Replace with** – replacement text (can be empty to just remove).

Example:  
`frame_001.png` → replace `frame_` with `shot_` → becomes `shot_001.png`.

---

### 3. Renumber Sequence

Labelled frame: **Renumber Sequence**.

- Tick **Enable** to renumber.
- **Start number** – starting frame (default `1001`).

Renumbering logic:

- Strips a trailing pattern like `.<digits>` or `_<digits>` (3–5 digits).
- Appends a new padded number (length defined in **Change Padding**).
- The counter increments per file in sorted order.

---

### 4. Change Padding

Labelled frame: **Change Padding**.

- Tick **Enable** to control digit width.
- **Padding** – number of digits to use (default `4`).

If renumbering is enabled, padding applies to the new frame number:
- `Start = 10`, `Padding = 4` → `0010`, `0011`, …

---

### 5. Change Extension

Labelled frame: **Change Extension**.

- Tick **Enable** to change file type extension.
- **New extension** – type without the leading dot (e.g. `jpg`, `exr`).

If disabled, original extensions are preserved.

---

## Preview and Rename Workflow

1. **Set Directories**
   - Choose an **Input Directory**.
   - Optionally choose an **Output Directory**.

2. **Configure Options**
   - Enable **Replace Section** / **Renumber Sequence** / **Change Padding** / **Change Extension** as needed.
   - Fill in the related fields.

3. **Preview Rename (safe)**
   - Click **Preview Rename**.
   - A new window opens showing one line per file:  
     `original_name.ext → new_name.ext`.  
   - Use this to sanity-check before committing.

4. **Rename Files (commit)**
   - When happy with the preview, close it and click **Rename Files**.
   - Files are renamed/moved according to your settings.
   - A confirmation dialog appears when done.

---

## Example

**Original files**

```text
frame_001.png
frame_002.png
```

**Settings**

- Replace: `frame_` → `shot_`
- Renumber Sequence: **Enable**
  - Start number: `10`
- Change Padding: **Enable**
  - Padding: `4`
- Change Extension: **Enable**
  - New extension: `jpg`

**Result**

```text
frame_001.png → shot_0010.jpg
frame_002.png → shot_0011.jpg
```

---

## Licence

CC BY-NC-ND 4.0

---

## Credits

- **Author:** Martin Heigan  
- **Tool family:** Part of the broader `mh_tools` utility suite for VFX, CGI and general production workflows.
