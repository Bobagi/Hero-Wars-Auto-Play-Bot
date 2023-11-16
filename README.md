# game-automation-bot

Python bot game automation

The dependencies are specified on requirements.txt.

In windows, you will have to install the tesseract to bot work properly, and install it in the path 'C:\Program Files\Tesseract-OCR\tesseract.exe'

The file for installation is located at tesseract folder.

To work on code and start the bot, create a virtual environment:

```sh
python -m venv venv
```

Then, activate your virtual environment:

```sh
.\venv\Scripts\activate
```

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
python bot.py
```

To end bot, use ´CTRL + C´ and desactivate the virtual environment:

```sh
deactivate
```

---

To build the application

Navigate to Your Script's Directory:
Open the command prompt and navigate to the directory containing your Python script (`bot.py`).

Create the Executable:
Run the following command to create the executable:

```sh
pyinstaller --onefile bot.py
```

This command will create a dist folder in your script's directory, containing the executable file (`bot.exe`).

Find the Executable:
Navigate to the dist folder, and you'll find your executable (`bot.exe`).
