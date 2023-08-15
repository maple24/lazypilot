@echo off

:: set path 
set ROOT=%~dp0..\
set PATH=%ROOT%\\.venv\\Scripts\\pyarmor.exe
set FOLDER=%ROOT%

:: run 
%PATH% gen -O lazypilot %FOLDER%