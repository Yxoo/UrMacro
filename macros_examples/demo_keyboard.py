"""
DEMO — Clavier
==============
Présente toutes les fonctionnalités clavier de macro_api :
  - Appui simple, touches spéciales, touches F
  - Combinaisons (Ctrl+C, Ctrl+V, Alt+Tab...)
  - Maintien / relâchement manuel
  - Écriture de texte Unicode

Pour tester : ouvrez un éditeur de texte (Notepad, VSCode...) et lancez la macro.
"""

from urmacro import *


DEMO_INTERVAL = 0.5   # secondes entre chaque démo


def executer_macro(get_active_status):

    # ── 1. Touches simples ───────────────────────────────────────────────────
    print("  [1] Touches simples : a b c espace entrée")
    for key in ['a', 'b', 'c', 'space', 'enter']:
        if not get_active_status(): return
        press(key)
        if not sleep_interruptible(0.15, get_active_status): return

    if not sleep_interruptible(DEMO_INTERVAL, get_active_status): return

    # ── 2. Touches directionnelles ───────────────────────────────────────────
    print("  [2] Flèches directionnelles")
    for key in ['up', 'down', 'left', 'right']:
        if not get_active_status(): return
        press(key)
        if not sleep_interruptible(0.15, get_active_status): return

    if not sleep_interruptible(DEMO_INTERVAL, get_active_status): return

    # ── 3. Touches F ─────────────────────────────────────────────────────────
    # Note : F5 = actualiser, F12 = devtools — commentez si gênant
    print("  [3] Touches F (F1 F2 F3)")
    for key in ['f1', 'f2', 'f3']:
        if not get_active_status(): return
        press(key)
        if not sleep_interruptible(0.2, get_active_status): return

    if not sleep_interruptible(DEMO_INTERVAL, get_active_status): return

    # ── 4. Combinaisons de touches (Ctrl+A, Ctrl+C) ──────────────────────────
    print("  [4] Ctrl+A  (tout sélectionner)")
    press('ctrl', hold=True)
    press('a')
    if not sleep_interruptible(0.05, get_active_status):
        release_all(); return
    release('ctrl')

    if not sleep_interruptible(DEMO_INTERVAL, get_active_status): return

    print("  [4] Ctrl+C  (copier)")
    press('ctrl', hold=True)
    press('c')
    if not sleep_interruptible(0.05, get_active_status):
        release_all(); return
    release('ctrl')

    if not sleep_interruptible(DEMO_INTERVAL, get_active_status): return

    # ── 5. Maintien d'une touche (Shift + lettres = majuscules) ──────────────
    print("  [5] Maintien Shift → majuscules")
    press('shift', hold=True)
    for key in ['h', 'e', 'l', 'l', 'o']:
        if not get_active_status():
            release_all(); return
        press(key)
        if not sleep_interruptible(0.1, get_active_status):
            release_all(); return
    release('shift')

    if not sleep_interruptible(DEMO_INTERVAL, get_active_status): return

    # ── 6. Écriture de texte Unicode ─────────────────────────────────────────
    print("  [6] Écriture Unicode (accents, symboles...)")
    write("Bonjour ! Voici du texte Unicode : éàü €£¥", delay=0.04)
    press('enter')

    if not sleep_interruptible(DEMO_INTERVAL, get_active_status): return

    print("  Demo clavier terminée.")
