
import importlib
import os
import subprocess
import sys
import venv
from pathlib import Path

# Package name, Python import name
required_packages = [
    ("requests", "requests"),
    ("Django", "django"),
    ("beautifulsoup4", "bs4"),
]

def package_installed(import_name):
    try:
        importlib.import_module(import_name)
        return True
    except ImportError:
        return False


def install_missing_packages():
    missing = [
        package
        for package, import_name in required_packages
        if not package_installed(import_name)
    ]

    if not missing:
        print("[SUCCESS] All required packages are installed.")
        return

    print("[INFO] Missing packages:", missing)

    # Do not modify Vercel's system Python.
    if os.environ.get("VERCEL"):
        raise RuntimeError(
            "Missing packages on Vercel. Install them through "
            "requirements.txt during the Vercel build."
        )

    # Local development: install into an isolated environment.
    env_dir = Path(__file__).resolve().parent.parent / ".venv"

    if not env_dir.exists():
        venv.EnvBuilder(with_pip=True).create(env_dir)

    if os.name == "nt":
        python_executable = env_dir / "Scripts" / "python.exe"
    else:
        python_executable = env_dir / "bin" / "python"

    subprocess.check_call([
        str(python_executable),
        "-m",
        "pip",
        "install",
        *missing
    ])

    print("[SUCCESS] Packages installed in:", env_dir)
    print("[INFO] Activate this environment and restart Django.")


for package_name, import_name in required_packages:
    if package_installed(import_name):
        print(f"[INSTALLED] {package_name}")
    else:
        print(f"[MISSING] {package_name}")

install_missing_packages()
