#!/usr/bin/env python3

import argparse
import json
import subprocess
import sys
from collections import defaultdict

import utils
from constants import DOTFILES_SSH_HOME, SSH_CONFIG_DIR, SSH_HOME, SSH_KEY


def generate_keypair(key_path, options=None):
    options = options or {}
    command = ["ssh-keygen"]
    command += ["-f", key_path]
    command += ["-t", options.get("t") or "ed25519"]
    if "C" not in options:
        options["C"] = ""
    for k, v in options.items():
        command += [f"-{k}", v]
    try:
        subprocess.check_call(command)
    except subprocess.CalledProcessError as exce:
        if not key_path.exists():
            raise exce
    print("Please add this key to ssh-agent (if you set password) by calling:")
    print('eval "$(ssh-agent -s)"')
    command = "ssh-add "
    if sys.platform == "darwin":
        command += "-K "
    print(f"{command}{key_path}")


def get_key_fullpath(host=None):
    key_path = SSH_KEY / host.replace(".", "_")
    return key_path


def generate_ssh_config(config, port=None):
    hostname = config.pop("hostname")
    postfix = config.pop("postfix")
    postfix = utils.add_prefix(postfix, ".")
    host = utils.add_postfix(hostname, postfix)
    key_path = get_key_fullpath(host)
    generate_keypair(key_path, config.pop("key", None))
    if port:
        config["Port"] = port

    content = "# AUTO GENERATED FILE. DO NOT EDIT\n\n"
    content += f"Host {host}\n"
    content += f"\tHostname {hostname}\n"
    content += f"\tIdentityFile {key_path}\n"
    for k, v in config.items():
        if k == "UseKeychain" and sys.platform != "darwin":
            continue
        v = "yes" if v is True else v
        content += f"\t{k} {v}\n"
    content += "\n"
    return content, key_path


def write_ssh_config(content, key_path):
    config_path = SSH_CONFIG_DIR / key_path.name
    config_path.with_suffix(".config")

    with open(config_path, "w") as f:
        f.write(content)

    default_config = SSH_HOME / "config"
    should_include_config = True
    if default_config.exists():
        with open(default_config, "r") as f:
            should_include_config = f"Include {config_path}" not in f.read()

    if should_include_config:
        with open(default_config, "a") as f:
            f.write(f"\nInclude {config_path}\n")


def make(config_path=None, port=None):
    config_path = DOTFILES_SSH_HOME / (config_path or "default.json")
    config = {}
    with open(config_path) as f:
        config = json.load(f)
    content, key_path = generate_ssh_config(config, port)
    write_ssh_config(content, key_path)


def list():
    res = defaultdict(int)
    for path in SSH_KEY.glob("*"):
        relpath = path.relative_to(SSH_KEY)
        res[relpath.with_suffix("")] += 1
    print(" ".join([str(key) for key, value in res.items() if value == 2]))


def cat(key_path):
    print((SSH_KEY / key_path).with_suffix(".pub").read_text())


def main():
    parser = argparse.ArgumentParser()
    subparser = parser.add_subparsers()

    # mk
    parser_mk = subparser.add_parser("mk", aliases=["make", "new"])
    parser_mk.add_argument("-c", "--config_path")
    parser_mk.add_argument("-p", "--port")
    parser_mk.set_defaults(func=make)

    # ls
    parser_ls = subparser.add_parser("ls", aliases=["list"])
    parser_ls.set_defaults(func=list)

    # cat
    parser_cat = subparser.add_parser("cat")
    parser_cat.add_argument("key_path")
    parser_cat.set_defaults(func=cat)

    args = vars(parser.parse_args())
    func = args.pop("func")
    func(**args)


if __name__ == "__main__":
    main()
