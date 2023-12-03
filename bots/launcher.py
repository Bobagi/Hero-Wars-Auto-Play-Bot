import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk  # You may need to install the Pillow library: pip install Pillow
import os
from tower import main as mainTower
from dungeon import main as mainDungeon
from config import *
from imageFind import *

default_path = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
tesseract = False

class HeroWarsBot:
    def __init__(self, root):
        self.root = root
        self.root.title("Hero Wars Time Saver edition")

        # Set the background color to blue
        self.root.configure(bg='black')  # Use your preferred shade of blue, this is a common one

        self.root.minsize(width=600, height=300)  # Adjust the values to your preferred minimum size
        self.root.maxsize(width=600, height=300)  # Adjust the values to your preferred maximum size

        # Set the window icon
        icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'icon.ico')
        self.root.iconbitmap(icon_path)

        # Add a cool text with the name of your bot
        title_label = tk.Label(self.root, text="Choose game module", font=("Helvetica", 32, "bold italic"), bg='black', fg='yellow')
        title_label.pack(pady=10)

        self.create_widgets()

        if os.path.isfile(default_path):
            self.icon_label.config(image=self.green_check_image)
            self.file_path = default_path
            global tesseract
            tesseract = True
            setTesseractPath(default_path)
        else:
            self.icon_label.config(image=self.red_cross_image)

        self.icon_label.pack()  # Make the icon visible using pack

    def create_widgets(self):
        images = find_image_paths('launcher')
       
        # Create labels, buttons, and other UI elements
        self.label = tk.Label(self.root, text="Hero Wars", font=("Helvetica", 16, "bold italic"), bg='black', fg='yellow')
        self.label.pack(pady=10)

        frame_tesseract = tk.Frame(self.root, bg='#000000')  # Create a frame to hold the buttons
        frame_tesseract.pack()

        # Create a label for the path textbox
        path_label = tk.Label(frame_tesseract, text="Tesseract Path:", font=("Helvetica", 12), bg='black', fg='yellow')
        path_label.pack(side=tk.LEFT, padx=10)

        # Set the default path
        global default_path
        self.path_var = tk.StringVar(value=default_path)

        # Create the path textbox
        self.path_entry = tk.Entry(frame_tesseract, textvariable=self.path_var, width=40)
        self.path_entry.pack(side=tk.LEFT, padx=0)

        # Create the Search button
        self.search_button = tk.Button(frame_tesseract, text="Search", font=("Helvetica", 12, "bold italic"), bg='yellow', fg='black', command=self.browse_tesseract)
        self.search_button.pack(side=tk.LEFT, padx=10)

        # Placeholder images for green check and red cross icons
        self.green_check_image = tk.PhotoImage(file=images["check"])
        self.red_cross_image = tk.PhotoImage(file=images["xcross"])

        # Create an icon label (initially invisible)
        self.icon_label = tk.Label(frame_tesseract, image=None, bg='black')
        self.icon_label.pack()
        self.icon_label.pack_forget()  # Make the icon initially invisible

        frame_buttons = tk.Frame(self.root, bg='#222021')  # Create a frame to hold the buttons
        frame_buttons.pack()

        self.browse_button = tk.Button(frame_buttons, text="Tower", font=("Helvetica", 12, "bold italic"), bg='yellow', fg='black', command=self.browse_tower_script)
        self.browse_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.browse_button = tk.Button(frame_buttons, text="Dungeon", font=("Helvetica", 12, "bold italic"), bg='yellow', fg='black', command=self.browse_dungeon_script)
        self.browse_button.pack(side=tk.LEFT, padx=10, pady=10)

        # Add a label for "by Bobagi"
        self.by_label = tk.Label(self.root, text="by Bobagi", font=("Helvetica", 10), bg='black', fg='yellow')
        self.by_label.pack(side=tk.RIGHT, padx=10, pady=10, anchor='se')  # Pack it to the right bottom corner

    def browse_tower_script(self):
        mainTower()

    def browse_dungeon_script(self):
        mainDungeon()

    def browse_tesseract(self):
        # Open a file dialog to choose the executable file
        file_path = filedialog.askopenfilename(filetypes=[("Executable files", "*.exe")])

        # Display the selected path
        if file_path:
            self.path_var.set(file_path)

            # Update the icon based on the selected file
            if "tesseract.exe" in file_path.lower():
                self.icon_label.config(image=self.green_check_image)
                global tesseract
                tesseract = True
            else:
                self.icon_label.config(image=self.red_cross_image)

            self.icon_label.pack()  # Make the icon visible using pack

            # Store the file path for later use
            self.file_path = file_path
            setTesseractPath(file_path)

if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = HeroWarsBot(root)
        root.mainloop()
    except Exception as e:
        print(f"An error occurred: {e}")
        input("Press Enter to exit...")