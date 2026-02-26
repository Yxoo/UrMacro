e# Projet Macro en Boucle avec PyDirectInput

## 📋 Description
Script Python qui exécute des macros clavier en boucle. Supporte deux modes d'utilisation :
1. **Mode Kit** (par défaut): Combine plusieurs macros avec différentes touches d'activation
2. **Mode Simple**: Lance une macro unique via la ligne de commande

## 🗂️ Structure du Projet
```
custom_macros/
├── main.py                    # Point d'entrée simplifié (22 lignes)
├── kits.json                  # Sauvegarde des kits de macros
├── macros/                    # Macros utilisateur
│   ├── __init__.py
│   ├── exemple_macro.py       # Exemple de macro simple
│   ├── farming_macro.py       # Macro de farming
│   ├── combat_macro.py        # Macro de combat
│   ├── click_spam_macro.py    # Maintien des clics
│   └── sequence_1to9_macro.py # Séquence 1-9
└── src/                       # Code source organisé
    ├── __init__.py            # Exports du module
    ├── kit.py                 # Classe Kit (44 lignes)
    ├── macro_instance.py      # Classe MacroInstance (44 lignes)
    ├── kit_runner.py          # Classe KitRunner (101 lignes)
    ├── kit_manager.py         # Gestion sauvegarde/chargement (62 lignes)
    ├── menu.py                # Menus interactifs (185 lignes)
    └── utils.py               # Utilitaires (sleep_interruptible)
```

## 🎮 Système de Kit (Nouveau)

Le système de kit permet de combiner plusieurs macros et de les contrôler simultanément avec différentes touches d'activation.

### Classes principales

#### `Kit`
Représente un ensemble de macros avec leurs touches d'activation
- `nom`: Nom du kit
- `macros`: Liste de tuples `(nom_macro, touche_activation)`
- `ajouter_macro(nom_macro, touche)`: Ajoute une macro au kit
- `retirer_macro(index)`: Retire une macro du kit
- `to_dict()` / `from_dict()`: Sauvegarde/chargement JSON

#### `MacroInstance`
Représente une macro en cours d'exécution
- `nom_macro`: Nom de la macro
- `touche_activation`: Touche pour activer/désactiver
- `active`: État actuel (actif/inactif)
- `toggle()`: Active ou désactive la macro
- `get_active_status()`: Retourne si la macro est active

#### `KitRunner`
Gère l'exécution d'un kit complet
- `charger_macros()`: Charge tous les modules du kit
- `on_press(key)`: Gère les touches pressées
- `run()`: Lance l'exécution du kit
- `arreter_toutes_macros()`: Arrête toutes les macros actives

### Fichier `kits.json`
Stocke les kits sauvegardés au format JSON:
```json
[
  {
    "nom": "donut_smp",
    "macros": [
      ["click_spam_macro", "j"],
      ["sequence_1to9_macro", "k"]
    ]
  },
  {
    "nom": "combat_smp",
    "macros": [
      ["combat_macro", "q"]
    ]
  }
]
```

### Fonctions de gestion des kits
- `sauvegarder_kit(kit, fichier='kits.json')`: Sauvegarde un kit
- `charger_kits(fichier='kits.json')`: Charge tous les kits
- `menu_gestion_kit(kit)`: Menu interactif de gestion d'un kit
- `lister_macros_disponibles()`: Liste toutes les macros disponibles

## 📄 Fichier: `main.py`

### Responsabilités (Mode Kit)
- Afficher le menu principal de gestion des kits
- Créer, modifier et sauvegarder des kits
- Charger dynamiquement les macros d'un kit
- Gérer plusieurs macros simultanément avec différentes touches
- Écouter les touches du clavier (pynput)
- Gérer le threading pour chaque macro du kit
- Afficher les messages de statut pour chaque macro

### Imports nécessaires
```python
import sys
import importlib
import os
import json
from pynput import keyboard
from pynput.keyboard import Key
import threading
```

## 📄 Fichiers dans `macros/`

### Format standard pour chaque macro

Chaque fichier de macro doit avoir:
- Une fonction `executer_macro(get_active_status)` qui prend en paramètre une fonction callable
- Utiliser `sleep_interruptible()` au lieu de `time.sleep()` pour permettre l'arrêt immédiat
- Vérifier régulièrement `get_active_status()` dans les boucles
- Section clairement délimitée pour le code personnalisé

### Exemple de structure d'une macro (avec arrêt immédiat)
```python
"""
Nom de la macro: Description courte
"""

import pydirectinput
import sys
import os

# Ajouter le dossier parent au path pour importer src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.utils import sleep_interruptible


def executer_macro(get_active_status):
    """
    Fonction principale de la macro
    get_active_status: fonction qui retourne True si la macro doit continuer
    """
    print("🔄 Macro [NOM] démarrée...")

    while get_active_status():
        # ========== DÉBUT DE LA MACRO ==========

        # Votre code ici
        pydirectinput.press('space')
        # Utiliser sleep_interruptible au lieu de time.sleep
        if not sleep_interruptible(1, get_active_status):
            break  # Arrêt immédiat

        # ========== FIN DE LA MACRO ==========

        if not sleep_interruptible(0.1, get_active_status):
            break

    print("⏹️ Macro [NOM] arrêtée")
```

