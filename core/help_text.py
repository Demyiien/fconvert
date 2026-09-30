"""All user-facing help text lives here."""
from converters import ALL_CONVERTERS
from core.config import VERSION

HELP = f"""
fconvert {VERSION} - command-line file converter (audio / video / images)

USAGE
  fconvert /<command> [arguments] [options]

COMMANDS
  /help                         Show this help
  /convert <file> <format>      Convert one file       e.g. fconvert /convert song.wav mp3
  /batch <folder> <format>      Convert every compatible file in a folder
  /formats                      Show supported formats and what converts to what
  /list                         List files waiting in the input/ folders
  /check                        Check that ffmpeg and Pillow are installed
  /version                      Show version

OPTIONS  (for /convert and /batch)
  /q <number>                   Quality (see /formats for meaning per type)
  /out <folder>                 Save results here instead of the default output folder
  /overwrite                    Replace existing files instead of creating name_1, name_2...

EXAMPLES
  fconvert /convert photo.png jpg
  fconvert /convert "C:\\Users\\me\\Videos\\clip.mp4" mp3
  fconvert /convert movie.mkv mp4 /q 80
  fconvert /convert clip.mp4 gif /out C:\\Users\\me\\Desktop
  fconvert /batch C:\\Users\\me\\Pictures webp /q 85

WHERE FILES GO
  Drop files into input\\audio, input\\video or input\\images and refer to them by
  name only. Results are saved to:
    output\\mp3 , output\\wav , output\\mp4 , ...   (audio/video, one folder per format)
    output\\images                                  (all images)

NOTES
  Audio and video need ffmpeg installed. Images need Pillow (pip install Pillow).
  Converting video to an audio format (e.g. mp4 -> mp3) extracts the audio track.
  "-h", "--help" and "help" also work.
"""


def formats_text() -> str:
    lines = ["\nSUPPORTED FORMATS\n"]
    for c in ALL_CONVERTERS:
        lines.append(f"  [{c.name}]")
        lines.append(f"    input : {', '.join(sorted(c.input_formats))}")
        lines.append(f"    output: {', '.join(sorted(c.output_formats))}")
        lines.append(f"    /q    : {c.quality_hint}\n")
    return "\n".join(lines)
