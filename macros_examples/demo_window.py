"""
DEMO — Gestion de fenêtres
============================
Présente les fonctionnalités window de macro_api :
  - find_window   → cherche une fenêtre par titre (partial ou exact)
  - focus_window  → met au premier plan + optionnellement maximise
  - Lecture de pixel dans une fenêtre spécifique (coordonnées relatives)

Modifiez WINDOW_TITLE pour cibler n'importe quelle fenêtre ouverte.
Exemples : "Notepad", "Chrome", "Visual Studio Code", "Discord"
"""

from urmacro import *


WINDOW_TITLE = "Notepad"   # ← changez ici


def executer_macro(get_active_status):

    # ── 1. Recherche de fenêtre (partial match) ──────────────────────────────
    print(f"\n  [1] Recherche de fenêtres contenant '{WINDOW_TITLE}'")
    hwnd, title = find_window(WINDOW_TITLE, partial=True)

    if not hwnd:
        print(f"  Aucune fenêtre trouvée pour '{WINDOW_TITLE}'.")
        print("  Modifiez WINDOW_TITLE dans la macro et relancez.")
        return

    print(f"  Fenêtre trouvée : '{title}'  (hwnd={hwnd})")

    if not sleep_interruptible(0.5, get_active_status): return

    # ── 2. Focus simple (sans changer la taille) ────────────────────────────
    print("\n  [2] focus_window() — mise au premier plan")
    success = focus_window(WINDOW_TITLE, partial=True)
    print(f"  Résultat : {'OK' if success else 'Échec'}")

    if not sleep_interruptible(1.0, get_active_status): return

    # ── 3. Focus avec maximisation ───────────────────────────────────────────
    print("\n  [3] focus_window(full_scale=True) — mise au premier plan + maximisé")
    focus_window(WINDOW_TITLE, partial=True, full_scale=True)

    if not sleep_interruptible(1.0, get_active_status): return

    # ── 4. Lecture de pixel en coordonnées relatives à la fenêtre ────────────
    print("\n  [4] get_pixel_color relatif à la fenêtre (pixel en 10, 10 de la zone client)")
    color = get_pixel_color(10, 10, window_title=WINDOW_TITLE)
    if color:
        r, g, b = color
        print(f"  Couleur à (10, 10) dans '{title}' : RGB({r}, {g}, {b})")
    else:
        print("  Impossible de lire le pixel (fenêtre hors écran ?)")

    if not sleep_interruptible(0.5, get_active_status): return

    # ── 5. find_window exact vs partial ─────────────────────────────────────
    print("\n  [5] Différence partial=True vs partial=False")
    hwnd_partial, t1 = find_window(WINDOW_TITLE, partial=True)
    hwnd_exact,   t2 = find_window(WINDOW_TITLE, partial=False)
    print(f"  partial=True  : {'trouvé → ' + str(t1) if hwnd_partial else 'non trouvé'}")
    print(f"  partial=False : {'trouvé → ' + str(t2) if hwnd_exact  else 'non trouvé (titre exact requis)'}")

    print("\n  Demo fenêtres terminée.")
