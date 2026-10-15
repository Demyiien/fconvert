# fconvert

Command-line converter for audio, video and images. Run `fconvert /help`.

## Setup (Windows)
1. Install Python 3.9+ and run: `pip install -r requirements.txt`
2. Install ffmpeg: `winget install ffmpeg` (needed for audio/video)
3. Add this folder to your PATH (Start > "Edit environment variables" > Path > New).
   Open a new cmd window; now `fconvert /help` works from anywhere.
   (Without PATH: `cd` into this folder and run `fconvert /help`.)

## Structure
    fconvert.py / fconvert.bat   entry point + cmd launcher
    core/        cli, engine, help text, config, helpers, ffmpeg runner
    converters/  one file per file type (audio, video, image) + base + registry
    input/       audio/  video/  images/   (drop files here)
                 (converted files are saved to the source file's folder, or custom /out)

## Add a new type
Create `converters/xxx_converter.py` subclassing `BaseConverter`, then add it to `ALL_CONVERTERS` in `converters/__init__.py`.
