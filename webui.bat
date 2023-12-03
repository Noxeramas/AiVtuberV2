@echo off
echo Starting AiVtuberV2...

REM Set the path to the directory where the script is located
cd src

REM activate virtual environment
call ../venv/Scripts/activate.bat

REM install dependencies
pip install -r ../requirements.txt

REM run the script
python main.py

REM pause the command window
pause