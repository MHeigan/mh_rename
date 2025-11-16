import tkinter as tk
from tkinter import PhotoImage

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

        # Feature toggles (example, continue with your original layout)
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

        # Renumber Section Frame
        renumber_frame = tk.LabelFrame(root, text="Renumber Sequence", padx=10, pady=10)
        renumber_frame.pack(fill="x", padx=10, pady=5)
        tk.Checkbutton(renumber_frame, text="Enable", variable=self.renumber_var).pack(anchor="w")
        tk.Label(renumber_frame, text="Start number:").pack(anchor="w")
        self.start_entry = tk.Entry(renumber_frame)
        self.start_entry.pack(fill="x")
        self.start_entry.insert(0, "1001")

        # Padding Section Frame
        padding_frame = tk.LabelFrame(root, text="Change Padding", padx=10, pady=10)
        padding_frame.pack(fill="x", padx=10, pady=5)
        tk.Checkbutton(padding_frame, text="Enable", variable=self.padding_var).pack(anchor="w")
        tk.Label(padding_frame, text="Padding:").pack(anchor="w")
        self.padding_entry = tk.Entry(padding_frame)
        self.padding_entry.pack(fill="x")
        self.padding_entry.insert(0, "4")

        # Extension Section Frame
        ext_frame = tk.LabelFrame(root, text="Change Extension", padx=10, pady=10)
        ext_frame.pack(fill="x", padx=10, pady=5)
        tk.Checkbutton(ext_frame, text="Enable", variable=self.ext_var).pack(anchor="w")
        tk.Label(ext_frame, text="New extension:").pack(anchor="w")
        self.ext_entry = tk.Entry(ext_frame)
        self.ext_entry.pack(fill="x")

        # Run button
        self.rename_button = tk.Button(root, text="Rename Files", command=self.rename_files, bg="light grey")
        self.rename_button.pack(pady=20)

    def select_input_directory(self):
        pass  # Placeholder

    def select_output_directory(self):
        pass  # Placeholder

    def rename_files(self):
        pass  # Placeholder


def create_splash_window(root):
    splash = tk.Toplevel(root)
    splash.geometry("640x480")  # Same size as the main window
    splash.overrideredirect(True)  # Remove window decorations (close/minimize)
    splash.configure(bg="black")

    # Load splash image
    splash_image = PhotoImage(file="_internal/splash.png")
    splash_label = tk.Label(splash, image=splash_image)
    splash_label.image = splash_image  # Keep a reference to the image
    splash_label.pack(fill="both", expand=True)

    # Center the splash screen
    splash_width = 640
    splash_height = 480
    screen_width = splash.winfo_screenwidth()
    screen_height = splash.winfo_screenheight()
    position_top = int(screen_height / 2 - splash_height / 2)
    position_right = int(screen_width / 2 - splash_width / 2)
    splash.geometry(f'{splash_width}x{splash_height}+{position_right}+{position_top}')

    # Wait for 2 seconds, then fade out and show the main window
    splash.after(2000, lambda: fade_out_and_show_gui(splash, root))


def fade_out_and_show_gui(splash, root):
    # Debugging print statement
    print("Splash screen has been closed, fading in main window...")

    splash.destroy()  # Close the splash screen

    # Ensure that widgets are packed and initialized before fading in
    root.deiconify()  # Unhide the root window after splash

    root.update_idletasks()  # Update window tasks before fade-in

    # Start fade-in effect
    fade_in(root, 0)


def fade_in(window, alpha):
    if alpha < 1.0:
        alpha += 0.05
        window.attributes("-alpha", alpha)  # Set window opacity
        window.after(50, lambda: fade_in(window, alpha))  # Continue fade-in


def main():
    root = tk.Tk()
    root.withdraw()  # Hide the root window initially (show only splash)

    # Show splash screen and then main window
    create_splash_window(root)

    # Initialize and show the main window (GUI)
    print("Main window is being initialized...")
    gui_app = FileRenamerGUI(root)

    # Start the Tkinter main loop
    root.mainloop()


if __name__ == "__main__":
    main()
