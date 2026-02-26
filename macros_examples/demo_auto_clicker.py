"""
DEMO — Auto-clicker configurable
==================================
Cas d'usage classique : clique à la position actuelle du curseur
à intervalle régulier jusqu'à ce que la macro soit désactivée.

Montre l'utilisation correcte de sleep_interruptible pour un
arrêt immédiat sans bloquer le thread.

Configuration :
  CLICK_INTERVAL  → délai entre chaque clic (secondes)
  CLICK_BUTTON    → 'left' ou 'right'
  CLICK_HOLD_MS   → 0 = clic simple, > 0 = maintien en ms avant relâche
"""

from urmacro import *


CLICK_INTERVAL = 0.1    # secondes entre chaque clic (0.1 = 10 clics/s)
CLICK_BUTTON   = 'left' # 'left' ou 'right'
CLICK_HOLD_MS  = 0       # 0 = clic simple, ex: 50 = maintient 50ms


def executer_macro(get_active_status):
    count = 0
    print(f"  Auto-clicker démarré ({1 / CLICK_INTERVAL:.0f} clics/s, bouton={CLICK_BUTTON})")

    while get_active_status():

        # ── Clic simple ou maintenu ──────────────────────────────────────────
        if CLICK_BUTTON == 'left':
            if CLICK_HOLD_MS > 0:
                left_click(hold=True)
                if not sleep_interruptible(CLICK_HOLD_MS / 1000, get_active_status):
                    release_left_click(); return
                release_left_click()
            else:
                left_click()
        else:
            if CLICK_HOLD_MS > 0:
                right_click(hold=True)
                if not sleep_interruptible(CLICK_HOLD_MS / 1000, get_active_status):
                    release_right_click(); return
                release_right_click()
            else:
                right_click()

        count += 1

        # ── Log toutes les 50 clics ──────────────────────────────────────────
        if count % 50 == 0:
            x, y = get_cursor_pos()
            print(f"  {count} clics  (position actuelle : {x}, {y})")

        # ── Attente interruptible ────────────────────────────────────────────
        if not sleep_interruptible(CLICK_INTERVAL, get_active_status):
            return

    print(f"  Auto-clicker arrêté après {count} clics.")
