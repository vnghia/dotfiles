#!/usr/bin/env python3

import argparse
import os
import subprocess
from pathlib import Path

import localcode
import localvenv
import sshkey
from constants import (
    DOTFILES_HOME,
    DUMPFILE_HOME,
    HISTFILE_HOME,
    SSH_CONFIG_DIR,
    SSH_KEY,
)

XDG_CONFIG_HOME = Path(os.environ["XDG_CONFIG_HOME"])
XDG_CACHE_HOME = Path(os.environ["XDG_CACHE_HOME"])
XDG_DATA_HOME = Path(os.environ["XDG_DATA_HOME"])
XDG_RUNTIME_DIR = Path(os.environ["XDG_RUNTIME_DIR"])


def main():
    XDG_CONFIG_HOME.mkdir(parents=True, exist_ok=True)
    XDG_CACHE_HOME.mkdir(parents=True, exist_ok=True)
    XDG_DATA_HOME.mkdir(parents=True, exist_ok=True)
    XDG_RUNTIME_DIR.mkdir(parents=True, exist_ok=True)

    DUMPFILE_HOME.mkdir(parents=True, exist_ok=True)
    HISTFILE_HOME.mkdir(parents=True, exist_ok=True)

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i",
        "--init",
        action="store_true",
        help="force remove and initialization from scratch",
    )
    parser.add_argument("-p", "--python")
    parser.add_argument("-np", "--no-pull", action="store_true")
    args = parser.parse_args()
    if not args.no_pull:
        subprocess.check_call(["git", "pull", "origin", "main"], cwd=DOTFILES_HOME)

    localcode.setup_localcode(args.init)
    localvenv.setup_localvenv(args.python, args.init)

    SSH_KEY.mkdir(parents=True, exist_ok=True)
    SSH_CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    sshkey.make()
    print("Please restart your shell !")


if __name__ == "__main__":
    main()
