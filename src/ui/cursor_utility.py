"""
Utilitaire curseur - Inspecte le pixel sous le curseur en temps réel
"""

import ctypes
import ctypes.wintypes
import win32gui
from pynput import keyboard, mouse


def _inspect_pixel():
    """Récupère et affiche les infos du pixel sous le curseur"""
    # Position du curseur
    point = ctypes.wintypes.POINT()
    ctypes.windll.user32.GetCursorPos(ctypes.byref(point))
    x, y = point.x, point.y

    # Couleur du pixel
    hdc = ctypes.windll.user32.GetDC(0)
    color = ctypes.windll.gdi32.GetPixel(hdc, x, y)
    ctypes.windll.user32.ReleaseDC(0, hdc)

    if color < 0:
        print(f"  ({x}, {y})  |  Couleur: impossible à lire")
        return

    r = color & 0xFF
    g = (color >> 8) & 0xFF
    b = (color >> 16) & 0xFF
    hex_color = f"#{r:02X}{g:02X}{b:02X}"

    # Fenêtre sous le curseur
    hwnd = win32gui.WindowFromPoint((x, y))
    window_title = win32gui.GetWindowText(hwnd) if hwnd else "N/A"
    if not window_title:
        window_title = "(sans titre)"

    print(f"  XY: ({x}, {y})  |  RGB: ({r}, {g}, {b})  |  HEX: {hex_color}  |  Fenetre: {window_title}")


def run_cursor_utility():
    """Lance l'utilitaire curseur interactif"""
    print("\n" + "=" * 60)
    print("  UTILITAIRE CURSEUR")
    print("=" * 60)
    print("\n  Appuyez sur [E], [*] ou [Clic gauche] pour inspecter le pixel")
    print("  Appuyez sur [ESC] pour quitter\n")

    def on_key_press(key):
        try:
            # Touche 'e' ou 'E'
            if hasattr(key, 'char') and key.char and key.char.lower() == 'e':
                _inspect_pixel()
                return
            # Touche '*' (clavier principal)
            if hasattr(key, 'char') and key.char == '*':
                _inspect_pixel()
                return
        except AttributeError:
            pass

        # Numpad * (VK_MULTIPLY = 0x6A)
        if hasattr(key, 'vk') and key.vk == 0x6A:
            _inspect_pixel()
            return

        # ESC pour quitter
        if key == keyboard.Key.esc:
            print("\n  Utilitaire curseur ferme.")
            return False  # Stop listener

    def on_click(x, y, button, pressed):
        if pressed and button == mouse.Button.left:
            _inspect_pixel()

    # Lancer les listeners
    kb_listener = keyboard.Listener(on_press=on_key_press)
    mouse_listener = mouse.Listener(on_click=on_click)

    kb_listener.start()
    mouse_listener.start()

    # Attendre que le keyboard listener s'arrête (ESC)
    kb_listener.join()
    mouse_listener.stop()
