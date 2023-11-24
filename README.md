# Hero Wars Domination Era Bot 🤖

Python bot to auto-play Hero Wars Domination Era

---
## Prerequisites ✔️

Before using this bot, ensure you have the following installed:

- Python (version 3.12.0 used for this project): [Download Python](https://www.python.org/downloads/release/python-3120/)
- Tesseract OCR (Windows only): Install and place executable at `C:\Program Files\Tesseract-OCR\tesseract.exe`

The file for installation is located at tesseract folder.

---
## Getting Started 📖

> :information_source: **Observation:** I am currently exploring ways to create a more user-friendly executable for easy usage. Stay tuned for updates on a simplified version that will make it even more straightforward for users to run the bot without the need for manual configurations. Your patience and feedback are highly appreciated!

First you need to create a virtual environment:

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

To end bot, use ´CTRL + C´ and deactivate the virtual environment:

```sh
deactivate
```

---
## Build application 🧑‍🏭

Navigate to Your Script's Directory:
Open the command prompt and navigate to the directory containing your Python script (`launcher.py`).

Create the Executable:
Run the following command into `launcher.py` folder to create the executable:

```sh
pyinstaller --onefile --add-data "icon.ico;." --add-data "../images;images" launcher.py
```

This command will create a dist folder in your script's directory, containing the executable file (`launcher.exe`).

Find the Executable:
Navigate to the dist folder, and you'll find your executable (`bot.exe`).

---
## Buy me a coffee ☕❤️

![PayPal](https://img.shields.io/badge/PayPal-00457C?style=for-the-badge&logo=paypal&logoColor=white)
[![Donate with PayPal](https://www.paypalobjects.com/en_US/i/btn/btn_donate_LG.gif)](https://www.paypal.com/donate?hosted_button_id=23PAVC8AMJGYW)

---
## Contact 📫:

Feedback, ideas, or anything else you'd like to share: [gustavoperin067@gmail.com](mailto:gustavoperin067@gmail.com)
