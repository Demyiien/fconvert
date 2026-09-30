"""Image conversion via Pillow (png, jpg, webp, bmp, gif, tiff, ico)."""
from pathlib import Path
from typing import Optional

from converters.base import BaseConverter, ConversionError

PIL_NAMES = {"png": "PNG", "jpg": "JPEG", "jpeg": "JPEG", "webp": "WEBP",
             "bmp": "BMP", "gif": "GIF", "tiff": "TIFF", "ico": "ICO"}


class ImageConverter(BaseConverter):
    name = "image"
    input_formats = {"png", "jpg", "jpeg", "webp", "bmp", "gif", "tiff", "tif", "ico"}
    output_formats = set(PIL_NAMES)
    quality_hint = "1-100 for jpg/webp (default 90)"

    def output_folder_name(self, target: str) -> str:
        return "images"

    def convert(self, src: Path, dest: Path, target: str, quality: Optional[int]) -> None:
        try:
            from PIL import Image
        except ImportError:
            raise ConversionError("Pillow is not installed. Run: pip install Pillow")

        with Image.open(src) as img:
            fmt = PIL_NAMES[target]
            if fmt in ("JPEG", "BMP") and img.mode in ("RGBA", "LA", "P"):
                img = img.convert("RGBA")
                bg = Image.new("RGB", img.size, (255, 255, 255))
                bg.paste(img, mask=img.split()[-1])
                img = bg
            elif fmt == "JPEG" and img.mode != "RGB":
                img = img.convert("RGB")

            opts = {}
            if fmt in ("JPEG", "WEBP"):
                opts["quality"] = quality or 90
            if fmt == "ICO":
                opts["sizes"] = [(s, s) for s in (16, 32, 48, 64, 128, 256) if s <= max(img.size)] or [(32, 32)]
            img.save(dest, fmt, **opts)
