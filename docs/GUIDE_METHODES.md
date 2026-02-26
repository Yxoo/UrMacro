# Guide : Quelle méthode utiliser ?

## Problème
"Si je ne suis pas sur la fenêtre, elle n'envoie pas les signaux dessus"

## Solution : Tester les 3 méthodes

J'ai créé `background_click_advanced.py` qui propose **3 méthodes différentes**.

## Les 3 méthodes expliquées

### Méthode 1 : PostMessage (la plus douce)
```python
METHOD = 1
```

**Comment ça marche :**
- Envoie des messages Windows asynchrones
- Ne bloque pas, la fenêtre n'a pas besoin d'être au focus
- La fenêtre traite le message quand elle peut

**Avantages :**
- ✅ Fenêtre peut rester en arrière-plan
- ✅ Votre souris reste libre
- ✅ Le plus léger en ressources

**Inconvénients :**
- ❌ Ne fonctionne PAS avec les jeux modernes (DirectX, OpenGL)
- ❌ Ignoré par beaucoup de jeux 3D
- ❌ Certaines applications filtrent ces messages

**Fonctionne avec :**
- Notepad, Calculator
- Jeux très anciens (DOS, Win95)
- Applications bureautiques

---

### Méthode 2 : SendMessage (plus forcée)
```python
METHOD = 2
```

**Comment ça marche :**
- Envoie des messages Windows synchrones
- **Bloque jusqu'à ce que** la fenêtre traite le message
- Plus "forcé" que PostMessage

**Avantages :**
- ✅ Fenêtre peut rester en arrière-plan
- ✅ Votre souris reste libre
- ✅ Plus fiable que PostMessage
- ✅ Meilleure garantie que le message est traité

**Inconvénients :**
- ❌ Toujours ignoré par les jeux DirectX/OpenGL modernes
- ❌ Peut bloquer la macro si la fenêtre ne répond pas
- ⚠️ Légèrement plus lent que PostMessage

**Fonctionne avec :**
- Tout ce qui fonctionne avec PostMessage
- Certains jeux 2D en mode fenêtré
- Applications qui traitent les messages Windows

---

### Méthode 3 : SetFocus + SendInput (focus temporaire)
```python
METHOD = 3
```

**Comment ça marche :**
- **Met la fenêtre au premier plan** temporairement
- Envoie les inputs via SendInput (comme si vous cliquiez vraiment)
- La fenêtre revient ensuite en arrière-plan

**Avantages :**
- ✅ Fonctionne avec BEAUCOUP plus de jeux
- ✅ Compatible DirectX/OpenGL
- ✅ Simule de vrais inputs hardware

**Inconvénients :**
- ❌ La fenêtre "flashe" au premier plan à chaque input
- ❌ Peut être gênant visuellement
- ❌ Votre souris reste libre MAIS la fenêtre prend le focus
- ⚠️ Certains anti-triche détectent SetForegroundWindow

**Fonctionne avec :**
- La plupart des jeux modernes en mode fenêtré
- Jeux Steam récents
- Émulateurs

---

## Comment tester ?

### Test rapide avec Notepad

1. **Ouvrez Notepad** (Bloc-notes)

2. **Testez Méthode 1** :
   ```python
   WINDOW_TITLE = "Notepad"
   METHOD = 1
   ACTION = "SPAM_KEY"
   KEY_TO_SPAM = ord('A')
   KEY_SPAM_INTERVAL = 0.5
   ```
   - Lancez la macro
   - Mettez Chrome au premier plan
   - Notepad devrait se remplir de "A" en arrière-plan ✅

3. **Testez Méthode 2** :
   ```python
   METHOD = 2  # Changez juste ça
   ```
   - Même résultat que Méthode 1 avec Notepad

4. **Testez Méthode 3** :
   ```python
   METHOD = 3
   ```
   - Notepad va "flasher" au premier plan à chaque "A"
   - Visuellement plus gênant mais plus compatible

### Test avec votre jeu

1. **Lancez votre jeu en mode FENÊTRÉ** (pas fullscreen)

