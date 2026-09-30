"""Converter registry. To add a new file type: create a converter file and list it here."""
from converters.audio_converter import AudioConverter
from converters.image_converter import ImageConverter
from converters.video_converter import VideoConverter

ALL_CONVERTERS = [ImageConverter(), AudioConverter(), VideoConverter()]


def get_converter(src_ext: str, target: str):
    for conv in ALL_CONVERTERS:
        if conv.can_convert(src_ext, target):
            return conv
    return None
