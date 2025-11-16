import os
import re
import tkinter as tk
from tkinter import filedialog, messagebox, PhotoImage

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

        # Feature control sections
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
            text="No output directory selected (will use input)"
        )
        self.output_dir_label.pack(pady=5)
        tk.Button(
            self.container,
            text="Select Output Directory (Optional)",
            command=self.select_output_directory,
            bg="light grey"
        ).pack(pady=5)

    def setup_replace_section(self):
        """Create controls for replacing text in filenames."""
        self.replace_var = tk.BooleanVar()
        replace_frame = tk.LabelFrame(
            self.container,
            text="Replace Section",
            padx=10,
            pady=10
        )
        replace_frame.pack(fill="x", padx=10, pady=5)
        tk.Checkbutton(
            replace_frame,
            text="Enable",
            variable=self.replace_var
        ).pack(anchor="w")
        tk.Label(replace_frame, text="Text to replace:").pack(anchor="w")
        self.replace_from_entry = tk.Entry(replace_frame)
        self.replace_from_entry.pack(fill="x")
        tk.Label(replace_frame, text="Replace with:").pack(anchor="w")
        self.replace_to_entry = tk.Entry(replace_frame)
        self.replace_to_entry.pack(fill="x")

    def setup_renumber_section(self):
        """Create controls for renumbering sequence."""
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
        tk.Label(renumber_frame, text="Start number:").pack(anchor="w")
        self.start_entry = tk.Entry(renumber_frame)
        self.start_entry.pack(fill="x")
        self.start_entry.insert(0, "1001")

    def setup_padding_section(self):
        """Create controls for changing padding."""
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
        self.padding_entry.pack(fill="x")
        self.padding_entry.insert(0, "4")

    def setup_extension_section(self):
        """Create controls for changing file extension."""
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
        tk.Label(ext_frame, text="New extension:").pack(anchor="w")
        self.ext_entry = tk.Entry(ext_frame)
        self.ext_entry.pack(fill="x")

    def setup_action_buttons(self):
        """Add Preview and Rename buttons."""
        btn_frame = tk.Frame(self.container)
        btn_frame.pack(pady=10)
        self.preview_button = tk.Button(
            btn_frame,
            text="Preview Rename",
            command=self.preview_files,
            bg="light grey"
        )
        self.preview_button.pack(side="left", padx=5)
        self.rename_button = tk.Button(
            btn_frame,
            text="Rename Files",
            command=self.rename_files,
            bg="light grey"
        )
        self.rename_button.pack(side="left", padx=5)

    def select_input_directory(self):
        """Handler for browsing input directory."""
        self.input_dir = filedialog.askdirectory()
        if self.input_dir:
            self.input_dir_label.config(text=self.input_dir)

    def select_output_directory(self):
        """Handler for browsing output directory."""
        self.output_dir = filedialog.askdirectory()
        if self.output_dir:
            self.output_dir_label.config(text=self.output_dir)

    def compute_new_name(self, filename, counter=None, padding=4, new_ext=None):
        """
        Given an original filename, apply replace, renumber, and extension
        rules to compute the new filename.
        """
        name, ext = os.path.splitext(filename)
        new_name = name
        # Replace text
        if self.replace_var.get():
            new_name = new_name.replace(
                self.replace_from_entry.get(),
                self.replace_to_entry.get()
            )
        # Renumber
        if self.renumber_var.get() and counter is not None:
            new_name = re.sub(r'[\._](\d{3,5})$', '', new_name)
            number = f"{counter:0{padding}d}"
            new_name = f"{new_name}.{number}"
        # Extension change
        ext = f".{new_ext}" if new_ext else ext
        return new_name + ext

    def preview_files(self):
        """
        Show a pop-up preview window with original → new filenames.
        """
        input_dir = self.input_dir
        if not input_dir or not os.path.isdir(input_dir):
            messagebox.showerror("Error", "Please select a valid input directory.")
            return
        files = sorted(os.listdir(input_dir))
        start_number = int(self.start_entry.get()) if self.renumber_var.get() else None
        padding = int(self.padding_entry.get()) if self.padding_var.get() else 4
        new_ext = self.ext_entry.get().lstrip('.') if self.ext_var.get() else None
        # Create preview window
        preview = tk.Toplevel(self.root)
        preview.title("Preview Renames")
        preview.geometry("600x400")
        # Text widget with scrollbars
        text = tk.Text(preview, wrap="none")
        text.pack(fill="both", expand=True)
        ys = tk.Scrollbar(preview, orient="vertical", command=text.yview)
        ys.pack(side="right", fill="y")
        xs = tk.Scrollbar(preview, orient="horizontal", command=text.xview)
        xs.pack(side="bottom", fill="x")
        text.configure(yscrollcommand=ys.set, xscrollcommand=xs.set)
        # Populate preview
        counter = start_number or 0
        for f in files:
            new_name = self.compute_new_name(f, counter, padding, new_ext)
            if self.renumber_var.get():
                counter += 1
            text.insert("end", f"{f} → {new_name}\n")
        text.config(state="disabled")

    def rename_files(self):
        """
        Perform the actual renaming on disk according to current rules.
        """
        input_dir = self.input_dir
        output_dir = self.output_dir or input_dir
        if not os.path.isdir(input_dir):
            messagebox.showerror("Error", "Please select a valid input directory.")
            return
        files = sorted(os.listdir(input_dir))
        start = int(self.start_entry.get()) if self.renumber_var.get() else None
        pad = int(self.padding_entry.get()) if self.padding_var.get() else 4
        ext = self.ext_entry.get().lstrip('.') if self.ext_var.get() else None
        counter = start or 0
        for f in files:
            src = os.path.join(input_dir, f)
            new_name = self.compute_new_name(f, counter, pad, ext)
            if self.renumber_var.get():
                counter += 1
            dst = os.path.join(output_dir, new_name)
            try:
                os.rename(src, dst)
            except Exception as err:
                print(f"Error renaming {f} -> {new_name}: {err}")
        messagebox.showinfo("Done", "Files renamed successfully.")

