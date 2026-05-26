#!/bin/bash
cd "$(dirname "$0")"

echo "==========================================="
echo "       LOUVRE ESCAPE  -  Lancement"
echo "==========================================="
echo ""

# Verifier Python
if ! command -v python3 &> /dev/null; then
    echo "[ERREUR] Python 3 n'est pas installe."
    echo ""
    echo "  - Ubuntu/Debian : sudo apt install python3 python3-pip"
    echo "  - Mac            : https://www.python.org/downloads/"
    echo ""
    read -p "Appuyez sur Entree pour fermer..."
    exit 1
fi

# Installer les dependances
echo "Installation des dependances..."
pip3 install -r requirements.txt --quiet

echo "Demarrage du jeu..."
echo ""
python3 main.py
