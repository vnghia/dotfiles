#!/usr/bin/env python3

import argparse
import shutil

from constants import CODE_BIN, CODE_HOME, CODE_LOCAL


def setup_localcode(init=None):
    if init:
        print(f"  Remove from: {CODE_LOCAL}")
        shutil.rmtree(CODE_LOCAL, ignore_errors=True)

    CODE_HOME.mkdir(parents=True, exist_ok=True)
    CODE_LOCAL.mkdir(parents=True, exist_ok=True)
    CODE_BIN.mkdir(parents=True, exist_ok=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i",
        "--init",
        action="store_true",
        help="force remove and initialization from scratch",
    )
    args = parser.parse_args()
    setup_localcode(args.init)


if __name__ == "__main__":
    main()
