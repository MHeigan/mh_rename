# mh_rename - CGI Renaming Script by Martin P Heigan (v2.0 - March 2025).
# https://anti-matter-3d.com

import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox
import re

class FileRenamerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("mh_tools - File Sequence Renamer")
        self.root.geometry("640x720")

        # Input Directory selection
        self.input_dir_label = tk.Label(root, text="No input directory selected")
        self.input_dir_label.pack(pady=5)
        tk.Button(root, text="Select Input Directory", command=self.select_input_directory).pack(pady=5)

        # Output Directory selection
        self.output_dir_label = tk.Label(root, text="No output directory selected (will use input)")
        self.output_dir_label.pack(pady=5)
        tk.Button(root, text="Select Output Directory (Optional)", command=self.select_output_directory).pack(pady=5)

        # Feature toggles
        self.replace_var = tk.BooleanVar()
        self.renumber_var = tk.BooleanVar()
        self.padding_var = tk.BooleanVar()
        self.ext_var = tk.BooleanVar()

        # Replace Section Frame
        replace_frame = tk.LabelFrame(root, text="Replace Section", padx=10, pady=10)
        replace_frame.pack(fill="x", padx=10, pady=5)
        tk.Checkbutton(replace_frame, text="Enable", variable=self.replace_var).pack(anchor="w")
        tk.Label(replace_frame, text="Text to replace:").pack(anchor="w")
        self.replace_from_entry = tk.Entry(replace_frame)
        self.replace_from_entry.pack(fill="x")
        tk.Label(replace_frame, text="Replace text with:").pack(anchor="w")
        self.replace_to_entry = tk.Entry(replace_frame)
        self.replace_to_entry.pack(fill="x")

        # Renumber Frame
        renumber_frame = tk.LabelFrame(root, text="Renumber Sequence", padx=10, pady=10)
        renumber_frame.pack(fill="x", padx=10, pady=5)
        tk.Checkbutton(renumber_frame, text="Enable", variable=self.renumber_var).pack(anchor="w")
        tk.Label(renumber_frame, text="Start number:").pack(anchor="w")
        self.start_entry = tk.Entry(renumber_frame)
        self.start_entry.pack(fill="x")
        self.start_entry.insert(0, "1001")

        # Padding Frame
        padding_frame = tk.LabelFrame(root, text="Change Padding", padx=10, pady=10)
        padding_frame.pack(fill="x", padx=10, pady=5)
        tk.Checkbutton(padding_frame, text="Enable", variable=self.padding_var).pack(anchor="w")
        tk.Label(padding_frame, text="Padding:").pack(anchor="w")
        self.padding_entry = tk.Entry(padding_frame)
        self.padding_entry.pack(fill="x")
        self.padding_entry.insert(0, "4")

        # Extension Frame
        ext_frame = tk.LabelFrame(root, text="Change Extension", padx=10, pady=10)
        ext_frame.pack(fill="x", padx=10, pady=5)
        tk.Checkbutton(ext_frame, text="Enable", variable=self.ext_var).pack(anchor="w")
        tk.Label(ext_frame, text="New extension:").pack(anchor="w")
        self.ext_entry = tk.Entry(ext_frame)
        self.ext_entry.pack(fill="x")

        # Run button
        tk.Button(root, text="Rename Files", command=self.rename_files).pack(pady=20)

        self.input_directory = ""
        self.output_directory = ""

    def select_input_directory(self):
        self.input_directory = filedialog.askdirectory()
        if self.input_directory:
            self.input_dir_label.config(text=f"Input: {self.input_directory}")

    def select_output_directory(self):
        self.output_directory = filedialog.askdirectory()
        if self.output_directory:
            self.output_dir_label.config(text=f"Output: {self.output_directory}")
        else:
            self.output_dir_label.config(text="No output directory selected (will use input)")

    def rename_files(self):
        if not self.input_directory:
            messagebox.showerror("Error", "Please select an input directory first!")
            return

        target_dir = self.output_directory if self.output_directory else self.input_directory

        try:
            # Ensure output directory exists
            if self.output_directory and not os.path.exists(self.output_directory):
                os.makedirs(self.output_directory)

            files = [f for f in os.listdir(self.input_directory) if os.path.isfile(os.path.join(self.input_directory, f))]
            files.sort()  # Ensure consistent ordering

            # Process files
            counter = int(self.start_entry.get()) if self.renumber_var.get() else None
            padding = int(self.padding_entry.get()) if self.padding_var.get() and self.padding_entry.get() else 4

            for filename in files:
                old_name = filename
                new_name = filename
                base, ext = os.path.splitext(filename)

                # Find number in filename if it exists
                num_match = re.search(r'(\d+)', base)
                num_part = num_match.group(1) if num_match else ""
                num_start = num_match.start() if num_match else len(base)
                prefix = base[:num_start] if num_match else base
                suffix = base[num_start + len(num_part):] if num_match else ""

                # Replace section
                if self.replace_var.get() and self.replace_from_entry.get():
                    new_name = new_name.replace(self.replace_from_entry.get(), self.replace_to_entry.get())
                    prefix = prefix.replace(self.replace_from_entry.get(), self.replace_to_entry.get())
                    suffix = suffix.replace(self.replace_from_entry.get(), self.replace_to_entry.get())

                # Renumber
                if self.renumber_var.get() and counter is not None:
                    new_num = str(counter).zfill(padding)
                    if num_match:
                        new_name = f"{prefix}{new_num}{suffix}{ext}"
                    else:
                        new_name = f"{prefix}{new_num}{ext}"
                    counter += 1
                # Change padding only
                elif self.padding_var.get() and num_match:
                    new_num = num_part.zfill(padding)
                    new_name = f"{prefix}{new_num}{suffix}{ext}"

                # Change extension
                if self.ext_var.get() and self.ext_entry.get():
                    new_name = os.path.splitext(new_name)[0] + self.ext_entry.get()

                # Perform rename or copy
                if new_name != old_name:
                    if self.output_directory:
                        shutil.copy2(
                            os.path.join(self.input_directory, old_name),
                            os.path.join(self.output_directory, new_name)
                        )
                    else:
                        os.rename(
                            os.path.join(self.input_directory, old_name),
                            os.path.join(self.input_directory, new_name)
                        )

            messagebox.showinfo("Success", "Files renamed successfully!")
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

def main():
    root = tk.Tk()
    app = FileRenamerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()