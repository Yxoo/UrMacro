"""
DEMO — Lecture de pixels & couleurs
=====================================
Présente les fonctionnalités pixel/écran de macro_api :
  - get_pixel_color     → lit la couleur d'un pixel (R, G, B)
  - check_pixel_color   → vérifie une couleur avec tolérance
  - find_color          → cherche une couleur dans une zone
  - find_color_bounds   → trouve le rectangle englobant d'une zone colorée
  - screenshot_region   → capture une zone de l'écran (retourne image PIL)

La macro lit des pixels pendant quelques secondes sans rien modifier.
"""

from urmacro import *


SAMPLE_DURATION = 8     # secondes de lecture continue
SAMPLE_INTERVAL = 0.5   # intervalle entre chaque lecture


def executer_macro(get_active_status):

    sw, sh = get_screen_size()
    print(f"  Résolution détectée : {sw}x{sh}")

    # ── 1. Lecture continue de la couleur sous le curseur ───────────────────
    print(f"\n  [1] Lecture de la couleur sous le curseur ({SAMPLE_DURATION}s)")
    print("       (déplacez la souris pour voir les valeurs changer)")
    import time
    end = time.perf_counter() + SAMPLE_DURATION
    prev_color = None
    while time.perf_counter() < end:
        if not get_active_status(): return
        x, y = get_cursor_pos()
        color = get_pixel_color(x, y)
        if color and color != prev_color:
            r, g, b = color
            # Estimation de la couleur dominante
            dominant = "rouge" if r > g and r > b else ("vert" if g > r and g > b else "bleu")
            print(f"     ({x:4d}, {y:4d}) → RGB({r:3d}, {g:3d}, {b:3d})  [{dominant}]")
            prev_color = color
        if not sleep_interruptible(SAMPLE_INTERVAL, get_active_status): return

    # ── 2. check_pixel_color avec tolérance ─────────────────────────────────
    print("\n  [2] check_pixel_color — vérification avec tolérance")
    x, y = get_cursor_pos()
    color = get_pixel_color(x, y)
    if color:
        r, g, b = color
        # Test avec tolérance 0 (exact)
        exact = check_pixel_color(x, y, r, g, b, tolerance=0)
        # Test avec tolérance 20 (permissif)
        loose = check_pixel_color(x, y, r, g, b, tolerance=20)
        # Test avec une couleur complètement fausse
        wrong = check_pixel_color(x, y, 0, 255, 0, tolerance=5)
        print(f"     Pixel en ({x}, {y}) = RGB({r}, {g}, {b})")
        print(f"     check exact (tol=0)        : {exact}")   # True
        print(f"     check permissif (tol=20)   : {loose}")   # True
        print(f"     check faux vert (tol=5)    : {wrong}")   # False (sauf si pixel vert)

    if not sleep_interruptible(0.5, get_active_status): return

    # ── 3. find_color — cherche une couleur dans un quart de l'écran ────────
    print("\n  [3] find_color — recherche d'une couleur dans une zone")
    x, y = get_cursor_pos()
    color = get_pixel_color(x, y)
    if color:
        r, g, b = color
        zone_x, zone_y = sw // 4, sh // 4
        zone_w, zone_h = sw // 2, sh // 2
        print(f"     Recherche de RGB({r}, {g}, {b}) dans la zone centrale ({zone_w}x{zone_h}px)...")
        result = find_color(zone_x, zone_y, zone_w, zone_h, r, g, b, tolerance=15)
        if result:
            print(f"     Trouvé en ({result[0]}, {result[1]})")
        else:
            print("     Non trouvé dans cette zone (essayez de placer le curseur sur une couleur visible)")

    if not sleep_interruptible(0.5, get_active_status): return

    # ── 4. find_color_bounds — bounding box d'une zone colorée ──────────────
    print("\n  [4] find_color_bounds — rectangle englobant autour de la couleur")
    x, y = get_cursor_pos()
    bounds = find_color_bounds(sw // 4, sh // 4, sw // 2, sh // 2, x, y, tolerance=20)
    if bounds:
        bx1, by1, bx2, by2 = bounds
        bw = bx2 - bx1
        bh = by2 - by1
        cx_b, cy_b = get_zone_center(bx1, by1, bx2, by2)
        print(f"     Zone colorée : ({bx1}, {by1}) → ({bx2}, {by2})  taille={bw}x{bh}px")
        print(f"     Centre de la zone : ({cx_b}, {cy_b})")
    else:
        print("     Aucune zone trouvée")

    if not sleep_interruptible(0.5, get_active_status): return

    # ── 5. screenshot_region — capture PIL d'une zone ───────────────────────
    print("\n  [5] screenshot_region — capture d'une zone (100x100px sous le curseur)")
    x, y = get_cursor_pos()
    img = screenshot_region(x - 50, y - 50, 100, 100)
    print(f"     Image capturée : {img.size} pixels, mode={img.mode}")
    # Exemple : sauvegarder localement (commenté par défaut)
    # img.save("demo_capture.png")

    print("\n  Demo pixel terminée.")
