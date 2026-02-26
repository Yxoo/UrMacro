"""
Système de macros modulaires avec kits
Utilisation: python main.py
Permet de combiner plusieurs macros avec différentes touches d'activation
"""

import sys
import os

from src.ui import menu_principal
from src.utils import get_macros_dir


def main():
    """Point d'entrée du programme"""
    # Déterminer le répertoire de base (où se trouve l'exe ou le script)
    if getattr(sys, 'frozen', False):
        # Exécutable PyInstaller
        base_dir = os.path.dirname(sys.executable)
    else:
        # Script Python normal
        base_dir = os.path.dirname(os.path.abspath(__file__))

    # Ajouter le répertoire de base au sys.path pour permettre l'import des macros
    if base_dir not in sys.path:
        sys.path.insert(0, base_dir)

    # Créer le dossier macros s'il n'existe pas
    macros_dir = get_macros_dir()
    if not os.path.exists(macros_dir):
        os.makedirs(macros_dir)
        print("📁 Dossier 'macros/' créé")
        print("💡 Ajoutez vos fichiers de macros dans ce dossier")

    # Lancer le menu principal
    menu_principal()


if __name__ == "__main__":
    main()
