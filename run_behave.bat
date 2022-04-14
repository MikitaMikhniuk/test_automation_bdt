@echo off
python3 --version > NUL 2>&1
if ERRORLEVEL 1 echo "No Python3 distributable! PLease isntall Python3 to proceed." & exit 1

pip install --upgrade pip
python3 -m venv bdt_env
bdt_env\Scripts\pip install pytest
bdt_env\Scripts\pip install selenium
bdt_env\Scripts\pip install webdriver_manager
bdt_env\Scripts\pip install behave
bdt_env\Scripts\python -m behave onliner/features --junit