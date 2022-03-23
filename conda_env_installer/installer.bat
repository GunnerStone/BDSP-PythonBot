:: What this line does is, the first time you run it, it re-launches itself 
:: in a subprocess that doesn't exit after it finishes running the batch file.
:: Source: https://stackoverflow.com/questions/17118846/how-to-prevent-batch-window-from-closing-when-error-occurs
:: This is to prevent the terminal from closing on an error.
@echo off
if not defined in_subprocess (cmd /k set in_subprocess=y ^& %0 %*) & exit )

:: Installs the conda environment needed to run the bot
call conda env create -f environment.yml