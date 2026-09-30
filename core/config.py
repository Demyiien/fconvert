"""Central paths and settings."""
from pathlib import Path

VERSION = "1.0.0"
BASE_DIR = Path(__file__).resolve().parent.parent
INPUT_DIR = BASE_DIR / "input"
OUTPUT_DIR = BASE_DIR / "output"
