# Guide de l'API Input - src/input_api.py

API simplifiée pour créer des macros facilement, sans manipuler directement win32.

## Import

```python
from src.input_api import (
    focus_window,
    move,
    left_click, right_click,
    release_left_click, release_right_click,
    press, release, release_all,
    write
)
```

---

## Gestion des fenêtres

### `focus_window(title, partial=True)`

Met le focus sur une fenêtre.

**Paramètres :**
- `title` : Titre de la fenêtre (ou partie du titre si partial=True)
- `partial` : Si True, cherche les fenêtres qui CONTIENNENT le titre

**Retour :** `True` si succès, `False` sinon

**Exemples :**
```python
# Recherche partielle (par défaut)
focus_window("Notepad")  # Trouve "Sans titre - Bloc-notes"

# Recherche exacte
focus_window("Sans titre - Bloc-notes", partial=False)
```

---

## Souris - Mouvement

### `move(x, y)`

Déplace la souris à des coordonnées spécifiques.

**Paramètres :**
- `x` : Position X à l'écran (en pixels)
- `y` : Position Y à l'écran (en pixels)

**Exemples :**
```python
# Déplacer la souris
move(100, 200)

# Déplacer puis cliquer
move(1033, 446)
left_click()

# Déplacer et maintenir clic
move(500, 300)
left_click(hold=True)
```

---

## Souris - Clics

### `left_click(hold=False)`

Clic gauche.

**Paramètres :**
- `hold` : Si `True`, maintient le clic. Si `False`, clic simple.

**Exemples :**
```python
# Clic simple
left_click()

# Maintenir le clic
left_click(hold=True)
```

### `right_click(hold=False)`

Clic droit.

**Paramètres :**
- `hold` : Si `True`, maintient le clic. Si `False`, clic simple.

**Exemples :**
```python
# Clic simple
right_click()

# Maintenir le clic
right_click(hold=True)
```

### `release_left_click()`

Relâche le clic gauche s'il est maintenu.

### `release_right_click()`

Relâche le clic droit s'il est maintenu.

---

## Clavier - Touches

### `press(key, hold=False)`

Appuie sur une touche.

**Paramètres :**
- `key` : La touche à presser (voir liste ci-dessous)
- `hold` : Si `True`, maintient la touche. Si `False`, appui simple.

**Touches supportées :**

#### Lettres
```python
press('a')  # Minuscule
press('A')  # Majuscule
press('z')
press('Z')
```

#### Chiffres
```python
press('0')
press('1')
press('9')
```

#### Touches spéciales
```python
press('esc')       # ou 'escape'
press('enter')     # ou 'return'
press('space')
press('tab')
press('shift')
press('ctrl')      # ou 'control'
press('alt')
press('backspace')
press('delete')
```

#### Flèches
```python
press('up')
press('down')
press('left')
press('right')
```

#### Touches F
```python
press('f1')
press('f2')
press('f12')
```

#### Caractères spéciaux
```python
press('/')   # Slash
press('\\')  # Backslash
press('.')   # Point
press(',')   # Virgule
press(';')   # Point-virgule
press(':')   # Deux-points
press('!')   # Exclamation
press('?')   # Point d'interrogation
press('-')   # Tiret
press('_')   # Underscore
press('+')   # Plus
press('=')   # Égal
press('*')   # Astérisque
press('&')   # Et commercial
press('%')   # Pourcentage
press('$')   # Dollar
press('#')   # Dièse
press('@')   # Arobase
press('(')   # Parenthèse ouvrante
press(')')   # Parenthèse fermante
press('[')   # Crochet ouvrant
press(']')   # Crochet fermant
press('{')   # Accolade ouvrante
press('}')   # Accolade fermante
press('<')   # Inférieur
press('>')   # Supérieur
press('|')   # Pipe
press('"')   # Guillemet double
press("'")   # Guillemet simple
press('`')   # Accent grave
press('~')   # Tilde
press('^')   # Circonflexe
```

**Exemples :**
```python
# Appui simple
press('a')
press('esc')
press('enter')

# Maintenir une touche
press('shift', hold=True)
press('a')  # Écrit 'A' majuscule
release('shift')
```

### `release(key)`

Relâche une touche si elle est maintenue.

**Exemples :**
```python
press('ctrl', hold=True)
press('c')  # Copier
release('ctrl')
```

### `release_all()`

Relâche **toutes** les touches et clics maintenus. Très utile à la fin d'une macro.

**Exemple :**
```python
# À la fin de votre macro
release_all()
```

### `write(text, delay=0.05)`

Écrit une chaîne de caractères.

**Paramètres :**
- `text` : Le texte à écrire
- `delay` : Délai entre chaque caractère (en secondes)

**Exemples :**
```python
write("Bonjour")
write("Hello World", delay=0.1)  # Plus lent
```

---

## Exemples complets

### Exemple 1 : Focus + ESC + Maintien clics

```python
from src.utils import sleep_interruptible
from src.input_api import focus_window, press, left_click, right_click, release_all

def executer_macro(get_active_status):
    # Focus
    focus_window("Mon Jeu")

    # ESC
    press('esc')

    # Maintenir clic gauche
    left_click(hold=True)

    # Spam clic droit
    while get_active_status():
        right_click()  # Clic simple
        sleep_interruptible(0.01, get_active_status)

    # Tout relâcher
    release_all()
