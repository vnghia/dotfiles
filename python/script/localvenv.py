#!/usr/bin/env python3

import argparse
import shutil

import pyvenv
from constants import (
    DOTFILES_PYTHON_REQUIREMENTS_DOTFILES,
    PYVENV_BIN,
    PYVENV_HOME,
    PYVENV_LOCAL,
)


def setup_localvenv(python=None, init=None):
    if init:
        print(f"  Remove from: {PYVENV_HOME}")
        shutil.rmtree(PYVENV_HOME, ignore_errors=True)

    PYVENV_HOME.mkdir(parents=True, exist_ok=True)
    if not PYVENV_LOCAL.exists():
        pyvenv.make(PYVENV_LOCAL, python)
    PYVENV_BIN.mkdir(parents=True, exist_ok=True)
    pyvenv.install(
        PYVENV_LOCAL, rs=[DOTFILES_PYTHON_REQUIREMENTS_DOTFILES / "requirements.txt"]
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i",
        "--init",
        action="store_true",
        help="force remove and initialization from scratch",
    )
    parser.add_argument("-p", "--python")
    args = parser.parse_args()
    setup_localvenv(args.python, args.init)


if __name__ == "__main__":
    main()
