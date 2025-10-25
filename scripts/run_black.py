"""Run Black over the project, preferring the project's .venv Python when present.
Usage:
    python scripts/run_black.py
"""

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VENV_PY = ROOT / ".venv" / "Scripts" / "python.exe"

if VENV_PY.exists():
    cmd = [str(VENV_PY), "-m", "black", str(ROOT)]
else:
    cmd = [sys.executable, "-m", "black", str(ROOT)]

print("Running:", " ".join(cmd))
try:
    subprocess.run(cmd, check=True)
    print("Black finished successfully.")
except subprocess.CalledProcessError as e:
    print(f"Black returned non-zero exit ({e.returncode})")
    sys.exit(e.returncode)