# Splash screen functions

def create_splash_window(root):
    """Display splash screen before main GUI."""
    splash = tk.Toplevel(root)
    splash.overrideredirect(True)
    splash.geometry("640x640")
    splash.configure(bg="black")
    try:
        img = PhotoImage(file="_internal/splash.png")
        lbl = tk.Label(splash, image=img)
        lbl.image = img
        lbl.pack(fill="both", expand=True)
    except Exception:
        pass
    # Center splash
    w, h = 640, 640
    x = (root.winfo_screenwidth() - w) // 2
    y = (root.winfo_screenheight() - h) // 2
    splash.geometry(f"{w}x{h}+{x}+{y}")
    root.after(2000, lambda: fade_out_and_show_gui(root, splash))

def fade_out_and_show_gui(root, splash):
    """Fade splash out and show main window."""
    try:
        splash.withdraw()
        root.deiconify()
        root.attributes("-alpha", 0.0)
        # Center main window
        w, h = 640, 780
        x = (root.winfo_screenwidth() - w) // 2
        y = (root.winfo_screenheight() - h) // 2
        root.geometry(f"{w}x{h}+{x}+{y}")
        fade_in(root, 0.0)
    except Exception as e:
        print(f"Splash cleanup error: {e}")

def fade_in(win, alpha):
    """Recursive fade-in effect for main window."""
    if alpha < 1.0:
        alpha += 0.1
        win.attributes("-alpha", alpha)
        win.after(30, lambda: fade_in(win, alpha))
    else:
        win.attributes("-alpha", 1.0)

def main():
    """Application entry point."""
    root = tk.Tk()
    root.withdraw()
    create_splash_window(root)
    FileRenamerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
