#!/usr/bin/env python3

import argparse
import shutil
import subprocess
import sys

from constants import PYVENV_BIN, PYVENV_HOME, PYVENV_LOCAL


def link_to_global_bin(bin_path):
    for bin in bin_path.iterdir():
        if not (
            not bin.is_file()
            or bin.name.startswith(".")
            or bin.name.startswith("activate")
            or bin.name.startswith("Activate")
            or bin.name.startswith("pip")
            or bin.name.startswith("python")
            or bin.name.startswith("wheel")
        ):
            dest_path = PYVENV_BIN / bin.name
            if not dest_path.exists():
                try:
                    if sys.version_info[1] < 10:
                        (bin_path / bin).link_to(dest_path)
                    else:
                        dest_path.hardlink_to(bin_path / bin)
                except NotImplementedError:
                    break


def make(venv=None, python=None, options=None):
    venv = venv or PYVENV_LOCAL
    python = python or "python3"
    command = [shutil.which(python)]
    command.append("-m")
    command.append("venv")
    if options:
        command += options
    env_dir = PYVENV_HOME / venv
    command.append(env_dir)
    subprocess.check_call(command)


def remove(venv=None):
    if not venv:
        print("Deleting local !")
    venv = venv or PYVENV_LOCAL
    shutil.rmtree(PYVENV_HOME / venv, ignore_errors=False)


def list():
    res = []
    for p in PYVENV_HOME.iterdir():
        path = PYVENV_HOME / p
        if path.is_dir() and path != PYVENV_LOCAL:
            res.append(p.name)
    print(" ".join(res))


def install(venv=None, packages=None, rs=None, options=None):
    venv = venv or PYVENV_LOCAL
    bin_path = PYVENV_HOME / venv / "bin"
    command = [bin_path / "python3", "-m", "pip", "install"]
    if packages:
        command += packages
    if rs:
        for f in rs:
            command += ["-r", f]
    if options:
        command += options
    subprocess.run(command)
    if venv != PYVENV_LOCAL:
        return
    link_to_global_bin(bin_path)


def run(script=None, venv=None, options=None):
    if not script:
        script = next(PYVENV_HOME.cwd().glob("*.py"))
    venv = venv or PYVENV_LOCAL
    bin_path = PYVENV_HOME / venv / "bin"
    command = [bin_path / "python3", script]
    if options:
        command += options
    subprocess.check_call(command)


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="action")

    # mk
    parser_mk = subparsers.add_parser("mk", aliases=["make", "new"])
    parser_mk.add_argument("venv", nargs="?")
    parser_mk.add_argument("-p", "--python")
    parser_mk.set_defaults(func=make)

    # rm
    parser_rm = subparsers.add_parser("rm", aliases=["remove", "del"])
    parser_rm.add_argument("venv", nargs="?")
    parser_rm.set_defaults(func=remove)

    # ls
    parser_ls = subparsers.add_parser("ls", aliases=["list"])
    parser_ls.set_defaults(func=list)

    # i
    parser_i = subparsers.add_parser("i", aliases=["install"])
    parser_i.add_argument("packages", nargs="*")
    parser_i.add_argument("-r", action="append", dest="rs")
    parser_i.add_argument("-v", "--venv")
    parser_i.set_defaults(func=install)

    # r
    parser_r = subparsers.add_parser("r", aliases=["run"])
    parser_r.add_argument("script", nargs="?")
    parser_r.add_argument("-v", "--venv")
    parser_r.set_defaults(func=run)

    args, unknown = parser.parse_known_args()
    args = vars(args)
    if args.pop("action") in ("mk", "i", "r"):
        args["options"] = unknown
    elif unknown:
        raise argparse.ArgumentError("unrecognized arguments: %s" % " ".join(unknown))
    func = args.pop("func")
    func(**args)


if __name__ == "__main__":
    main()
