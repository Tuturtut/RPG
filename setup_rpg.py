
#!/usr/bin/env python3

"""
Minimal project bootstrapper for your RPG repo.

Usage (from the root of your repo):
    python setup_rpg.py [--with-textual | --no-textual] [--install] [--commit] [--force]

Defaults:
    --with-textual   (enabled)
    --install        (disabled)
    --commit         (disabled)
    --force          (disabled: won't overwrite existing files)

What it does (minimal):
- Creates src/ layout and a tiny app (Textual if requested)
- Writes a minimal pyproject.toml
- Writes .gitignore and README.md (if missing)
- Optionally installs deps and makes an initial commit

Safe for a repo that already exists (it won't overwrite files unless --force).
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path
from typing import Iterable


def write_file(path: Path, content: str, force: bool = False) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and not force:
        print(f"[skip] {path} (exists)")
        return
    path.write_text(content, encoding="utf-8")
    print(f"[write] {path}")


def run(cmd: Iterable[str]) -> int:
    print(f"[run] {' '.join(cmd)}")
    try:
        return subprocess.call(list(cmd), shell=False)
    except FileNotFoundError:
        print(f"[warn] Command not found: {cmd!r}")
        return 127


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--with-textual", dest="with_textual", action="store_true", default=True)
    ap.add_argument("--no-textual", dest="with_textual", action="store_false")
    ap.add_argument("--install", action="store_true", default=False, help="pip install runtime deps")
    ap.add_argument("--commit", action="store_true", default=False, help="git add/commit after generating")
    ap.add_argument("--force", action="store_true", default=False, help="overwrite existing files")
    args = ap.parse_args()

    root = Path.cwd()
    src_root = root / "src"
    pkg_root = src_root / "rpg"

    # Minimal files
    pyproject = f"""
[project]
name = "rpg"
version = "0.1.0"
requires-python = ">=3.11"
description = "Minimal RPG starter"
readme = "README.md"
dependencies = [{('"textual>=0.58.0"') if args.with_textual else ''}]
{'' if args.with_textual else '# Tip: add textual later with: pip install textual'}

[tool.black]
line-length = 100
target-version = ["py311"]

[tool.ruff]
line-length = 100
target-version = "py311"
select = ["E","F","I","N","UP","B","SIM","PL"]
ignore = ["E203"]

[tool.mypy]
python_version = "3.11"
strict = true
warn_unused_ignores = true
disallow_untyped_defs = true
mypy_path = ["src"]
""".strip() + "\n"

    gitignore = """
.venv/
__pycache__/
*.pyc
.mypy_cache/
.pytest_cache/
.cache/
dist/
build/
*.log
""".lstrip()

    readme = """
# RPG — minimal starter

## Setup
```powershell
python -m venv .venv
# Windows
.\\.venv\\Scripts\\Activate
# macOS/Linux
# source .venv/bin/activate

# install runtime (created by this script if you use --install)
pip install -e .
```

## Run
```powershell
python -m rpg.ui.textual.app
```
""".lstrip()

    init_py = "__all__ = []\n"

    if args.with_textual:
        app_py = """
from __future__ import annotations
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static

class RPGApp(App):
    CSS_PATH = "styles.tcss"
    BINDINGS = [("q", "quit", "Quit")]

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Static("RPG (Textual) — Press Q to quit.", id="main")
        yield Footer()

if __name__ == "__main__":
    RPGApp().run()
""".lstrip()

        styles_tcss = """
Screen { background: black; color: white; }
#main { padding: 1 2; }
""".lstrip()
    else:
        # Provide a plain CLI placeholder
        app_py = """
def main() -> None:
    print("RPG CLI stub is running. (Add Textual later if you wish.)")

if __name__ == "__main__":
    main()
""".lstrip()
        styles_tcss = ""

    # Write files
    write_file(Path("pyproject.toml"), pyproject, args.force)
    write_file(Path(".gitignore"), gitignore, args.force)
    write_file(Path("README.md"), readme, args.force)

    write_file(pkg_root / "__init__.py", init_py, args.force)
    ui_root = pkg_root / "ui" / "textual"
    if args.with_textual:
        write_file(ui_root / "__init__.py", "", args.force)
        write_file(ui_root / "app.py", app_py, args.force)
        write_file(ui_root / "styles.tcss", styles_tcss, args.force)
    else:
        # CLI fallback
        write_file(pkg_root / "app.py", app_py, args.force)

    # Optional install
    if args.install:
        # Use current Python to install
        rc = run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
        if rc != 0:
            print("[warn] pip upgrade failed (continuing).")
        rc = run([sys.executable, "-m", "pip", "install", "-e", "."])
        if rc != 0:
            print("[error] pip install -e . failed.")
            return rc

    # Optional commit
    if args.commit:
        if (Path(".git") / "config").exists() or (Path(".git")).exists():
            run(["git", "add", "-A"])
            run(["git", "commit", "-m", "chore: bootstrap minimal RPG skeleton"])
        else:
            print("[warn] Not a git repo; skipping commit. (Run `git init` first.)")

    print("\nDone.")
    if args.with_textual:
        print("Run the app with:")
        print("  python -m rpg.ui.textual.app")
    else:
        print("Run the stub with:")
        print("  python -m rpg.app")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
