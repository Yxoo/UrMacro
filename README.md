# UrMacro

A modular macro system for Windows with a **kit** system — combine multiple macros with custom keybindings, run them simultaneously, and save your configurations.

Built on top of a custom input API using `SendInput` / `win32` for real input events (compatible with games using DirectInput/raw input).

---

## Download & Install

> **Download the latest installer from [Releases](../../releases/latest)**

1. Download `UrMacro_Setup.exe`
2. Run the installer — it creates a shortcut on your desktop
3. Launch **UrMacro**
4. Drop your macro files (`.py`) into the `macros/` folder next to the exe

No Python required to run the installed version.

---

## What is a Kit?

A **kit** is a collection of macros, each assigned to a hotkey. You can run multiple macros at the same time:

```
Kit "My Setup"
├─ [j] farming_macro      (runs in background)
├─ [k] combat_macro       (runs in background)
└─ [l] click_spam_macro   (runs in background)
```

Press the assigned key to toggle each macro on/off independently.

---

## Usage

```
1. Create a new kit       — name it, add macros with keybindings
2. Load a saved kit       — reload a previous configuration
0. Manage saved kits      — rename, delete saved kits
```

**While a kit is running:**

| Key | Action |
|-----|--------|
| Assigned keys (j, k...) | Toggle the corresponding macro on/off |
| `~` | Open kit editor without stopping |
| `Esc` | Return to main menu |

---

## Writing a Macro

Create a `.py` file in the `macros/` folder:

```python
from macro_api import *

def executer_macro(get_active_status):
    while get_active_status():

        press('space')
        if not sleep_interruptible(1.0, get_active_status):
            return

```

The `macro_api` module is available next to the exe and provides:

| Function | Description |
|----------|-------------|
| `press(key)` | Press a key (`'a'`, `'f1'`, `'enter'`, `'space'`...) |
| `press(key, hold=True)` / `release(key)` | Hold / release a key |
| `left_click()` / `right_click()` | Mouse clicks |
| `smooth_move(x, y, duration)` | Smooth mouse movement (Bezier curve) |
| `send_input_delta(dx, dy)` | Raw relative mouse movement (for game cameras) |
| `focus_window(title)` | Bring a window to foreground |
| `get_pixel_color(x, y)` | Read pixel color |
| `check_pixel_color(x, y, r, g, b, tolerance)` | Pixel color check with tolerance |
| `find_color(x, y, w, h, r, g, b)` | Search for a color in a region |
| `sleep_interruptible(seconds, get_active_status)` | Interruptible sleep — returns `False` if macro is stopped |
| `release_all()` | Release all held keys and clicks |

See [docs/INPUT_API_GUIDE.md](docs/INPUT_API_GUIDE.md) for the full API reference.

---

## Build from Source

**Requirements:** Python 3.10+, [Inno Setup 6](https://jrsoftware.org/isdl.php) (for the installer)

```bash
git clone https://github.com/<user>/urmacro.git
cd urmacro
pip install -r requirements.txt

# Run from source
python main.py

# Build standalone exe
tools\build.bat

# Build exe + installer
tools\build_installer.bat
```

---

## Project Structure

```
UrMacro/
├── main.py              # Entry point
├── macro_api.pyi        # Type stubs (IDE autocomplete)
├── requirements.txt
├── src/                 # Core engine
│   ├── input_api.py     # Mouse, keyboard, window API
│   ├── macro_api.py     # Public macro API
│   ├── utils.py         # sleep_interruptible
│   ├── kit.py           # Kit data model
│   ├── kit_runner.py    # Kit execution engine
│   ├── kit_manager.py   # Save / load kits
│   └── menu.py          # Interactive menus
├── macros/              # Example macros
├── tools/               # Build scripts & config
│   ├── build.bat
│   ├── build_installer.bat
│   ├── urmacro.spec
│   ├── installer.iss
│   └── icon.ico
└── docs/                # Documentation
```

---

## License

MIT — see [LICENSE](LICENSE)
