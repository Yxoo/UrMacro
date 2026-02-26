"""
DEMO — Suivi de couleur
=========================
Démo avancée combinant pixel + souris :
  1. Lit la couleur sous le curseur au démarrage
  2. Cherche continuellement cette couleur sur l'écran
  3. Déplace le curseur vers la zone trouvée avec smooth_move

Cas d'usage : suivre un objet coloré dans une vidéo, une interface,
ou détecter la présence d'un élément visuel précis.

Configuration :
  SCAN_TOLERANCE  → marge de couleur acceptable (0 = exact, 30 = permissif)
  SCAN_STEP       → pas de scan en pixels (5 = précis mais lent, 20 = rapide)
  MOVE_DURATION   → fluidité du déplacement vers la cible (secondes)
  FOLLOW_INTERVAL → délai entre chaque cycle de recherche
"""

from urmacro import *


SCAN_TOLERANCE  = 25
SCAN_STEP       = 8
MOVE_DURATION   = 0.15
FOLLOW_INTERVAL = 0.05


def executer_macro(get_active_status):

    # ── 1. Capture de la couleur cible sous le curseur ──────────────────────
    if not sleep_interruptible(0.5, get_active_status): return

    x, y = get_cursor_pos()
    target_color = get_pixel_color(x, y)

    if not target_color:
        print("  Erreur : impossible de lire la couleur sous le curseur.")
        return

    r, g, b = target_color
    print(f"  Couleur cible capturée : RGB({r}, {g}, {b}) en ({x}, {y})")
    print(f"  La macro va maintenant suivre cette couleur sur l'écran.")
    print(f"  (tolérance={SCAN_TOLERANCE}, step={SCAN_STEP}px)")

    sw, sh = get_screen_size()
    not_found_count = 0

    # ── 2. Boucle de suivi ───────────────────────────────────────────────────
    while get_active_status():

        # Scan de tout l'écran (sauf les bords de 50px)
        result = find_color(
            50, 50,
            sw - 100, sh - 100,
            r, g, b,
            tolerance=SCAN_TOLERANCE,
            x_step=SCAN_STEP,
            y_step=SCAN_STEP,
        )

        if result:
            not_found_count = 0
            tx, ty = result
            cx, cy = get_cursor_pos()

            # Ne bouger que si la cible est assez loin (évite le micro-tremblement)
            dist = abs(tx - cx) + abs(ty - cy)
            if dist > 15:
                smooth_move(tx, ty, duration=MOVE_DURATION)
                print(f"  → cible en ({tx}, {ty})  dist={dist}px")
        else:
            not_found_count += 1
            if not_found_count == 1:
                print(f"  Couleur RGB({r},{g},{b}) introuvable à l'écran...")
            if not_found_count > 20:
                print("  Couleur perdue depuis trop longtemps, arrêt.")
                return

        if not sleep_interruptible(FOLLOW_INTERVAL, get_active_status): return

    print("  Suivi de couleur arrêté.")