### Fonction `sleep_interruptible(duration, get_active_status)`
Cette fonction remplace `time.sleep()` et permet l'arrêt immédiat de la macro:
- **duration**: Durée du sleep en secondes
- **get_active_status**: Fonction de statut de la macro
- **Retour**: `True` si le sleep s'est terminé normalement, `False` si interrompu

La fonction vérifie toutes les 50ms si la macro doit s'arrêter, permettant une réponse quasi-instantanée à l'appui sur Echap.

### Types de macros

#### Macro en boucle infinie (exemple: click_spam_macro)
```python
def executer_macro(get_active_status):
    print("🔄 Macro démarrée...")

    while get_active_status():  # Boucle tant que la macro est active
        # Votre code répétitif
        pydirectinput.press('space')
        if not sleep_interruptible(1, get_active_status):
            break

    print("⏹️ Macro arrêtée")
```
- Se répète à l'infini jusqu'à désactivation manuelle
- Nécessite un appui sur la touche ou Echap pour arrêter

#### Macro "one-shot" (exemple: sequence_1to9_macro)
```python
def executer_macro(get_active_status):
    print("🔄 Macro démarrée...")

    # Pas de while get_active_status() !
    # Juste une exécution unique
    for i in range(1, 10):
        if not get_active_status():  # Vérifier si arrêt demandé
            break
        pydirectinput.press(str(i))
        if not sleep_interruptible(0.2, get_active_status):
            break

    print("⏹️ Macro terminée")
    # Pas besoin d'appeler stop() - désactivation automatique !
```
- S'exécute une seule fois puis **se désactive automatiquement**
- Pour relancer : un seul appui sur la touche (pas besoin de double appui)
- Le système affiche : `✅ [touche] Macro 'nom' terminée (désactivation auto)`

## 🎯 Utilisation

### Mode Kit (Recommandé)

#### 1. Lancer le programme
```bash
python main.py
```

#### 2. Menu principal
- **Option 1**: Créer un nouveau kit
- **Option 2**: Charger/Gérer un kit sauvegardé (par défaut : appuyez sur Entrée)

💡 **Astuce**: Appuyez simplement sur Entrée pour charger rapidement un kit

#### 3. Gestion d'un kit
Dans le menu de gestion:
1. **Ajouter une macro**: Choisir une macro et assigner une touche
2. **Retirer une macro**: Supprimer une macro du kit
3. **Renommer le kit**: Changer le nom du kit
4. **Sauvegarder le kit**: Enregistrer dans `kits.json`
5. **Lancer le kit**: Démarrer l'exécution (par défaut : appuyez sur Entrée)
0. **Retour au menu principal**

💡 **Astuce**: Appuyez simplement sur Entrée pour lancer directement le kit

#### 4. Contrôles pendant l'exécution
- **Touches assignées**: Activer/Désactiver la macro correspondante
- **Touche 'Echap'**: Comportement intelligent
  - **1er Echap** (si macros actives) : Arrête toutes les macros
  - **2ème Echap** (si aucune macro active) : Retour au menu principal
- **Touche '/'**: Recharger les macros (appliquer les changements de code)
- **Touche '~'**: Modifier le kit

### Exemple de workflow

#### Workflow ultra-rapide (kit existant)
```bash
# Lancer votre kit favori en 3 touches !
python main.py
[Entrée]           # Charge un kit (option 2 par défaut)
1                  # Sélectionne le kit #1
[Entrée]           # Lance le kit (option 5 par défaut)

# Total : 3 appuis de touches ! ⚡
```

#### Créer un nouveau kit
```bash
# 1. Lancer le programme
python main.py

# 2. Créer un nouveau kit
1 → Entrer "mon_kit"

# 3. Ajouter des macros
1 → Choisir "click_spam_macro" → Touche "j"
1 → Choisir "combat_macro" → Touche "k"

# 4. Sauvegarder le kit
4

# 5. Lancer le kit
[Entrée]           # Lance directement (option par défaut)

# 6. Pendant l'exécution:
# - Appuyer sur 'j' pour activer/désactiver click_spam_macro
# - Appuyer sur 'k' pour activer/désactiver combat_macro
# - Appuyer sur 'Echap' une fois pour arrêter toutes les macros
# - Appuyer sur 'Echap' deux fois pour retourner au menu
# - Appuyer sur '/' pour recharger les macros après modification du code
# - Appuyer sur '~' pour modifier le kit
```

