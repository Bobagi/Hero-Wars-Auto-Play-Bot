# game-automation-bot
Python bot game automation

The dependencies are specified on requirements.txt.

To work on code and start the bot, create a virtual environment:

´´´sh
python -m venv venv
´´´

Then, activate your virtual environment:

´´´sh
.\venv\Scripts\activate
´´´

To install the depencies, go to the project folder and use:

´´´sh
pip install -r requirements.txt
´´´

That file does not update automatically, so if you chance something (add, update or remove dependencies), need to run that command to update the file:

´´´sh
pip freeze > requirements.txt
´´´

them, run the code:

´´´sh
python bot.py
´´´

To end bot, use ´CTRL + C´ and desactivate the virtual environment:

´´´sh
deactivate
´´´