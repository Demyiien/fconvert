"""Audio conversion (mp3, wav, ogg, flac, aac, m4a) + audio extraction from video."""
from pathlib import Path
from typing import Optional

from converters.base import BaseConverter
from core.ffmpeg_runner import run_ffmpeg

CODECS = {
    "mp3": "libmp3lame",
    "wav": "pcm_s16le",
    "ogg": "libvorbis",
    "flac": "flac",
    "aac": "aac",
    "m4a": "aac",
}


class AudioConverter(BaseConverter):
    name = "audio"
    input_formats = {"mp3", "wav", "ogg", "flac", "aac", "m4a", "wma",
                     # video containers -> extract the audio track
                     "mp4", "mkv", "avi", "mov", "webm"}
    output_formats = set(CODECS)
    quality_hint = "bitrate in kbps (default 192)"

    def convert(self, src: Path, dest: Path, target: str, quality: Optional[int]) -> None:
        args = ["-vn", "-c:a", CODECS[target]]
        if target not in ("wav", "flac"):
            args += ["-b:a", f"{quality or 192}k"]
        run_ffmpeg(src, dest, args)
