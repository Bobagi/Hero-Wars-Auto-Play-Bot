import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk  # You may need to install the Pillow library: pip install Pillow
import os
from tower import main as mainTower

class HeroWarsBot:
    def __init__(self, root):
        self.root = root
        self.root.title("Hero Wars Time Saver edition")

        # Set the background color to blue
        self.root.configure(bg='black')  # Use your preferred shade of blue, this is a common one

        # Set the minimum height and minimum width
        self.root.minsize(width=400, height=300)  # Adjust the values to your preferred minimum size

        # Set the window icon
        icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'icon.ico')
        self.root.iconbitmap(icon_path)

        # Add a cool text with the name of your bot
        title_label = tk.Label(self.root, text="Choose game module", font=("Helvetica", 32, "bold italic"), bg='black', fg='yellow')
        title_label.pack(pady=10)

        self.create_widgets()

    def create_widgets(self):
        # Create labels, buttons, and other UI elements
        self.label = tk.Label(self.root, text="Hero Wars", font=("Helvetica", 16, "bold italic"), bg='black', fg='yellow')
        self.label.pack(pady=10)

        frame_buttons = tk.Frame(self.root, bg='#000000')  # Create a frame to hold the buttons
        frame_buttons.pack()

        self.browse_button = tk.Button(frame_buttons, text="Tower", font=("Helvetica", 12, "bold italic"), bg='yellow', fg='black', command=self.browse_tower_script)
        self.browse_button.pack(side=tk.LEFT, padx=10, pady=10)

        # self.search_button = tk.Button(frame_buttons, text="Search Image", font=("Helvetica", 12, "bold italic"), bg='yellow', fg='black', command=self.browse_image)
        # self.search_button.pack(side=tk.LEFT, padx=10, pady=10)

        # Add a label for "by Bobagi"
        self.by_label = tk.Label(self.root, text="by Bobagi", font=("Helvetica", 10), bg='black', fg='yellow')
        self.by_label.pack(side=tk.RIGHT, padx=10, pady=10, anchor='se')  # Pack it to the right bottom corner


    def browse_tower_script(self):
        mainTower()

    def browse_image(self):
        # Open a file dialog to choose the screenshot
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])

        # Display the selected image
        if file_path:
            image = Image.open(file_path)
            image.thumbnail((300, 300))
            photo = ImageTk.PhotoImage(image)

            self.label.config(text="Selected screenshot:")
            self.image_label = tk.Label(self.root, image=photo)
            self.image_label.image = photo
            self.image_label.pack(pady=10)

            # Store the file path for later use
            self.file_path = file_path

if __name__ == "__main__":
    root = tk.Tk()
    app = HeroWarsBot(root)
    root.mainloop()
