"""Entry point. Run from cmd:  fconvert /help"""
import sys

from core.cli import main

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
