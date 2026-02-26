"""
Auto-updater — vérifie GitHub Releases et propose la mise à jour.
Télécharge uniquement UrMacro.exe, sans réinstaller.
"""

import sys
import os
import tempfile
import subprocess
import requests

VERSION = "1.0.0"
_GITHUB_API = "https://api.github.com/repos/Yxoo/UrMacro/releases/latest"
_EXE_ASSET  = "UrMacro.exe"


def _parse_version(v: str) -> tuple:
    return tuple(int(x) for x in v.lstrip('v').split('.'))


def _check() -> tuple | None:
    """Interroge l'API GitHub. Retourne (version, url) ou None."""
    try:
        resp = requests.get(_GITHUB_API, timeout=5)
        if resp.status_code != 200:
            return None
        data = resp.json()
        latest = data.get('tag_name', '').lstrip('v')
        if not latest or _parse_version(latest) <= _parse_version(VERSION):
            return None
        for asset in data.get('assets', []):
            if asset['name'] == _EXE_ASSET:
                return latest, asset['browser_download_url']
        return None
    except Exception:
        return None


def _download(url: str) -> str | None:
    """Télécharge l'exe dans un fichier temp. Retourne le chemin ou None."""
    try:
        resp = requests.get(url, stream=True, timeout=60)
        resp.raise_for_status()
        total = int(resp.headers.get('content-length', 0))
        done  = 0
        fd, tmp = tempfile.mkstemp(suffix='.exe', prefix='UrMacro_update_')
        os.close(fd)
        with open(tmp, 'wb') as f:
            for chunk in resp.iter_content(chunk_size=8192):
                f.write(chunk)
                done += len(chunk)
                if total:
                    print(f"\r  Téléchargement... {done * 100 // total}%", end='', flush=True)
        print()
        return tmp
    except Exception as e:
        print(f"\n  Erreur téléchargement : {e}")
        return None


def _launch_updater(tmp_exe: str) -> None:
    """
    Génère un .bat qui attend la fermeture du processus courant,
    remplace l'exe, puis relance la nouvelle version.
    """
    exe_path = sys.executable
    _, bat = tempfile.mkstemp(suffix='.bat', prefix='urmacro_upd_')
    os.close(_)

    with open(bat, 'w', encoding='ascii') as f:
        f.write(f"""@echo off
timeout /t 2 /nobreak > nul
move /y "{tmp_exe}" "{exe_path}"
if errorlevel 1 (
    echo Erreur : impossible de remplacer l'executable. Lancez en administrateur.
    pause
) else (
    start "" "{exe_path}"
)
del "%~f0"
""")

    subprocess.Popen(
        ['cmd', '/c', bat],
        creationflags=subprocess.CREATE_NEW_CONSOLE,
        close_fds=True,
    )
    sys.exit(0)


def prompt_update() -> None:
    """
    Vérifie la mise à jour au démarrage et propose à l'utilisateur.
    Ne fait rien si lancé depuis le source (hors exe compilé).
    """
    if not getattr(sys, 'frozen', False):
        return

    result = _check()
    if result is None:
        return

    version, url = result
    print(f"\n{'=' * 60}")
    print(f"  Nouvelle version disponible : v{VERSION}  →  v{version}")
    print(f"  Seul UrMacro.exe sera remplacé — vos macros et kits restent intacts.")
    print(f"{'=' * 60}")

    try:
        choix = input("  Mettre à jour maintenant ? [O/n] : ").strip().lower()
    except (EOFError, KeyboardInterrupt):
        return

    if choix not in ('', 'o', 'y'):
        return

    tmp = _download(url)
    if tmp:
        print("  Installation en cours...")
        _launch_updater(tmp)