2. **Commencez par Méthode 2** (meilleur compromis) :
   ```python
   WINDOW_TITLE = "Titre exact de votre jeu"
   METHOD = 2
   ACTION = "SPAM_KEY"
   KEY_TO_SPAM = ord('E')
   KEY_SPAM_INTERVAL = 1.0
   ```

3. **Lancez la macro, puis mettez Chrome au premier plan**

4. **Observez le jeu** (visible en arrière si mode fenêtré) :
   - ✅ **Ça marche** : Le personnage appuie sur E → Utilisez Méthode 2
   - ❌ **Ça marche pas** : Rien ne se passe → Passez à Méthode 3

5. **Si Méthode 2 ne marche pas, essayez Méthode 3** :
   ```python
   METHOD = 3
   ```
   - Le jeu va flasher au premier plan
   - Mais les inputs devraient passer

## Pourquoi ça ne marche pas toujours ?

### Jeux modernes (DirectX/Vulkan)
```
Jeu moderne → DirectInput/RawInput → Lit directement depuis le hardware
              ↑
              Ignore les messages Windows (WM_KEYDOWN, etc.)
```

Ces jeux **ne lisent PAS** les messages Windows. Ils lisent directement le clavier/souris.

**Solutions :**
- Méthode 3 (SetFocus + SendInput) → Simule le hardware
- OU le jeu doit être au premier plan (macro classique)

### Jeux avec anti-triche
Certains jeux détectent :
- SetForegroundWindow appelé trop souvent
- Patterns d'inputs trop réguliers
- Messages Windows non-authentiques

**Solutions :**
- Ajouter des délais aléatoires
- Garder le jeu au premier plan
- Ne pas utiliser dans les jeux en ligne

### Jeux fullscreen exclusif
En mode fullscreen exclusif, le jeu a un accès direct au GPU.

**Solutions :**
- Passez en mode **Fenêtré** ou **Borderless Windowed**
- Dans les options graphiques du jeu

## Tableau récapitulatif

| Type de jeu/app | Méthode 1 | Méthode 2 | Méthode 3 |
|----------------|-----------|-----------|-----------|
| Notepad, Calculator | ✅ | ✅ | ✅ |
| Jeux DOS/anciens | ✅ | ✅ | ✅ |
| Jeux 2D simples | ⚠️ | ⚠️ | ✅ |
| Émulateurs | ❌ | ❌ | ✅ |
| Jeux DirectX (mode fenêtré) | ❌ | ❌ | ✅ |
| Jeux DirectX (fullscreen) | ❌ | ❌ | ❌ |
| Jeux avec anti-triche | ❌ | ❌ | ⚠️ |

## Réponse à votre question

> "Si je ne suis pas sur la fenêtre il n'envoie pas les signaux dessus"

**Cause probable :** Votre jeu utilise DirectInput et ignore les messages Windows.

**Solution :**
1. ✅ Essayez **Méthode 3** dans `background_click_advanced.py`
2. ✅ Mettez le jeu en mode **Fenêtré** (pas fullscreen)
3. ⚠️ Acceptez que la fenêtre flashe au premier plan
4. ❌ Si ça ne marche toujours pas : le jeu est incompatible avec cette approche

## Alternative ultime : Garder le jeu au premier plan

Si AUCUNE méthode ne marche, utilisez les macros classiques :
- `click_spam_macro.py`
- `sequence_1to9_macro.py`
- etc.

**Avantages :**
- ✅ Fonctionne avec 100% des jeux

**Inconvénients :**
- ❌ Le jeu doit rester au premier plan
- ❌ Votre souris/clavier est monopolisé

## Configuration recommandée

Pour la plupart des jeux modernes :

```python
# background_click_advanced.py

WINDOW_TITLE = "Votre Jeu"  # Titre exact

METHOD = 3  # ⭐ Commencez par là

ACTION = "SPAM_KEY"
KEY_TO_SPAM = ord('E')
KEY_SPAM_INTERVAL = 0.5
```

**Et surtout :** Mettez le jeu en **mode Fenêtré** !
