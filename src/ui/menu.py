"""
Menus interactifs pour la gestion des kits
"""

import sys
import os
import subprocess
import platform
from ..core.kit import Kit
from ..core.kit_runner import KitRunner
from ..core.kit_manager import sauvegarder_kit, charger_kits, lister_macros_disponibles
from ..utils import get_macros_dir
from .cursor_utility import run_cursor_utility


def ouvrir_dossier_macros():
    """Ouvre le dossier macros dans l'explorateur de fichiers"""
    macros_dir = get_macros_dir()

    # Créer le dossier s'il n'existe pas
    if not os.path.exists(macros_dir):
        os.makedirs(macros_dir)

    try:
        if platform.system() == 'Windows':
            os.startfile(macros_dir)
        elif platform.system() == 'Darwin':  # macOS
            subprocess.run(['open', macros_dir])
        else:  # Linux
            subprocess.run(['xdg-open', macros_dir])
        print(f"\n✅ Dossier ouvert: {macros_dir}")
    except Exception as e:
        print(f"\n❌ Erreur lors de l'ouverture du dossier: {e}")


def menu_gestion_kit(kit=None):
    """Menu de gestion d'un kit"""
    if kit is None:
        kit = Kit()

    while True:
        # Recharger les macros disponibles à chaque itération
        macros_disponibles = lister_macros_disponibles()
        print("\n" + "=" * 60)
        print(f"⚙️  GESTION DU KIT: {kit.nom}")
        print("=" * 60)

        if kit.macros:
            print("\n📋 Macros dans le kit:\n")
            for i, (macro, touche) in enumerate(kit.macros, 1):
                print(f"  {i}. [{touche}] {macro}")
        else:
            print("\n📋 Le kit est vide")

        print("\n🔧 Options:")
        print("  1. Ajouter une macro")
        print("  2. Retirer une macro")
        print("  3. Renommer le kit")
        print("  4. Sauvegarder le kit")
        print("  5. Lancer le kit (par défaut)")
        print("  0. Retour au menu principal")

        choix = input("\nChoisissez une option [Entrée = Lancer]: ").strip()

        # Si Entrée sans input, lancer le kit par défaut
        if choix == '':
            choix = '5'

        if choix == '1':
            # Ajouter une macro
            if not macros_disponibles:
                print("\n❌ Aucune macro disponible")
                print("💡 Ajoutez d'abord des fichiers .py dans le dossier 'macros/'")
                continue

            print("\n📁 Macros disponibles:\n")
            for i, macro in enumerate(macros_disponibles, 1):
                print(f"  {i}. {macro}")

            try:
                idx = int(input("\nNuméro de la macro: ")) - 1
                if 0 <= idx < len(macros_disponibles):
                    touche = input("Touche d'activation (une lettre): ").strip().lower()
                    if len(touche) == 1:
                        success, msg = kit.ajouter_macro(macros_disponibles[idx], touche)
                        print(f"\n{'✅' if success else '❌'} {msg}")
                    else:
                        print("\n❌ Veuillez entrer une seule lettre")
                else:
                    print("\n❌ Numéro invalide")
            except ValueError:
                print("\n❌ Entrée invalide")

        elif choix == '2':
            # Retirer une macro
            if kit.macros:
                try:
                    idx = int(input("\nNuméro de la macro à retirer: ")) - 1
                    success, msg = kit.retirer_macro(idx)
                    print(f"\n{'✅' if success else '❌'} {msg}")
                except ValueError:
                    print("\n❌ Entrée invalide")
            else:
                print("\n❌ Le kit est vide")

        elif choix == '3':
            # Renommer le kit
            nouveau_nom = input("\nNouveau nom du kit: ").strip()
            if nouveau_nom:
                kit.nom = nouveau_nom
                print(f"\n✅ Kit renommé en '{nouveau_nom}'")

        elif choix == '4':
            # Sauvegarder le kit
            sauvegarder_kit(kit)
            print(f"\n✅ Kit '{kit.nom}' sauvegardé")

        elif choix == '5':
            # Lancer le kit
            if kit.macros:
                runner = KitRunner(kit)
                modifier = runner.run()

                # Si l'utilisateur a demandé à modifier le kit, continuer la boucle
                if modifier:
                    continue
                else:
                    # Retour au menu principal
                    return kit
            else:
                print("\n❌ Le kit est vide. Ajoutez des macros avant de lancer.")

        elif choix == '0':
            # Retour
            return kit

        else:
            print("\n❌ Option invalide")


def menu_principal():
    """Menu principal du programme"""
    # Boucle principale
    while True:
        # Recharger les macros et les kits à chaque itération
        macros_disponibles = lister_macros_disponibles()
        kits_sauvegardes = charger_kits()
        print("\n" + "=" * 60)
        print("🎮 SYSTÈME DE MACROS MODULAIRES - KITS")
        print("=" * 60)

        print("\n📦 Options:")
        print("  1. Créer un nouveau kit")
        print("  2. Charger un kit sauvegardé (par défaut)")
        print("  3. Ouvrir le dossier des macros")
        print("  4. Utilitaire curseur")
        print("\n  [ESC] Quitter le programme (Ctrl+C)")

        try:
            choix = input("\nChoisissez une option [Entrée = Charger]: ").strip()

            # Si Entrée sans input, charger un kit par défaut
            if choix == '':
                choix = '2'

            if choix == '1':
                # Créer un nouveau kit
                if not macros_disponibles:
                    print("\n❌ Aucune macro disponible")
                    print("💡 Ajoutez d'abord des macros dans le dossier 'macros/' (option 3)")
                else:
                    nom = input("\nNom du kit: ").strip()
                    if not nom:
                        nom = "Kit sans nom"
                    kit = Kit(nom)
                    menu_gestion_kit(kit)

            elif choix == '2':
                # Charger un kit sauvegardé
                if not kits_sauvegardes:
                    print("\n📦 Aucun kit sauvegardé")
                    print("💡 Créez d'abord un kit avec l'option 1")
                else:
                    print("\n📦 Kits sauvegardés:\n")
                    for i, kit in enumerate(kits_sauvegardes, 1):
                        nb_macros = len(kit.macros)
                        print(f"  {i}. {kit.nom} ({nb_macros} macro{'s' if nb_macros > 1 else ''})")

                    try:
                        idx = int(input("\nNuméro du kit (0 pour annuler): ")) - 1
                        if idx == -1:
                            continue
                        if 0 <= idx < len(kits_sauvegardes):
                            menu_gestion_kit(kits_sauvegardes[idx])
                            # Recharger les kits pour avoir les modifications
                            kits_sauvegardes = charger_kits()
                        else:
                            print("\n❌ Numéro invalide")
                    except ValueError:
                        print("\n❌ Entrée invalide")

            elif choix == '3':
                # Ouvrir le dossier des macros
                ouvrir_dossier_macros()

            elif choix == '4':
                # Utilitaire curseur
                run_cursor_utility()

            else:
                print("\n❌ Option invalide")

        except KeyboardInterrupt:
            print("\n\n👋 Au revoir !")
            sys.exit(0)
