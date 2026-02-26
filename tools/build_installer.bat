@echo off
cd /d "%~dp0\.."
echo ========================================
echo Build complet : Executable + Installateur
echo ========================================
echo.

echo [1/4] Installation du package urmacropkg (source locale)...
pip install -e "D:\=Dev\_Packages\urmacropkg" --quiet
if errorlevel 1 (
    echo ERREUR : impossible d'installer urmacropkg
    pause
    exit /b 1
)
echo.

echo [2/4] Installation des dependances...
pip install -r requirements.txt --quiet
if errorlevel 1 (
    echo ERREUR lors de l'installation des dependances
    pause
    exit /b 1
)
echo.

echo [3/4] Generation de l'executable...
pyinstaller --clean tools\urmacro.spec
if errorlevel 1 (
    echo ERREUR lors de la generation de l'executable
    pause
    exit /b 1
)

if not exist "dist\macros" mkdir "dist\macros"
if not exist "dist\kits.json" echo [] > "dist\kits.json"
echo.

echo [4/4] Generation de l'installateur...
echo.

set ISCC=""
if exist "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" (
    set ISCC="C:\Program Files (x86)\Inno Setup 6\ISCC.exe"
) else if exist "C:\Program Files\Inno Setup 6\ISCC.exe" (
    set ISCC="C:\Program Files\Inno Setup 6\ISCC.exe"
) else (
    echo ========================================
    echo Inno Setup non installe
    echo ========================================
    echo.
    echo L'executable a ete genere dans dist\UrMacro.exe
    echo Pour l'installateur, installez Inno Setup 6 puis relancez.
    echo https://jrsoftware.org/isdl.php
    echo.
    pause
    exit /b 0
)

%ISCC% tools\installer.iss
if errorlevel 1 (
    echo ERREUR lors de la generation de l'installateur
    pause
    exit /b 1
)

echo.
echo ========================================
echo BUILD COMPLET TERMINE !
echo ========================================
echo.
echo   Executable  : dist\UrMacro.exe
echo   Installateur: installer_output\UrMacro_Setup.exe
echo.
echo A joindre au GitHub Release :
echo   - dist\UrMacro.exe          (mise a jour legere)
echo   - installer_output\UrMacro_Setup.exe  (installation complete)
echo.
pause
