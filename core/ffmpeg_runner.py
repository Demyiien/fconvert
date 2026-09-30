"""Thin wrapper around the ffmpeg executable (used by audio + video converters)."""
import shutil
import subprocess
from pathlib import Path

from converters.base import ConversionError


def find_ffmpeg():
    return shutil.which("ffmpeg")


def run_ffmpeg(src: Path, dest: Path, args: list):
    exe = find_ffmpeg()
    if not exe:
        raise ConversionError(
            "ffmpeg not found. Install it (winget install ffmpeg) and make sure "
            "it is on your PATH. Run 'fconvert /check' to verify."
        )
    cmd = [exe, "-y", "-hide_banner", "-loglevel", "error", "-i", str(src), *args, str(dest)]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise ConversionError(result.stderr.strip() or "ffmpeg failed.")
