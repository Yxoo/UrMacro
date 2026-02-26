@echo off
cd /d "%~dp0\.."
echo ========================================
echo Generation de l'executable UrMacro
echo ========================================
echo.

echo Installation du package urmacropkg (depuis source locale)...
pip install -e "D:\=Dev\_Packages\urmacropkg" --quiet
echo.

echo Installation des dependances...
pip install -r requirements.txt
echo.

taskkill /F /IM UrMacro.exe >nul 2>&1

echo Generation de l'executable...
pyinstaller tools\urmacro.spec
echo.

if exist "dist\UrMacro.exe" (
    if not exist "dist\macros" mkdir "dist\macros"
    if not exist "dist\kits.json" echo [] > "dist\kits.json"

    echo ========================================
    echo Executable genere avec succes !
    echo Emplacement: dist\UrMacro.exe
    echo ========================================
    echo.
    echo Contenu du dossier dist:
    echo   - UrMacro.exe
    echo   - macros\          (dossier pour vos macros)
    echo   - kits.json        (configuration des kits)
) else (
    echo ========================================
    echo Erreur lors de la generation !
    echo ========================================
)

pause
