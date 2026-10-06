"""
Annapurna Groceries & Liquor — Unified Single-Port Server Runner
Runs the full application (Storefront + Django Admin + REST API) on http://127.0.0.1:8000
"""
import sys
import os
import subprocess
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

POSSIBLE_SHOPADMIN_DIRS = [
    BASE_DIR / 'shopadmin_clean' / 'shopadmin',
    BASE_DIR / 'shopadmin',
    BASE_DIR.parent / 'shopadmin_clean' / 'shopadmin',
]

shopadmin_dir = None
for p in POSSIBLE_SHOPADMIN_DIRS:
    if (p / 'manage.py').exists():
        shopadmin_dir = p
        break

if not shopadmin_dir:
    print("❌ Error: Could not find 'manage.py'. Please check folder structure.")
    sys.exit(1)

POSSIBLE_PYTHONS = [
    shopadmin_dir / 'venv' / 'Scripts' / 'python.exe',
    shopadmin_dir.parent / 'venv' / 'Scripts' / 'python.exe',
    BASE_DIR / 'venv' / 'Scripts' / 'python.exe',
]

python_exe = sys.executable
for py in POSSIBLE_PYTHONS:
    if py.exists():
        python_exe = str(py)
        break

print("=" * 60)
print("🚀 STARTING ANNAPURNA STORE (UNIFIED SINGLE SERVER)")
print("=" * 60)
print("📍 Storefront (Customer):   http://127.0.0.1:8000/")
print("🛒 Liquor Catalog:          http://127.0.0.1:8000/liquior.html")
print("🥦 Grocery Catalog:         http://127.0.0.1:8000/grocries.html")
print("⚙️  Admin Dashboard:         http://127.0.0.1:8000/dashboard/")
print("🔑 Admin Login:             http://127.0.0.1:8000/?admin_login=1")
print("📦 REST API:                http://127.0.0.1:8000/api/products/")
print("=" * 60)
print("Press Ctrl+C anytime to stop the server.\n")

try:
    cmd = [python_exe, 'manage.py', 'runserver', '127.0.0.1:8000']
    subprocess.run(cmd, cwd=str(shopadmin_dir))
except KeyboardInterrupt:
    print("\n👋 Server stopped.")
