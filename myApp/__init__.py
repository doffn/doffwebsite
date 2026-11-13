
import importlib
import sys

# Required packages: (package name, Python import name)
required_packages = [
    ("time", "time"),
    ("requests", "requests"),
    ("os", "os"),
    ("django", "django"),
    ("beautifulsoup4", "bs4"),
    ("json", "json"),
]

# Check whether a package is installed
def package_installed(import_name):
    try:
        importlib.import_module(import_name)
        return True
    except ImportError:
        return False


# Check and report package status
def check_required_packages():
    missing_packages = []

    print("\n========== PACKAGE CHECK ==========")

    for package_name, import_name in required_packages:
        if package_installed(import_name):
            print(f"[INSTALLED] {package_name}")
        else:
            print(f"[MISSING]   {package_name}")
            missing_packages.append(package_name)

    print("===================================\n")

    if missing_packages:
        print("Missing packages:", ", ".join(missing_packages))
        print("Install them using requirements.txt.")
        return False

    print("All required packages are available.")
    return True


# Run package check
PACKAGES_OK = check_required_packages()
