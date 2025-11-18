import os
import re
import tkinter as tk
from tkinter import filedialog, messagebox

"""
mh_tools - File Sequence Renamer
--------------------------------
A Tkinter-based GUI tool for batch renaming numbered file sequences.
Supports: replace text sections, renumber sequences with padding,
change file extensions, and preview renames before execution.
"""

class FileRenamerGUI:
    """
    Main application class for the file renamer GUI.
    """
    def __init__(self, root):
        """
        Initialize the main window and all UI components.
        """
        self.root = root
        self.root.title("mh_tools - File Sequence Renamer")
        self.root.geometry("640x780")  # Slightly taller to accommodate comments

        # Main container frame
        self.container = tk.LabelFrame(
            root,
            text="mh_tools",
            padx=10,
            pady=10
        )
        self.container.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        # Input and output directory selection
        self.setup_directory_selection()

        # Replace / Renumber / Padding / Extension sections
        self.setup_feature_toggles()
        self.setup_replace_section()
        self.setup_renumber_section()
        self.setup_padding_section()
        self.setup_extension_section()

        # Action buttons: preview and rename
        self.setup_action_buttons()

        # Internal state
        self.input_dir = ""
        self.output_dir = ""

    def setup_directory_selection(self):
        """Create input/output directory browse controls."""
        dir_frame = tk.Frame(self.container)
        dir_frame.pack(fill="x", pady=(0, 10))

        # Input
        self.input_dir_label = tk.Label(
            self.container,
            text="No input directory selected"
        )
        self.input_dir_label.pack(pady=5)
        tk.Button(
            self.container,
            text="Select Input Directory",
            command=self.select_input_directory,
            bg="light grey"
        ).pack(pady=5)

        # Output
        self.output_dir_label = tk.Label(
            self.container,
            text="No output directory selected (rename in place)"
        )
        self.output_dir_label.pack(pady=5)
        tk.Button(
            self.container,
            text="Select Output Directory (Optional)",
            command=self.select_output_directory,
            bg="light grey"
        ).pack(pady=5)

    def setup_feature_toggles(self):
        """Create section headers and checkboxes for each feature."""
        # Replace Section
        self.replace_var = tk.BooleanVar()
        replace_frame = tk.LabelFrame(
            self.container,
            text="Replace Section",
            padx  = 10,
            pady  = 10
        )
        replace_frame.pack(fill="x", padx=10, pady=5)
        tk.Checkbutton(
            replace_frame,
            text="Enable",
            variable=self.replace_var
        ).pack(anchor="w")

        # We'll populate specific controls in setup_replace_section
        self.replace_frame = replace_frame

        # Renumber Section
        self.renumber_var = tk.BooleanVar()
        renumber_frame = tk.LabelFrame(
            self.container,
            text="Renumber Sequence",
            padx=10,
            pady=10
        )
        renumber_frame.pack(fill="x", padx=10, pady=5)
        tk.Checkbutton(
            renumber_frame,
            text="Enable",
            variable=self.renumber_var
        ).pack(anchor="w")

        self.renumber_frame = renumber_frame

        # Padding Section
        self.padding_var = tk.BooleanVar()
        padding_frame = tk.LabelFrame(
            self.container,
            text="Change Padding",
            padx=10,
            pady=10
        )
        padding_frame.pack(fill="x", padx=10, pady=5)
        tk.Checkbutton(
            padding_frame,
            text="Enable",
            variable=self.padding_var
        ).pack(anchor="w")
        tk.Label(padding_frame, text="Padding:").pack(anchor="w")
        self.padding_entry = tk.Entry(padding_frame)
        self.padding_entry.insert(0, "4")  # Default padding value
        self.padding_entry.pack(fill="x", pady=2)

        self.padding_frame = padding_frame

        # Extension Section
        self.ext_var = tk.BooleanVar()
        ext_frame = tk.LabelFrame(
            self.container,
            text="Change Extension",
            padx=10,
            pady=10
        )
        ext_frame.pack(fill="x", padx=10, pady=5)
        tk.Checkbutton(
            ext_frame,
            text="Enable",
            variable=self.ext_var
        ).pack(anchor="w")
        tk.Label(ext_frame, text="New extension (without dot):").pack(anchor="w")
        self.ext_entry = tk.Entry(ext_frame)
        self.ext_entry.insert(0, "exr")
        self.ext_entry.pack(fill="x", pady=2)

        self.ext_frame = ext_frame

    def setup_replace_section(self):
        """Create controls for text replace feature."""
        tk.Label(self.replace_frame, text="Text to replace:").pack(anchor="w")
        self.find_entry = tk.Entry(self.replace_frame)
        self.find_entry.pack(fill="x", pady=2)

        tk.Label(self.replace_frame, text="Replace with:").pack(anchor="w")
        self.replace_entry = tk.Entry(self.replace_frame)
        self.replace_entry.pack(fill="x", pady=2)

    def setup_renumber_section(self):
        """Create controls for renumbering sequence."""
        tk.Label(self.renumber_frame, text="Start number:").pack(anchor="w")
        self.start_entry = tk.Entry(self.renumber_frame)
        self.start_entry.insert(0, "1001")  # Default start number
        self.start_entry.pack(fill="x", pady=2)

        tk.Label(self.renumber_frame, text="(Existing 3–5 digit suffix will be stripped)").pack(anchor="w")

    def setup_padding_section(self):
        """Create controls for changing padding."""
        # Already created in setup_feature_toggles; this method kept for clarity/extension.
        pass

    def setup_extension_section(self):
        """Additional configuration for extension changes (already prepared)."""
        # Already created in setup_feature_toggles; this method kept for clarity/extension.
        pass

    def setup_action_buttons(self):
        """Create Preview and Rename buttons."""
        btn_frame = tk.Frame(self.container)
        btn_frame.pack(fill="x", pady=10)

        tk.Button(
            btn_frame,
            text="Preview Rename",
            command=self.preview_renames,
            bg="light grey"
        ).pack(side="left", expand=True, padx=5)

        tk.Button(
            btn_frame,
            text="Rename Files",
            command=self.rename_files,
            bg="light grey"
        ).pack(side="left", expand=True, padx=5)

    def select_input_directory(self):
        """Open a dialog to select the input directory."""
        directory = filedialog.askdirectory(title="Select Input Directory")
        if directory:
            self.input_dir = os.path.normpath(directory)
            self.input_dir_label.config(text=f"Input: {self.input_dir}")

    def select_output_directory(self):
        """Open a dialog to select the output directory (optional)."""
        directory = filedialog.askdirectory(title="Select Output Directory")
        if directory:
            self.output_dir = os.path.normpath(directory)
            self.output_dir_label.config(text=f"Output: {self.output_dir}")
        else:
            self.output_dir = ""
            self.output_dir_label.config(text="No output directory selected (rename in place)")

    def get_new_filename(self, filename, counter, padding, start_number):
        """
        Build a new filename based on the enabled options:
        - Replace text section.
        - Renumber sequence.
        - Change padding.
        - Change extension.
        """
        name, ext = os.path.splitext(filename)
        new_name = name
        new_ext = ext

        # 1) Replace Section
        if self.replace_var.get():
            find_text = self.find_entry.get()
            replace_text = self.replace_entry.get()
            if find_text:
                new_name = new_name.replace(find_text, replace_text)

        # 2) Renumber Sequence
        if self.renumber_var.get():
            # Remove existing trailing .#### or _####
            new_name = re.sub(r"(\.|\_)\d{3,5}$", "", new_name)
            # Build new padded number
            if start_number is not None:
                frame_num = start_number + counter
                pad_width = 4
                if self.padding_var.get():
                    try:
                        pad_width = int(self.padding_entry.get())
                    except ValueError:
                        pad_width = 4
                frame_str = str(frame_num).zfill(pad_width)
                new_name = f"{new_name}.{frame_str}"

        # 3) Change Extension
        if self.ext_var.get():
            ext_txt = self.ext_entry.get().strip()
            if ext_txt:
                new_ext = f".{ext_txt}"

        return f"{new_name}{new_ext}"

    def preview_renames(self):
        """
        Show a preview of the renaming operations in a separate window.
        Does not perform any actual file operations.
        """
        input_dir = self.input_dir
        if not input_dir or not os.path.isdir(input_dir):
            messagebox.showerror("Error", "Please select a valid input directory.")
            return

        files = sorted(os.listdir(input_dir))
        if not files:
            messagebox.showwarning("No Files", "The selected directory is empty.")
            return

        try:
            start_number = int(self.start_entry.get()) if self.renumber_var.get() else None
        except ValueError:
            messagebox.showerror("Error", "Start number must be an integer.")
            return

        try:
            if self.padding_var.get():
                int(self.padding_entry.get())
        except ValueError:
            messagebox.showerror(self.root, "Error", "Padding must be an integer.")
            return

        preview = tk.Toplevel(self.root)
        preview.title("Preview Renames")
        preview.geometry("600x400")

        # Text widget with scrollbars
        text = tk.Text(preview, wrap="none")
        text.pack(fill="both", expand=True)

        scrollbar_y = tk.Scrollbar(preview, orient="vertical", command=text.yview)
        scrollbar_y.pack(side="right", fill="y")
        text.config(yscrollcommand=scrollbar_y.set)

        counter = 0
        for f in files:
            if os.path.isdir(os.path.join(input_dir, f)):
                continue
            new_name = self.get_new_filename(f, counter, int(self.padding_entry.get()), start_number)
            line = f"{f}  ->  {new_name}\n"
            text.insert("end", line)
            if self.renumber_var.get():
                counter += 1

        text.config(state="disabled")

    def rename_files(self):
        """
        Execute the renaming operations on disk.
        """
        input_dir = self.input_dir
        if not input_dir or not os.path.isdir(input_dir):
            messagebox.showerror("Error", "Please select a valid input directory.")
            return

        files = sorted(os.listdir(input_dir))
        if not files:
            messagebox.showwarning("No Files", "The selected directory is empty.")
            return

        # Confirm action
        proceed = messagebox.askyesno(
            "Confirm Rename",
            "Are you sure you want to rename the files?"
        )
        if not proceed:
            return

        try:
            start_number = int(self.start_entry.get()) if self.renumber_var.get() else None
        except ValueError:
            messagebox.showerror("Error", "Start number must be an integer.")
            return

        try:
            padding = int(self.padding_entry.get()) if self.padding_var.get() else 4
        except ValueError:
            messagebox.showerror("Error", "Padding must be an integer.")
            return

        output_dir = self.output_dir if self.output_dir else self.input_dir
        if not os.path.isdir(output_dir):
            try:
                os.makedirs(output_dir, exist_ok=True)
            except Exception as e:
                messagebox.showerror("Error", f"Could not create output directory:\n{e}")
                return

        counter = 0
        for f in files:
            src = os.path.join(input_dir, f)
            if os.path.isdir(src):
                continue

            new_name = self.get_new_filename(f, counter, padding, start_number)
            dst = os.path.join(output_dir, new_name)

            if self.renumber_var.get():
                counter += 1

            try:
                os.rename(src, dst)
            except Exception as err:
                print(f"Error renaming {f} -> {new_name}: {err}")
        messagebox.showinfo("Done", "Files renamed successfully.")

def main():
    """Application entry point (no splash, no custom icon)."""
    root = tk.Tk()
    # Center the main window roughly on screen
    try:
        width, height = 640, 780
        screen_w = root.winfo_screenwidth()
        screen_h = root.winfo_screenheight()
        x = (screen_w - width) // 2
        y = (screen_h - height) // 2
        root.geometry(f"{width}x{height}+{x}+{y}")
    except Exception:
        # Fallback: just set a default size
        root.geometry("640x780")
    FileRenamerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
