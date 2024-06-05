import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import os
import ctypes


# Function to maximize the console window on the left side
def maximize_console_left():
    hwnd = ctypes.windll.kernel32.GetConsoleWindow()
    if hwnd:
        user32 = ctypes.windll.user32
        screen_width = user32.GetSystemMetrics(0)
        screen_height = user32.GetSystemMetrics(1)
        left_width = screen_width // 2
        user32.MoveWindow(hwnd, 0, 0, left_width, screen_height, True)

# Function to center a window on the screen
def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    window.geometry(f'{width}x{height}+{x}+{y}')

# Function to run the auto extract command
def auto_extract():
    if installer_path.get():
        normalized_path = os.path.normpath(installer_path.get())
        command = f'innoextract.exe "{normalized_path}"'
        print(f"Running command: {command}")  # Debug print
        subprocess.run(command, shell=True)
    else:
        messagebox.showwarning("No Installer Selected", "Please select an installer file.")

# Function to open the advanced extract window
def advanced_extract():
    if installer_path.get():
        AdvancedExtractWindow(installer_path.get())
    else:
        messagebox.showwarning("No Installer Selected", "Please select an installer file.")

# Function to show the About dialog
def show_about():
    messagebox.showinfo("Abouttt", "Inno Setup Extractor\nVersion 409.23\nInnoExtract by Daniel Scharrer https://constexpr.org/innoextract/ \nGUI by Whale Linguini")

