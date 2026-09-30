"""Command parsing and dispatch."""
import shutil
from pathlib import Path

from converters import ALL_CONVERTERS, get_converter
from converters.base import ConversionError
from core.config import INPUT_DIR, VERSION
from core.engine import convert_file
from core.help_text import HELP, formats_text
from core.utils import human_size

OPTION_NAMES = {"q": "quality", "quality": "quality", "out": "out", "o": "out",
                "overwrite": "overwrite", "w": "overwrite"}
FLAG_OPTIONS = {"overwrite"}


def parse_args(args):
    positional, opts, i = [], {}, 0
    while i < len(args):
        key = OPTION_NAMES.get(args[i].lstrip("/-").lower())
        if key and args[i][0] in "/-":
            if key in FLAG_OPTIONS:
                opts[key] = True
            else:
                i += 1
                if i >= len(args):
                    raise ValueError(f"Option '{args[i - 1]}' needs a value.")
                opts[key] = args[i]
        else:
            positional.append(args[i])
        i += 1
    if "quality" in opts:
        try:
            opts["quality"] = int(opts["quality"])
        except ValueError:
            raise ValueError("Quality must be a number.")
    return positional, opts


def cmd_convert(args):
    pos, opts = parse_args(args)
    if len(pos) != 2:
        print("Usage: fconvert /convert <file> <format> [/q N] [/out FOLDER] [/overwrite]")
        return 1
    dest = convert_file(pos[0], pos[1], opts.get("out"), opts.get("quality"), opts.get("overwrite", False))
    print(f"OK  -> {dest}  ({human_size(dest.stat().st_size)})")
    return 0


def cmd_batch(args):
    pos, opts = parse_args(args)
    if len(pos) != 2:
        print("Usage: fconvert /batch <folder> <format> [/q N] [/out FOLDER] [/overwrite]")
        return 1
    folder, target = Path(pos[0].strip('"')), pos[1].lower().lstrip(".")
    if not folder.is_dir():
        print(f"Error: folder not found: {folder}")
        return 1
    ok = failed = skipped = 0
    for f in sorted(folder.iterdir()):
        if not f.is_file():
            continue
        if not get_converter(f.suffix.lower().lstrip("."), target):
            skipped += 1
            continue
        try:
            dest = convert_file(str(f), target, opts.get("out"), opts.get("quality"), opts.get("overwrite", False))
            print(f"OK    {f.name} -> {dest}")
            ok += 1
        except (ConversionError, OSError) as e:
            print(f"FAIL  {f.name}: {e}")
            failed += 1
    print(f"\nDone. converted={ok} failed={failed} skipped={skipped}")
    return 0 if failed == 0 else 1


def cmd_list(_):
    found = False
    for sub in sorted(p for p in INPUT_DIR.iterdir() if p.is_dir()):
        files = [f for f in sub.iterdir() if f.is_file() and f.name != ".gitkeep"]
        print(f"\n{sub.name}\\ ({len(files)} file(s))")
        for f in files:
            found = True
            print(f"  {f.name}  ({human_size(f.stat().st_size)})")
    if not found:
        print("\nNo files yet. Drop files into input\\audio, input\\video or input\\images.")
    return 0


def cmd_check(_):
    print("ffmpeg :", shutil.which("ffmpeg") or "NOT FOUND (needed for audio/video)")
    try:
        import PIL
        print("Pillow :", PIL.__version__)
    except ImportError:
        print("Pillow : NOT INSTALLED (needed for images) -> pip install Pillow")
    return 0


COMMANDS = {
    "help": lambda _: print(HELP) or 0,
    "h": lambda _: print(HELP) or 0,
    "convert": cmd_convert,
    "batch": cmd_batch,
    "formats": lambda _: print(formats_text()) or 0,
    "list": cmd_list,
    "check": cmd_check,
    "version": lambda _: print(f"fconvert {VERSION}") or 0,
}


def main(argv):
    if not argv:
        print(HELP)
        return 0
    name = argv[0].lstrip("/-").lower()
    handler = COMMANDS.get(name)
    if handler is None:
        print(f"Unknown command: {argv[0]}\nType 'fconvert /help' to see all commands.")
        return 1
    try:
        return handler(argv[1:])
    except (ConversionError, FileNotFoundError, ValueError) as e:
        print(f"Error: {e}")
        return 1
    except KeyboardInterrupt:
        print("\nCancelled.")
        return 130
