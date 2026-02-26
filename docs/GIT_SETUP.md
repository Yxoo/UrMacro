# Git Setup — Commandes à exécuter

Ce fichier liste toutes les commandes git à exécuter manuellement.
Le projet n'est pas encore un dépôt git (`git init` n'a pas été fait).

---

## 1. Créer le dépôt GitHub

1. Aller sur [github.com/new](https://github.com/new)
2. Nom suggéré : `UrMacro`
3. Visibilité : **Public** (projet open source)
4. Ne pas initialiser avec README/gitignore (on a déjà les nôtres)
5. Copier l'URL du dépôt (`https://github.com/<user>/UrMacro.git`)

---

## 2. Initialiser le dépôt local

```bash
cd "d:\=Dev\_Macros\custom_macros"

git init
git branch -M main
```

---

## 3. Premier commit

```bash
# Vérifier ce qui va être ajouté
# dist/, build/, installer_output/ ne doivent PAS apparaître
git status

git add .
git commit -m "Initial commit"
```

---

## 4. Connecter au dépôt GitHub et pousser

```bash
git remote add origin https://github.com/<user>/UrMacro.git
git push -u origin main
```

---

## 5. Publier un Release

Après avoir buildé avec `tools\build_installer.bat` :

1. Aller sur `https://github.com/<user>/UrMacro/releases/new`
2. **Tag** : `v1.0.0` — doit correspondre exactement à la version dans :
   - `tools/installer.iss` → `#define MyAppVersion "1.0.0"`
   - `src/core/updater.py` → `VERSION = "1.0.0"` (quand créé)
3. **Title** : `v1.0.0 — Initial release`
4. Joindre **les deux fichiers** dans les assets :
   - `installer_output\UrMacro_Setup.exe` — installation complète (nouvel utilisateur)
   - `dist\UrMacro.exe` — exécutable seul (mise à jour légère via l'auto-updater)
5. Écrire les notes de version
6. Cliquer **Publish release**

> Le README pointe vers `releases/latest`.
> L'auto-updater télécharge uniquement `UrMacro.exe` — les macros et kits de l'utilisateur ne sont jamais touchés.

---

## 6. Workflow quotidien

```bash
git status
git add src/core/kit_runner.py
git commit -m "feat: rechargement automatique des macros"
git push
```

**Conventions de messages :**
```
feat: nouvelle fonctionnalité
fix: correction de bug
perf: optimisation
refactor: restructuration sans changement de comportement
docs: documentation
```

---

## 7. Publier une nouvelle version

```bash
# 1. Incrémenter la version dans :
#      tools/installer.iss  → #define MyAppVersion "1.x.x"
#      src/core/updater.py  → VERSION = "1.x.x"
# 2. Commiter
git add tools/installer.iss src/core/updater.py
git commit -m "chore: bump version 1.x.x"
git push

# 3. Tagger
git tag v1.1.0
git push origin v1.1.0
```

Puis créer un nouveau Release sur GitHub et attacher `UrMacro.exe` + `UrMacro_Setup.exe`.

---

## 8. Structure du projet (référence)

```
UrMacro/
├── main.py
├── src/
│   ├── core/           (Kit, KitRunner, MacroInstance, kit_manager)
│   ├── ui/             (menu, cursor_utility)
│   └── utils.py
├── macros_examples/    (macros de démonstration)
├── tools/
│   ├── build.bat               (exe uniquement)
│   ├── build_installer.bat     (exe + installateur Inno Setup)
│   ├── urmacro.spec
│   └── installer.iss
└── docs/
```

**Package séparé :** `urmacropkg` → `D:\=Dev\_Packages\urmacropkg`
Installable via `pip install -e "D:\=Dev\_Packages\urmacropkg"` en local,
ou `pip install urmacropkg` une fois publié sur PyPI.

---

## 9. Commandes utiles

```bash
git log --oneline
git diff
git restore src/core/kit_runner.py
git revert <hash>
```