# Class for the advanced extract window
class AdvancedExtractWindow:
    def __init__(self, installer_path):
        self.installer_path = installer_path
        self.adv_window = tk.Toplevel()
        self.adv_window.title("Advanced Extract")

        self.options = {
            "Generic options": ["--help", "--version", "--license"],
            "Actions": ["--test", "--extract", "--list", "--list-sizes", "--list-checksums", "--info", "--list-languages", "--gog-game-id", "--show-password", "--check-password", "--data-version"],
            "Modifiers": ["--codepage", "--collisions", "--default-language", "--dump", "--lowercase", "--timestamps", "--output-dir", "--password", "--password-file", "--gog", "--no-gog-galaxy", "--no-extract-unknown"],
            "Filters": ["--exclude-temp", "--language", "--language-only", "--include"],
            "Display options": ["--quiet", "--silent", "--no-warn-unused", "--color", "--progress"]
        }

        self.check_vars = {opt: tk.StringVar() for section in self.options.values() for opt in section}
        self.entry_vars = {opt: tk.StringVar() for opt in self.options["Modifiers"] if opt not in ["--dump", "--lowercase", "--gog", "--no-gog-galaxy", "--no-extract-unknown"]}
        self.entry_vars.update({opt: tk.StringVar() for opt in self.options["Filters"] if opt not in ["--exclude-temp", "--language-only"]})
        self.entry_vars.update({opt: tk.StringVar() for opt in self.options["Display options"] if opt in ["--color", "--progress"]})

        row = 0
        col = 0
        max_rows_per_column = 20
        total_options = sum(len(opts) for opts in self.options.values())
        num_columns = (total_options // max_rows_per_column) + 1

        for section, opts in self.options.items():
            tk.Label(self.adv_window, text=section, font=('Arial', 10, 'bold')).grid(row=row, column=col, sticky='w', padx=10, pady=(10, 0))
            row += 1
            for opt in opts:
                if opt in self.entry_vars:
                    tk.Label(self.adv_window, text=opt).grid(row=row, column=col, sticky='w', padx=10)
                    tk.Entry(self.adv_window, textvariable=self.entry_vars[opt]).grid(row=row, column=col + 1, sticky='w', padx=10)
                else:
                    tk.Checkbutton(self.adv_window, text=opt, variable=self.check_vars[opt], onvalue=opt, offvalue='').grid(row=row, column=col, sticky='w', padx=10)
                row += 1
                if row % max_rows_per_column == 0:
                    col += 2
                    row = 1

        # Position the buttons at the bottom of the window
        button_frame = tk.Frame(self.adv_window)
        button_frame.grid(row=max_rows_per_column + 1, column=0, columnspan=num_columns * 2, pady=10, sticky='ew')
        
        tk.Button(button_frame, text="Extract", command=self.extract).pack(side=tk.LEFT, padx=(10, 5))
        tk.Button(button_frame, text="Help", command=self.show_help).pack(side=tk.LEFT, padx=(5, 5))
        tk.Button(button_frame, text="Exit", command=self.adv_window.destroy).pack(side=tk.LEFT, padx=(5, 10))

        # Center the advanced window
        self.adv_window.update_idletasks()
        center_window(self.adv_window, self.adv_window.winfo_reqwidth(), self.adv_window.winfo_reqheight())

    def extract(self):
        selected_options = [var.get() for var in self.check_vars.values() if var.get()]
        for opt, var in self.entry_vars.items():
            if var.get():
                selected_options.append(f"{opt}={var.get()}")
        normalized_path = os.path.normpath(self.installer_path)
        command = f'innoextract.exe {" ".join(selected_options)} "{normalized_path}"'
        print(f"Running command: {command}")  # Debug print
        subprocess.run(command, shell=True)
        self.adv_window.destroy()

    def show_help(self):
        help_text = (
            "Usage: ...\\...\\innoextract.exe [options] <setup file(s)>\n\n"
            "Extract files from an Inno Setup installer.\n"
            "For multi-part installers only specify the exe file.\n\n"
            "Generic options:\n"
            "  -h [ --help ]                 Show supported options\n"
            "  -v [ --version ]              Print version information\n"
            "  --license                     Show license information\n\n"
            "Actions:\n"
            "  -t [ --test ]                 Only verify checksums, don't write anything\n"
            "  -e [ --extract ]              Extract files (default action)\n"
            "  -l [ --list ]                 Only list files, don't write anything\n"
            "  --list-sizes                  List file sizes\n"
            "  --list-checksums              List file checksums\n"
            "  -i [ --info ]                 Print information about the installer\n"
            "  --list-languages              List languages supported by the installer\n"
            "  --gog-game-id                 Determine the installer's GOG.com game ID\n"
            "  --show-password               Show password check information\n"
            "  --check-password              Abort if the password is incorrect\n"
            "  -V [ --data-version ]         Only print the data version\n\n"
            "Modifiers:\n"
            "  --codepage arg                Encoding for ANSI strings\n"
            "  --collisions arg              How to handle duplicate files\n"
            "  --default-language arg        Default language for renaming\n"
            "  --dump                        Dump contents without converting filenames\n"
            "  -L [ --lowercase ]            Convert extracted filenames to lower-case\n"
            "  -T [ --timestamps ] arg       Timezone for file times or \"local\" or \"none\"\n"
            "  -d [ --output-dir ] arg       Extract files into the given directory\n"
            "  -P [ --password ] arg         Password for encrypted files\n"
            "  --password-file arg           File to load password from\n"
            "  -g [ --gog ]                  Extract additional archives from GOG.com\n"
            "                                installers\n"
            "  --no-gog-galaxy               Don't re-assemble GOG Galaxy file parts\n"
            "  -n [ --no-extract-unknown ]   Don't extract unknown Inno Setup versions\n\n"
            "Filters:\n"
            "  -m [ --exclude-temp ]         Don't extract temporary files\n"
            "  --language arg                Extract only files for this language\n"
            "  --language-only               Only extract language-specific files\n"
            "  -I [ --include ] arg          Extract only files that match this path\n\n"
            "Display options:\n"
            "  -q [ --quiet ]                Output less information\n"
            "  -s [ --silent ]               Output only error/warning information\n"
            "  --no-warn-unused              Don't warn on unused .bin files\n"
            "  -c [ --color ] [=arg(=1)]     Enable/disable color output\n"
            "  -p [ --progress ] [=arg(=1)]  Enable/disable the progress bar\n\n"
            "Extracts installers created by Inno Setup 1.2.10 to 6.0.5\n\n"
            "innoextract 1.9 (C) 2011-2020 Daniel Scharrer <daniel@constexpr.org>\n"
        )
        help_window = tk.Toplevel(self.adv_window)
        help_window.title("Help")
        help_textbox = tk.Text(help_window, wrap='word', height=30, width=100)
        help_textbox.insert('1.0', help_text)
        help_textbox.config(state='disabled')
        help_textbox.pack(padx=10, pady=10)

# Main GUI setup
root = tk.Tk()
root.title("Inno Setup Extractor - Whale Linguini")

# Create the menu bar
menubar = tk.Menu(root)
root.config(menu=menubar)

# Create the File menu
file_menu = tk.Menu(menubar, tearoff=0)
file_menu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="File", menu=file_menu)

# Create the Help menu
help_menu = tk.Menu(menubar, tearoff=0)
help_menu.add_command(label="About", command=show_about)
menubar.add_cascade(label="Help", menu=help_menu)

installer_path = tk.StringVar()

tk.Label(root, text="Select Installer:").grid(row=0, column=0, sticky='w', padx=10, pady=10)
tk.Entry(root, textvariable=installer_path, width=50).grid(row=0, column=1, sticky='w', padx=10, pady=10)
tk.Button(root, text="Browse", command=lambda: installer_path.set(filedialog.askopenfilename(initialdir=os.path.dirname(__file__)))).grid(row=0, column=2, sticky='w', padx=10, pady=10)

tk.Button(root, text="Auto Extract", command=auto_extract).grid(row=1, column=0, sticky='w', padx=10, pady=10)
tk.Button(root, text="Advanced Extract", command=advanced_extract).grid(row=1, column=1, sticky='w', padx=10, pady=10)
tk.Button(root, text="Quit", command=root.quit).grid(row=1, column=2, sticky='w', padx=10, pady=10)

# Center the main window
root.update_idletasks()
center_window(root, root.winfo_reqwidth(), root.winfo_reqheight())

# Maximize the console window on the left side
maximize_console_left()

root.mainloop()
