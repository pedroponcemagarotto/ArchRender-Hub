@echo off
setlocal
cd /d "%~dp0"
title ArchRender Hub - Videos Gratis no PC
where py >nul 2>nul
if %errorlevel%==0 (
  py -3 tools\video_local_gui.py
  goto end
)
where python >nul 2>nul
if %errorlevel%==0 (
  python tools\video_local_gui.py
  goto end
)
echo Python 3.9 ou superior nao foi encontrado.
echo Instale Python em https://www.python.org/downloads/
echo Depois execute este arquivo novamente.
pause
:end
endlocal
