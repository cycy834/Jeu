@echo off
title Louvre Escape
pushd %~dp0

echo ===========================================
echo        LOUVRE ESCAPE  -  Lancement
echo ===========================================
echo.

:: Verifier que Python est installe
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERREUR] Python n'est pas installe sur cet ordinateur.
    echo.
    echo  1. Allez sur https://www.python.org/downloads/
    echo  2. Telechargez Python 3.12
    echo  3. IMPORTANT : cochez "Add Python to PATH" pendant l'installation
    echo  4. Relancez ce fichier
    echo.
    pause
    exit /b 1
)

:: Installer les dependances si besoin
echo Installation des dependances...
pip install -r requirements.txt --quiet --disable-pip-version-check
if %errorlevel% neq 0 (
    echo [ERREUR] Impossible d'installer les dependances.
    echo Verifiez votre connexion internet et relancez.
    echo.
    pause
    exit /b 1
)

echo Demarrage du jeu...
echo.
python main.py

if %errorlevel% neq 0 (
    echo.
    echo Le jeu s'est ferme avec une erreur.
    pause
)
