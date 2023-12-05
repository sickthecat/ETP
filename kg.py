import tkinter as tk
from pygame import mixer
import ctypes
import sys
import os

# Function to get the path of data files (works for both development and bundled app)
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Function to hide the console window on Windows
def hide_console():
    if sys.platform.startswith('win'):
        ctypes.windll.kernel32.FreeConsole()

# Hide the console window
hide_console()

# Function to calculate the registration key
def calculate_registration_key(imei):
    x = -1
    key = 0

    for i in range(10):
        if x < 4:
            x = x + 1
        else:
            x = len(imei) + i - 10
        n = ord(imei[x]) & 0xFF
        key += (((49635 * n & 0xFFFF) >> 1) - n & 0xFFFF) & 0xFFFF

    return 0xFFFF & key

# Function to generate the key based on IMEI
def generate_key():
    imei = imei_entry.get()
    if len(imei) < 15 or len(imei) > 16:
        key_entry.config(state='normal')
        key_entry.delete(0, tk.END)
        key_entry.insert(0, "Invalid IMEI length")
        key_entry.config(state='readonly')
    else:
        key = calculate_registration_key(imei)
        key_entry.config(state='normal')
        key_entry.delete(0, tk.END)
        key_entry.insert(0, f"{key:05d}")
        key_entry.config(state='readonly')

# Function to display the About window
def show_about():
    about_window = tk.Toplevel(root)
    about_window.title("About")
    about_window.geometry("300x100")  # Adjust the size as needed
    about_text = ("Keygen by: _SiCk\n"
                  "Protection: Basic math?\n"
                  "Music by: Dubmood and JoSss - Starship")
    tk.Label(about_window, text=about_text, justify=tk.LEFT).pack(padx=10, pady=10)

# Initialize Pygame for audio
mixer.init()
mixer.music.load(resource_path('crack.xm'))  # Use resource_path to locate the file
mixer.music.play(-1)

# Set up the GUI
root = tk.Tk()
root.title("EasyTether Pro Keygen")
root.geometry("400x500")  # Adjust the window size here

# Logo
logo_image = tk.PhotoImage(file=resource_path('logo.png'))  # Use resource_path to locate the file
logo_label = tk.Label(root, image=logo_image)
logo_label.pack()

# IMEI Entry
tk.Label(root, text="Enter IMEI (15-16 chars):").pack()
imei_entry = tk.Entry(root, width=40)  # Increase width
imei_entry.pack()

# Generate Button
generate_button = tk.Button(root, text="Generate", command=generate_key)
generate_button.pack()

# Key Display as a copyable Entry
key_entry = tk.Entry(root, width=40, readonlybackground='white', fg='black', state='readonly')  # Increase width
key_entry.pack()

# About Button
about_button = tk.Button(root, text="About", command=show_about)
about_button.pack()

root.mainloop()