### Comportement de la touche Echap
```bash
# Scénario 1 : Macros actives
# - Vous avez lancé 2 macros (j et k)
# - 1er Echap : Arrête les 2 macros → Vous restez dans le kit
# - 2ème Echap : Retour au menu principal

# Scénario 2 : Aucune macro active
# - Vous êtes dans le kit mais aucune macro ne tourne
# - 1er Echap : Retour direct au menu principal

# Scénario 3 : Arrêt accidentel évité
# - Macro en cours d'exécution importante
# - Vous appuyez sur Echap par réflexe
# - Résultat : Macro arrêtée MAIS vous restez dans le kit
# - Vous pouvez relancer immédiatement sans tout refaire !
```

### Workflow de développement rapide
```bash
# Vous voulez modifier une macro sans redémarrer le programme

# 1. Lancer votre kit
python main.py → 2 → 1 → [Entrée]

# 2. Tester la macro
j → La macro tourne

# 3. Vous voyez un problème, arrêter
Echap (1er fois → Arrête la macro)

# 4. Modifier le code de la macro dans votre éditeur
# Exemple: Changer un délai de 1s à 0.5s dans click_spam_macro.py

# 5. Recharger les macros (sans quitter le programme)
/

# 6. Tester à nouveau
j → La macro tourne avec les changements !

# Plus besoin de quitter et relancer le programme !
```

### Créer une nouvelle macro

```bash
# Créer un fichier dans macros/
touch macros/ma_macro.py
```

Copier le format standard et personnaliser la section entre les délimiteurs

## 📦 Installation
```bash
pip install pynput pydirectinput
```

## ✨ Fonctionnalités

### Système de Kit
- ✅ Combinaison de plusieurs macros dans un kit
- ✅ Touches d'activation personnalisables pour chaque macro
- ✅ Exécution simultanée de plusieurs macros
- ✅ Sauvegarde/chargement des kits (JSON)
- ✅ Menu interactif de gestion des kits
- ✅ Modification des kits à la volée (touche '~')
- ✅ Affichage du statut en temps réel
- ✅ **Echap intelligent** : 1er appui = arrête les macros, 2ème appui = retour au menu (évite les sorties accidentelles)
- ✅ **Hot-reload avec '/'** : Recharge les macros sans redémarrer le programme (développement rapide)

### Macros
- ✅ Macros modulaires dans des fichiers séparés
- ✅ Toggle ON/OFF indépendant pour chaque macro
- ✅ **Arrêt immédiat** : Les macros s'arrêtent instantanément (< 50ms) lors de l'appui sur Echap ou toggle
- ✅ **Désactivation automatique** : Les macros "one-shot" se désactivent automatiquement à la fin (pas besoin de double appui)
- ✅ Boucle infinie jusqu'à désactivation ou exécution unique
- ✅ Compatible jeux (PyDirectInput)
- ✅ Format standardisé facile à dupliquer
- ✅ Messages console avec nom de la macro
- ✅ Fonction `sleep_interruptible()` pour des sleeps interruptibles

## 🔍 Gestion des erreurs

Le `main.py` gère:
- Dossier `macros/` introuvable → message d'erreur et arrêt
- Aucune macro disponible → message d'erreur et arrêt
- Erreur lors du chargement d'une macro → message détaillé
- Kit vide lors du lancement → demande d'ajouter des macros
- Touche déjà utilisée dans un kit → refus et message
- Erreur lors de la sauvegarde/chargement JSON → gestion gracieuse

## 📝 Exemples de macros à créer

### macros/exemple_macro.py
Macro simple qui appuie sur espace toutes les secondes

### macros/farming_macro.py
Macro pour farmer des ressources dans un jeu

### macros/combat_macro.py
Macro pour combattre automatiquement

## 🔧 Template de nouvelle macro

Chaque nouveau fichier dans `macros/` suit exactement le même format avec:
1. Docstring descriptive
2. Imports (pydirectinput, time)
3. Fonction `executer_macro(get_active_status)`
4. Boucle while avec vérification du statut
5. Section délimitée pour le code personnalisé
6. Messages de début/fin

## 📦 Exemples de Kits

### Kit "donut_smp"
Kit pour farming automatique avec deux macros:
```json
{
  "nom": "donut_smp",
  "macros": [
    ["click_spam_macro", "j"],
    ["sequence_1to9_macro", "k"]
  ]
}
```
- **Touche 'j'**: Active le spam de clics
- **Touche 'k'**: Active la séquence 1-9

### Kit "combat_smp"
Kit pour combat automatique:
```json
{
  "nom": "combat_smp",
  "macros": [
    ["combat_macro", "q"]
  ]
}
```
- **Touche 'q'**: Active la macro de combat

### Créer un kit personnalisé
1. Lancer `python main.py`
2. Choisir "1. Créer un nouveau kit"
3. Nommer le kit (ex: "mon_kit_perso")
4. Ajouter les macros avec leurs touches
5. Sauvegarder avec l'option 4
6. Le kit sera disponible dans `kits.json`