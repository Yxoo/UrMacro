# UrMacro

A modular macro system for Windows with a **kit** system — combine multiple macros with custom keybindings, run them simultaneously, and save your configurations.

Built on top of [urmacropkg](https://github.com/Yxoo/urmacropkg), a standalone Windows input API using `SendInput` / `win32` for real input events (compatible with games using DirectInput/raw input).

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
| `/` | Reload macros from disk (apply code changes without restarting) |
| `~` | Open kit editor without stopping |
| `Esc` | Stop active macros / Return to main menu |

---

## Writing a Macro

Create a `.py` file in the `macros/` folder. The full input API is automatically available — no import needed at runtime:

```python
from urmacro import *  # optional: for IDE autocomplete only

def executer_macro(get_active_status):
    while get_active_status():
        press('space')
        if not sleep_interruptible(1.0, get_active_status):
            return
```

The input API is provided by **[urmacropkg](https://github.com/Yxoo/urmacropkg)** — see that repository for the full API reference (keyboard, mouse, pixel, window, OCR).

---

## Build from Source

**Requirements:** Python 3.10+, [Inno Setup 6](https://jrsoftware.org/isdl.php) (for the installer)

```bash
git clone https://github.com/<user>/UrMacro.git
cd UrMacro

pip install -e "path/to/urmacropkg"
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
├── main.py
├── requirements.txt
├── src/
│   ├── core/            # Kit, KitRunner, MacroInstance, kit_manager
│   ├── ui/              # Interactive menus, cursor utility
│   └── utils.py
├── macros_examples/     # Example macros
├── tools/               # Build scripts & config
│   ├── build.bat
│   ├── build_installer.bat
│   ├── urmacro.spec
│   ├── installer.iss
│   └── icon.ico
└── docs/
```

---

## License

MIT — see [LICENSE](LICENSE)
