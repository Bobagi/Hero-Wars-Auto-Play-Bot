@echo off

echo Activating virtual environment...
call .\venv\Scripts\activate
echo Remember to deactivate the virtual environment... (deactivate)

echo Running the bot...
python bots/bot.py