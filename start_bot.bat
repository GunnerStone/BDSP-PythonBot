:: What this line does is, the first time you run it, it re-launches itself 
:: in a subprocess that doesn't exit after it finishes running the batch file.
:: Source: https://stackoverflow.com/questions/17118846/how-to-prevent-batch-window-from-closing-when-error-occurs
:: This is to prevent the terminal from closing on an error.
@echo off
if not defined in_subprocess (cmd /k set in_subprocess=y ^& %0 %*) & exit )

:: Starts the conda environment needed to run the bot
call activate pySwitchBots

:: Starts the bot with python

echo [32mReposition the terminal window out of the way of the capture utility ^& MaxAimDI Plugin[0m

set /p DUMMY=[33mHit ENTER to start the bot...[0m
cls
color 0F
python BDSP-Scripts/script_runner.py

:: Changes the window position to the top right corner
WINDOW[bottom]