```

### Exemple 2 : Spam de touches

```python
from src.utils import sleep_interruptible
from src.input_api import focus_window, press

def executer_macro(get_active_status):
    focus_window("Notepad")

    while get_active_status():
        press('a')
        sleep_interruptible(0.5, get_active_status)
```

### Exemple 3 : Écrire du texte

```python
from src.input_api import focus_window, write

def executer_macro(get_active_status):
    focus_window("Notepad")
    write("Ceci est un test automatique")
```

### Exemple 4 : Combinaisons de touches

```python
from src.input_api import focus_window, press, release
import time

def executer_macro(get_active_status):
    focus_window("Notepad")

    # Ctrl+A (sélectionner tout)
    press('ctrl', hold=True)
    press('a')
    release('ctrl')

    time.sleep(0.1)

    # Ctrl+C (copier)
    press('ctrl', hold=True)
    press('c')
    release('ctrl')
```

### Exemple 5 : Farming avec clics alternés

```python
from src.utils import sleep_interruptible
from src.input_api import focus_window, left_click, right_click

def executer_macro(get_active_status):
    focus_window("Mon Jeu")

    while get_active_status():
        left_click()   # Clic gauche
        sleep_interruptible(0.5, get_active_status)
        right_click()  # Clic droit
        sleep_interruptible(0.5, get_active_status)
```

### Exemple 6 : Cliquer à des positions spécifiques

```python
from src.utils import sleep_interruptible
from src.input_api import focus_window, move, left_click

def executer_macro(get_active_status):
    focus_window("Mon Jeu")

    # Liste de positions à cliquer
    positions = [
        (100, 200),
        (500, 300),
        (1033, 446),
    ]

    while get_active_status():
        for x, y in positions:
            move(x, y)  # Déplacer la souris
            left_click()  # Cliquer
            sleep_interruptible(0.5, get_active_status)
```

### Exemple 7 : Pattern de mouvement + clic

```python
from src.utils import sleep_interruptible
from src.input_api import focus_window, move, left_click, right_click

def executer_macro(get_active_status):
    focus_window("Mon Jeu")

    # Déplacer à une position et maintenir clic gauche
    move(500, 400)
    left_click(hold=True)

    # Spam clic droit à une autre position
    move(600, 500)
    while get_active_status():
        right_click()
        sleep_interruptible(0.1, get_active_status)

    # Relâcher tout à la fin
    release_all()
```

---

## Différences avec pydirectinput

| Fonctionnalité | pydirectinput | input_api |
|----------------|---------------|-----------|
| Focus fenêtre | ❌ Non | ✅ `focus_window()` |
| Mouvement souris | ✅ `moveTo()` | ✅ `move()` |
| Clics simples | ✅ | ✅ |
| Maintenir clics | ❌ Complexe | ✅ `hold=True` |
| Touches simples | ✅ | ✅ |
| Maintenir touches | ❌ Complexe | ✅ `hold=True` |
| Relâcher tout | ❌ Manuel | ✅ `release_all()` |
| Syntaxe | Complexe | Simple |

---

## Bonnes pratiques

### 1. Toujours relâcher à la fin

```python
def executer_macro(get_active_status):
    try:
        # Votre code ici
        left_click(hold=True)
        # ...
    finally:
        # Assure que tout est relâché même si erreur
        release_all()
```

### 2. Utiliser sleep_interruptible

```python
# ✅ BON - Réactif à l'arrêt
from src.utils import sleep_interruptible

while get_active_status():
    right_click()
    sleep_interruptible(0.01, get_active_status)

# ❌ MAUVAIS - Pas réactif
import time

while get_active_status():
    right_click()
    time.sleep(0.01)  # Macro lente à s'arrêter
```

### 3. Vérifier le focus avant d'agir

```python
def executer_macro(get_active_status):
    if not focus_window("Mon Jeu"):
        print("   ❌ Impossible de trouver la fenêtre")
        return

    # Continue seulement si focus réussi
    press('esc')
    # ...
```

---

## Troubleshooting

### "Rien ne se passe"
- Vérifiez que `focus_window()` retourne `True`
- Vérifiez le titre exact avec `python macros/list_windows.py`

### "Les clics ne relâchent pas"
- Appelez `release_all()` à la fin de votre macro
- Utilisez `try/finally` pour garantir le relâchement

### "Caractères non supportés dans write()"
- `write()` supporte : a-z, A-Z, 0-9 et tous les caractères spéciaux (/, \, ., etc.)
- Si un caractère ne fonctionne pas, utilisez `press()` directement

---

## Résumé API

```python
# FENÊTRES
focus_window(title, partial=True)

# SOURIS - MOUVEMENT
move(x, y)

# SOURIS - CLICS
left_click(hold=False)
right_click(hold=False)
release_left_click()
release_right_click()

# CLAVIER
press(key, hold=False)
release(key)
write(text, delay=0.05)

# UTILITAIRE
release_all()  # Relâche TOUT
```

Utilisez cette API dans toutes vos macros pour un code simple et lisible !
