"""
Utilitaires pour les macros
"""

import os
import sys


def get_macros_dir():
    """
    Retourne le chemin absolu du dossier macros
    Compatible avec les scripts Python et les exécutables PyInstaller
    """
    if getattr(sys, 'frozen', False):
        # Exécutable PyInstaller
        base_dir = os.path.dirname(sys.executable)
    else:
        # Script Python normal
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    return os.path.join(base_dir, 'macros')
