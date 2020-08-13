import subprocess
import sys
import get_pip
import os
import importlib
import contextlib

def install(package):
    """Installs a package using pip.
    Package must be a string.
    """
    subprocess.call([sys.executable, "-m", "pip", "install", package])

required = ["bs4", "chromedriver", "lxml", "openpyxl", "pandas", "PyQt5", \
    "PyQtWebEngine", "requests", "selenium", "sqlite3"]
failed = []

if len(required) > 0:
    print(f"You are about to install {len(required)}" + \
        " packages, would you like to proceed? (y/n):", end=" ")
    ans = input()

    if ans.lower() in ["y", "yes", "", " "]:
        for package in required:
            try:
                print("\n[LOG] Looking for ", package)
                with contextlib.redirect_stdout(None):
                    __import__(package)
                print(f"[LOG] {package} is already installed, skipping...")

            except RuntimeError:
                if package == "chromedriver":
                    print(f"[LOG] {package} is already installed, skipping...")
            
            except ImportError:
                print(f"[LOG] {package} not installed.")

                try:
                    print(f"[LOG] Trying to install {package} via pip.")
                    try:
                        import pip
                    except:
                        print("[EXCEPTION] Pip is not installed.")
                        print("[LOG] Trying to install pip...")
                        get_pip.main()
                        print("[LOG] Pip has been installed!")

                    print(f"[LOG] Installing {package}")    
                    install(package)
                    with contextlib.redirect_stdout(None):
                        if package not in ("PyQtWebEngine", "chromedriver"):
                            __import__(package)
                    print(f"[LOG] {package} has been installed")

                except Exception as e:
                    print(f"[ERROR] Could not install {package}: {e}")
                    failed.append(package)                  
    
    else:
        print("[STOP] Operation terminated by user.")
else:
    print("[LOG] No packages to install!")

if len(failed) > 0:
    print(f"\n[FAILED] {len(failed)} package(s) were not installed." + \
    "\nFailed package install(s):", end=" ")
    for x, package in enumerate(failed):
        if x != len(failed) -1:
            print(package, end=", ")
        else:
            print(package)
else:
    print(f"\n[SUCCESS] {len(required)} package(s) available on machine!")