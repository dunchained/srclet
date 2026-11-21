@echo off
setlocal
pushd "%~dp0" || exit /b 1
if exist ".venv-win\Scripts\python.exe" goto install
where py >nul 2>nul
if errorlevel 1 goto try_python
py -3 -m venv ".venv-win"
if not errorlevel 1 goto install
:try_python
where python >nul 2>nul
if errorlevel 1 goto need_python
python -m venv ".venv-win"
if errorlevel 1 goto need_python
:install
".venv-win\Scripts\python.exe" -c "import sys; sys.exit(0 if sys.version_info >= (3,10) else 'Python 3.10+ required')"
if errorlevel 1 goto failed
".venv-win\Scripts\python.exe" -m pip install --disable-pip-version-check -r requirements.txt
if errorlevel 1 goto failed
".venv-win\Scripts\python.exe" srclet.py %*
if errorlevel 1 goto failed
popd
exit /b 0
:need_python
where winget >nul 2>nul
if errorlevel 1 goto no_package_manager
winget install --id Python.Python.3.13 --exact --scope user --accept-package-agreements --accept-source-agreements
if errorlevel 1 goto no_package_manager
if not exist "%LOCALAPPDATA%\Programs\Python\Python313\python.exe" goto no_package_manager
"%LOCALAPPDATA%\Programs\Python\Python313\python.exe" -m venv ".venv-win"
if errorlevel 1 goto failed
goto install
:no_package_manager
echo Install 64-bit Python 3.10 or newer from python.org, then run this file again.
:failed
pause
popd
exit /b 1
