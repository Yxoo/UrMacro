"""
Gestionnaire de kits - Sauvegarde, chargement et utilitaires
"""

import os
import json
from .kit import Kit
from ..utils import get_macros_dir


def lister_macros_disponibles():
    """Liste toutes les macros disponibles"""
    macros_dir = get_macros_dir()
    if not os.path.exists(macros_dir):
        return []

    macros = []
    for fichier in os.listdir(macros_dir):
        if fichier.endswith('.py') and fichier != '__init__.py':
            macros.append(fichier[:-3])
    return sorted(macros)


def sauvegarder_kit(kit, fichier='kits.json'):
    """Sauvegarde un kit dans un fichier JSON"""
    kits = []

    # Charger les kits existants
    if os.path.exists(fichier):
        try:
            with open(fichier, 'r', encoding='utf-8') as f:
                data = json.load(f)
                kits = [Kit.from_dict(k) for k in data]
        except:
            pass

    # Vérifier si un kit avec le même nom existe
    kit_existe = False
    for i, k in enumerate(kits):
        if k.nom == kit.nom:
            kits[i] = kit
            kit_existe = True
            break

    if not kit_existe:
        kits.append(kit)

    # Sauvegarder
    with open(fichier, 'w', encoding='utf-8') as f:
        json.dump([k.to_dict() for k in kits], f, indent=2, ensure_ascii=False)


def charger_kits(fichier='kits.json'):
    """Charge tous les kits depuis un fichier JSON"""
    if not os.path.exists(fichier):
        return []

    try:
        with open(fichier, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return [Kit.from_dict(k) for k in data]
    except:
        return []
