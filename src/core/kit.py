"""
Classe Kit pour gérer un ensemble de macros
"""


class Kit:
    """Représente un kit de macros"""

    def __init__(self, nom="Kit par défaut"):
        self.nom = nom
        self.macros = []  # Liste de tuples (nom_macro, touche_activation)

    def ajouter_macro(self, nom_macro, touche_activation):
        """Ajoute une macro au kit"""
        # Vérifier que la touche n'est pas déjà utilisée
        for macro, touche in self.macros:
            if touche.lower() == touche_activation.lower():
                return False, f"La touche '{touche}' est déjà utilisée par '{macro}'"

        self.macros.append((nom_macro, touche_activation.lower()))
        return True, f"Macro '{nom_macro}' ajoutée avec la touche '{touche_activation}'"

    def retirer_macro(self, index):
        """Retire une macro du kit par son index"""
        if 0 <= index < len(self.macros):
            macro_retiree = self.macros.pop(index)
            return True, f"Macro '{macro_retiree[0]}' retirée du kit"
        return False, "Index invalide"

    def to_dict(self):
        """Convertit le kit en dictionnaire pour la sauvegarde"""
        return {
            "nom": self.nom,
            "macros": self.macros
        }

    @staticmethod
    def from_dict(data):
        """Crée un kit depuis un dictionnaire"""
        kit = Kit(data.get("nom", "Kit par défaut"))
        kit.macros = data.get("macros", [])
        return kit
