"""Small helpers: path resolution, unique names, sizes."""
from pathlib import Path

from core.config import INPUT_DIR


def resolve_input(name: str) -> Path:
    """Use the path as given; otherwise look for it inside input/ subfolders."""
    p = Path(name.strip('"')).expanduser()
    if p.is_file():
        return p.resolve()
    if INPUT_DIR.exists():
        for match in INPUT_DIR.rglob(p.name):
            if match.is_file():
                return match.resolve()
    raise FileNotFoundError(f"File not found: {name}")


def unique_path(path: Path) -> Path:
    if not path.exists():
        return path
    i = 1
    while True:
        candidate = path.with_name(f"{path.stem}_{i}{path.suffix}")
        if not candidate.exists():
            return candidate
        i += 1


def human_size(num: int) -> str:
    for unit in ("B", "KB", "MB", "GB"):
        if num < 1024 or unit == "GB":
            return f"{num:.1f} {unit}" if unit != "B" else f"{num} B"
        num /= 1024
