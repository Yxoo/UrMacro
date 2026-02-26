"""
Classe KitRunner pour gérer l'exécution d'un kit de macros
"""

import importlib.util
import sys
import os
import time
from pynput import keyboard
from pynput.keyboard import Key

import urmacro
from .macro_instance import MacroInstance
from ..utils import get_macros_dir


def _charger_module(nom_macro):
    """Charge un module macro avec urmacro injecté dans son namespace."""
    module_name = f'macros.{nom_macro}'
    file_path = os.path.join(get_macros_dir(), f'{nom_macro}.py')
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    for name in urmacro.__all__:
        module.__dict__[name] = getattr(urmacro, name)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


class KitRunner:
    """Gère l'exécution d'un kit de macros"""

    def __init__(self, kit):
        self.kit = kit
        self.macro_instances = []
        self.running = True
        self.modifier_kit = False

    def charger_macros(self):
        """Charge tous les modules de macros du kit"""
        self.macro_instances = []
        for nom_macro, touche in self.kit.macros:
            try:
                module = _charger_module(nom_macro)
                instance = MacroInstance(nom_macro, touche, module)
                self.macro_instances.append(instance)
            except Exception as e:
                print(f"❌ Erreur lors du chargement de '{nom_macro}': {e}")
                return False
        return True

    def recharger_macros(self):
        """Recharge les modules de macros pour appliquer les modifications du code"""
        # Vérifier qu'aucune macro n'est active
        macros_actives = [inst for inst in self.macro_instances if inst.active]
        if macros_actives:
            print("\n⚠️  Impossible de recharger : des macros sont actives")
            print("   Arrêtez toutes les macros avant de recharger (Echap)")
            return False

        print("\n🔄 Rechargement des macros...")

        modules_recharges = []
        for nom_macro, touche in self.kit.macros:
            try:
                _charger_module(nom_macro)
                print(f"   ✅ {nom_macro} rechargé")
                modules_recharges.append(nom_macro)
            except Exception as e:
                print(f"   ❌ Erreur lors du rechargement de '{nom_macro}': {e}")
                return False

        # Recréer les instances avec les modules rechargés
        self.macro_instances = []
        for nom_macro, touche in self.kit.macros:
            module = sys.modules[f'macros.{nom_macro}']
            instance = MacroInstance(nom_macro, touche, module)
            self.macro_instances.append(instance)

        print(f"\n✅ {len(modules_recharges)} macro(s) rechargée(s) avec succès\n")
        time.sleep(0.5)
        return True

    def on_press(self, key):
        """Callback pour les touches pressées"""
        try:
            if hasattr(key, 'char'):
                char = key.char.lower()

                # Vérifier si c'est une touche de toggle pour une macro
                for instance in self.macro_instances:
                    if char == instance.touche_activation:
                        instance.toggle()
                        return

                # Touche ~ pour modifier le kit
                if char == '`' or char == '~':
                    print("\n\n⚙️  Modification du kit...")
                    self.modifier_kit = True
                    self.arreter_toutes_macros()
                    time.sleep(0.15)
                    return False

                # Touche / pour recharger les macros
                if char == '/':
                    if self.recharger_macros():
                        self.afficher_statut()

            elif key == Key.esc:
                macros_actives = [inst for inst in self.macro_instances if inst.active]

                if macros_actives:
                    print("\n⏹️  Arrêt de toutes les macros actives...")
                    self.arreter_toutes_macros()
                    time.sleep(0.15)
                    self.afficher_statut()
                else:
                    print("\n\n🔙 Retour au menu principal...")
                    self.running = False
                    return False
        except AttributeError:
            pass

    def arreter_toutes_macros(self):
        """Arrête toutes les macros actives"""
        for instance in self.macro_instances:
            instance.stop()

    def afficher_statut(self):
        """Affiche le statut du kit et des macros"""
        print("=" * 60)
        print(f"🎮 Kit actif: {self.kit.nom}")
        print("=" * 60)
        print("\n📋 Macros chargées:\n")

        for instance in self.macro_instances:
            statut = "🟢 ACTIVE" if instance.active else "⚪ Inactive"
            print(f"  [{instance.touche_activation}] {instance.nom_macro} - {statut}")

        print("\n📖 Contrôles:")
        print("  • Touches assignées : Démarrer/Arrêter la macro correspondante")
        print("  • Touche 'Echap' : Arrêter les macros actives (x1) / Retour au menu (x2)")
        print("  • Touche '/' : Recharger les macros (appliquer les changements de code)")
        print("  • Touche '~' : Modifier le kit")
        print("\n⏳ En attente de commande...\n")

    def run(self):
        """Lance l'exécution du kit"""
        if not self.charger_macros():
            print("❌ Erreur lors du chargement des macros")
            return False

        if len(self.macro_instances) == 0:
            print("❌ Le kit est vide. Ajoutez des macros avant de lancer.")
            return False

        self.afficher_statut()

        with keyboard.Listener(on_press=self.on_press) as listener:
            listener.join()

        return self.modifier_kit
