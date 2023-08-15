@echo off

:: set path 
set ROOT=%~dp0..\
set PATH=%ROOT%\\.venv\\Scripts\\pyinstaller.exe
set FILE=%ROOT%\\main.py

:: run 
%PATH% %FILE% -n webcamapp