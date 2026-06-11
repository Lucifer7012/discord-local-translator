@echo off
cd /d "%~dp0"
where pythonw >nul 2>nul
if %errorlevel%==0 (
    start "" /b pythonw local_translator.py
    exit /b 0
)

where pyw >nul 2>nul
if %errorlevel%==0 (
    start "" /b pyw local_translator.py
    exit /b 0
)

python local_translator.py
pause
