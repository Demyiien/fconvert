"""Conversion logic shared by single and batch commands."""
from pathlib import Path
from typing import Optional

from converters import get_converter
from converters.base import ConversionError
from core.config import OUTPUT_DIR
from core.utils import resolve_input, unique_path


def convert_file(name: str, target: str, out_dir: Optional[str] = None,
                 quality: Optional[int] = None, overwrite: bool = False) -> Path:
    src = resolve_input(name)
    src_ext = src.suffix.lower().lstrip(".")
    target = target.lower().lstrip(".")

    conv = get_converter(src_ext, target)
    if conv is None:
        raise ConversionError(f"Cannot convert '.{src_ext}' to '.{target}'. See: fconvert /formats")

    folder = Path(out_dir) if out_dir else OUTPUT_DIR / conv.output_folder_name(target)
    folder.mkdir(parents=True, exist_ok=True)
    dest = folder / f"{src.stem}.{target}"
    if not overwrite:
        dest = unique_path(dest)

    conv.convert(src, dest, target, quality)
    return dest
