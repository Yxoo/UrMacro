"""
Classe MacroInstance pour gérer une instance de macro en cours d'exécution
"""

import threading


class MacroInstance:
    """Représente une instance de macro en cours d'exécution"""

    def __init__(self, nom_macro, touche_activation, module_macro):
        self.nom_macro = nom_macro
        self.touche_activation = touche_activation.lower()
        self.module_macro = module_macro
        self.active = False
        self.thread = None

    def get_active_status(self):
        """Retourne le statut actif de cette macro"""
        return self.active

    def _run_macro_wrapper(self):
        """Wrapper qui exécute la macro et la désactive automatiquement à la fin"""
        try:
            # Exécuter la macro
            self.module_macro.executer_macro(self.get_active_status)
        finally:
            # Si la macro se termine et qu'elle est toujours marquée comme active,
            # la désactiver automatiquement (pour les macros "one-shot")
            if self.active:
                self.active = False
                print(f"\n✅ [{self.touche_activation}] Macro '{self.nom_macro}' terminée (désactivation auto)")

    def toggle(self):
        """Active ou désactive cette macro"""
        if not self.active:
            # Démarrer la macro
            self.active = True
            print(f"\n▶️  [{self.touche_activation}] Macro '{self.nom_macro}' activée")
            self.thread = threading.Thread(
                target=self._run_macro_wrapper,
                daemon=True
            )
            self.thread.start()
        else:
            # Arrêter la macro
            self.active = False
            print(f"\n⏸️  [{self.touche_activation}] Macro '{self.nom_macro}' désactivée")

    def stop(self):
        """Arrête la macro si elle est active"""
        if self.active:
            self.active = False
