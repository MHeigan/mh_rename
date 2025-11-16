import os
import re
import tkinter as tk
from tkinter import filedialog, messagebox, PhotoImage

class FileRenamerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("mh_tools - File Sequence Renamer")
        self.root.geometry("640x720")

        # Input Directory selection
        self.input_dir_label = tk.Label(root, text="No input directory selected")
        self.input_dir_label.pack(pady=5)
        self.select_input_button = tk.Button(root, text="Select Input Directory", command=self.select_input_directory, bg="light grey")
        self.select_input_button.pack(pady=5)

        # Output Directory selection
        self.output_dir_label = tk.Label(root, text="No output directory selected (will use input)")
        self.output_dir_label.pack(pady=5)
        self.select_output_button = tk.Button(root, text="Select Output Directory (Optional)", command=self.select_output_directory, bg="light grey")
        self.select_output_button.pack(pady=5)

        # Feature toggles
        self.replace_var = tk.BooleanVar()
        self.renumber_var = tk.BooleanVar()
        self.padding_var = tk.BooleanVar()
        self.ext_var = tk.BooleanVar()

        # Replace Section
        replace_frame = tk.LabelFrame(root, text="Replace Section", padx=10, pady=10)
        replace_frame.pack(fill="x", padx=10, pady=5)
        tk.Checkbutton(replace_frame, text="Enable", variable=self.replace_var).pack(anchor="w")
        tk.Label(replace_frame, text="Text to replace:").pack(anchor="w")
        self.replace_from_entry = tk.Entry(replace_frame)
        self.replace_from_entry.pack(fill="x")
        tk.Label(replace_frame, text="Replace text with:").pack(anchor="w")
        self.replace_to_entry = tk.Entry(replace_frame)
        self.replace_to_entry.pack(fill="x")

        # Renumber Section
        renumber_frame = tk.LabelFrame(root, text="Renumber Sequence", padx=10, pady=10)
        renumber_frame.pack(fill="x", padx=10, pady=5)
        tk.Checkbutton(renumber_frame, text="Enable", variable=self.renumber_var).pack(anchor="w")
        tk.Label(renumber_frame, text="Start number:").pack(anchor="w")
        self.start_entry = tk.Entry(renumber_frame)
        self.start_entry.pack(fill="x")
        self.start_entry.insert(0, "1001")

        # Padding Section
        padding_frame = tk.LabelFrame(root, text="Change Padding", padx=10, pady=10)
        padding_frame.pack(fill="x", padx=10, pady=5)
        tk.Checkbutton(padding_frame, text="Enable", variable=self.padding_var).pack(anchor="w")
        tk.Label(padding_frame, text="Padding:").pack(anchor="w")
        self.padding_entry = tk.Entry(padding_frame)
        self.padding_entry.pack(fill="x")
        self.padding_entry.insert(0, "4")

        # Extension Section
        ext_frame = tk.LabelFrame(root, text="Change Extension", padx=10, pady=10)
        ext_frame.pack(fill="x", padx=10, pady=5)
        tk.Checkbutton(ext_frame, text="Enable", variable=self.ext_var).pack(anchor="w")
        tk.Label(ext_frame, text="New extension:").pack(anchor="w")
        self.ext_entry = tk.Entry(ext_frame)
        self.ext_entry.pack(fill="x")

        # Run button
        self.rename_button = tk.Button(root, text="Rename Files", command=self.rename_files, bg="light grey")
        self.rename_button.pack(pady=20)

        # Internal variables
        self.input_dir = ""
        self.output_dir = ""

    def select_input_directory(self):
        self.input_dir = filedialog.askdirectory()
        if self.input_dir:
            self.input_dir_label.config(text=self.input_dir)

    def select_output_directory(self):
        self.output_dir = filedialog.askdirectory()
        if self.output_dir:
            self.output_dir_label.config(text=self.output_dir)

    def rename_files(self):
        input_dir = self.input_dir
        output_dir = self.output_dir if self.output_dir else self.input_dir

        if not input_dir or not os.path.isdir(input_dir):
            messagebox.showerror("Error", "Please select a valid input directory.")
            return

        files = sorted(os.listdir(input_dir))
        start_number = int(self.start_entry.get()) if self.renumber_var.get() else None
        padding = int(self.padding_entry.get()) if self.padding_var.get() else 4
        new_ext = self.ext_entry.get().lstrip('.') if self.ext_var.get() and self.ext_entry.get() else None

        counter = start_number if start_number is not None else 0

        for filename in files:
            name, ext = os.path.splitext(filename)
            new_name = name

            # Apply text replacement
            if self.replace_var.get():
                new_name = new_name.replace(self.replace_from_entry.get(), self.replace_to_entry.get())

            # Remove existing numbering if renumbering
            if self.renumber_var.get():
                new_name = re.sub(r'[\._](\d{3,5})$', '', new_name)  # remove .1001 or _1001 etc.
                number = f"{counter:0{padding}d}"
                new_name = f"{new_name}.{number}"
                counter += 1

            # Change extension
            if new_ext:
                ext = f".{new_ext}"

            new_filename = new_name + ext
            src = os.path.join(input_dir, filename)
            dst = os.path.join(output_dir, new_filename)

            try:
                os.rename(src, dst)
            except Exception as e:
                print(f"Failed to rename {filename} -> {new_filename}: {e}")

        messagebox.showinfo("Done", "Files renamed successfully.")

# Splash screen setup
def create_splash_window(root):
    splash = tk.Toplevel(root)
    splash.geometry("640x480")
    splash.overrideredirect(True)
    splash.configure(bg="black")

    splash_image = PhotoImage(file="_internal/splash.png")
    splash_label = tk.Label(splash, image=splash_image)
    splash_label.image = splash_image
    splash_label.pack(fill="both", expand=True)

    splash.update_idletasks()
    w, h = 640, 480
    x = (splash.winfo_screenwidth() // 2) - (w // 2)
    y = (splash.winfo_screenheight() // 2) - (h // 2)
    splash.geometry(f"{w}x{h}+{x}+{y}")

    root.after(2000, lambda: fade_out_and_show_gui(root, splash))

def fade_out_and_show_gui(root, splash):
    try:
        splash.withdraw()
        root.deiconify()
        root.attributes("-alpha", 0.0)

        # Center main GUI window
        w, h = 640, 720
        x = (root.winfo_screenwidth() // 2) - (w // 2)
        y = (root.winfo_screenheight() // 2) - (h // 2)
        root.geometry(f"{w}x{h}+{x}+{y}")

        fade_in(root, 0.0)

    except Exception as e:
        print(f"Error during splash cleanup or GUI init: {e}")

def fade_in(window, alpha):
    if alpha < 1.0:
        alpha = min(alpha + 0.1, 1.0)
        window.attributes("-alpha", alpha)
        window.after(30, lambda: fade_in(window, alpha))
    else:
        window.attributes("-alpha", 1.0)

def main():
    root = tk.Tk()
    root.withdraw()
    create_splash_window(root)
    FileRenamerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
