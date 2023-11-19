# game-automation-bot

Python bot game automation

For that to work, you need to have installed Python (used version 3.12.0 for that project): https://www.python.org/downloads/release/python-3120/

In windows, you will have to install the tesseract to bot work properly, and install it in the path `C:\Program Files\Tesseract-OCR\tesseract.exe`

The file for installation is located at tesseract folder.

To work on code and start the bot, create a virtual environment:

```sh
python -m venv venv
```

Then, activate your virtual environment:

```py
.\venv\Scripts\activate
```

The dependencies are specified on `requirements.txt`.
To install the depencies, go to the project folder and use:

```sh
pip install -r requirements.txt
```

That file does not update automatically, so if you chance something (add, update or remove dependencies), need to run that command to update the file:

```sh
pip freeze > requirements.txt
```

them, run the code:

```sh
python launcher.py
```

To end bot, use ´CTRL + C´ and desactivate the virtual environment:

```sh
deactivate
```

---

To build the application

Navigate to Your Script's Directory:
Open the command prompt and navigate to the directory containing your Python script (`launcher.py`).

Create the Executable:
Run the following command to create the executable:

```sh
pyinstaller --onefile --add-data "icon.ico;." --add-data "../images;images" launcher.py
```

This command will create a dist folder in your script's directory, containing the executable file (`launcher.exe`).

Find the Executable:
Navigate to the dist folder, and you'll find your executable (`bot.exe`).
