"""
DEMO — Souris
=============
Présente toutes les fonctionnalités souris de macro_api :
  - move()           → déplacement instantané (SetCursorPos)
  - smooth_move()    → déplacement fluide avec courbe de Bézier
  - send_input_delta → mouvement relatif brut (caméras de jeu)
  - left_click / right_click avec hold
  - Tracé de motifs géométriques pour visualiser smooth_move

La macro ne clique nulle part de critique — elle dessine juste avec le curseur.
"""

from urmacro import *
import math


def executer_macro(get_active_status):

    sw, sh = get_screen_size()
    cx, cy = sw // 2, sh // 2   # centre de l'écran

    # ── 1. Déplacement instantané aux 4 coins ────────────────────────────────
    print("  [1] move() instantané → 4 coins")
    corners = [(100, 100), (sw - 100, 100), (sw - 100, sh - 100), (100, sh - 100)]
    for x, y in corners:
        if not get_active_status(): return
        move(x, y)
        if not sleep_interruptible(0.3, get_active_status): return

    if not sleep_interruptible(0.5, get_active_status): return

    # ── 2. smooth_move — aller-retour avec différentes vitesses ─────────────
    print("  [2] smooth_move() — vitesses variées")
    move(cx, cy)
    speeds = [
        (cx - 300, cy, 0.8, "lent (0.8s)"),
        (cx,       cy, 0.3, "moyen (0.3s)"),
        (cx + 300, cy, 0.1, "rapide (0.1s)"),
        (cx,       cy, 0.5, "retour (0.5s)"),
    ]
    for x, y, dur, label in speeds:
        if not get_active_status(): return
        print(f"     {label}")
        smooth_move(x, y, duration=dur)
        if not sleep_interruptible(0.2, get_active_status): return

    if not sleep_interruptible(0.5, get_active_status): return

    # ── 3. Tracé d'un cercle avec smooth_move ───────────────────────────────
    print("  [3] Tracé d'un cercle (smooth_move par segments)")
    radius = 200
    steps = 24
    move(cx + radius, cy)
    for i in range(1, steps + 1):
        if not get_active_status(): return
        angle = 2 * math.pi * i / steps
        tx = cx + int(radius * math.cos(angle))
        ty = cy + int(radius * math.sin(angle))
        smooth_move(tx, ty, duration=0.07)

    if not sleep_interruptible(0.5, get_active_status): return

    # ── 4. Clic simple gauche / droit ────────────────────────────────────────
    print("  [4] Clic gauche puis clic droit au centre")
    smooth_move(cx, cy, duration=0.3)
    if not sleep_interruptible(0.2, get_active_status): return
    left_click()
    if not sleep_interruptible(0.3, get_active_status): return
    right_click()
    if not sleep_interruptible(0.5, get_active_status): return

    # ── 5. Maintien clic gauche (drag simulation) ────────────────────────────
    print("  [5] Drag simulé : hold left_click + smooth_move")
    smooth_move(cx - 200, cy, duration=0.3)
    if not sleep_interruptible(0.1, get_active_status): return
    left_click(hold=True)
    smooth_move(cx + 200, cy, duration=0.8)
    if not sleep_interruptible(0.1, get_active_status): return
    release_left_click()

    if not sleep_interruptible(0.5, get_active_status): return

    # ── 6. send_input_delta — mouvement relatif brut ─────────────────────────
    # Utile pour les caméras de jeu (raw input / DirectInput)
    print("  [6] send_input_delta() — mouvement relatif (50px droite, 50px bas, retour)")
    send_input_delta(50, 0)
    if not sleep_interruptible(0.2, get_active_status): return
    send_input_delta(0, 50)
    if not sleep_interruptible(0.2, get_active_status): return
    send_input_delta(-50, -50)

    if not sleep_interruptible(0.3, get_active_status): return

    # ── 7. get_cursor_pos ────────────────────────────────────────────────────
    x, y = get_cursor_pos()
    print(f"  [7] Position finale du curseur : ({x}, {y})")

    print("  Demo souris terminée.")
