@echo off
setlocal
cd /d "%~dp0"
where py >nul 2>&1
if %errorlevel%==0 (
  py -3 app.py
) else (
  where python >nul 2>&1
  if %errorlevel%==0 (
    python app.py
  ) else (
    echo.
    echo ERRO: Python 3.9 ou superior nao foi encontrado.
    echo Instale Python a partir de https://www.python.org/downloads/
    echo Marque a opcao Add Python to PATH e tente novamente.
    echo.
    pause
  )
)
endlocal
