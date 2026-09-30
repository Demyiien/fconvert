"""Video conversion (mp4, mkv, avi, mov, webm, gif)."""
from pathlib import Path
from typing import Optional

from converters.base import BaseConverter
from core.ffmpeg_runner import run_ffmpeg


class VideoConverter(BaseConverter):
    name = "video"
    input_formats = {"mp4", "mkv", "avi", "mov", "webm", "flv", "wmv"}
    output_formats = {"mp4", "mkv", "avi", "mov", "webm", "gif"}
    quality_hint = "1-100, higher = better (default ~65)"

    def convert(self, src: Path, dest: Path, target: str, quality: Optional[int]) -> None:
        if target == "gif":
            args = ["-vf", "fps=12,scale=480:-1:flags=lanczos", "-an"]
        else:
            crf = 23 if quality is None else int(51 - (max(1, min(quality, 100)) / 100) * 33)
            if target == "webm":
                args = ["-c:v", "libvpx-vp9", "-crf", str(crf), "-b:v", "0", "-c:a", "libopus"]
            else:
                args = ["-c:v", "libx264", "-crf", str(crf), "-preset", "medium",
                        "-c:a", "aac", "-pix_fmt", "yuv420p"]
                if target in ("mp4", "mov"):
                    args += ["-movflags", "+faststart"]
        run_ffmpeg(src, dest, args)
