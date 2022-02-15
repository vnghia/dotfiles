#!/usr/bin/env python3

import argparse
import json
import subprocess

import git_utils
from constants import DOTFILES_GIT_PROFILE


def write_profile_config(config_path=None, postfix=None, email=None):
    config_path = config_path or DOTFILES_GIT_PROFILE / "default.json"
    config = {}
    with open(config_path) as f:
        config.update(json.load(f))
    postfix = postfix or config.pop("postfix")
    email = email or config.pop("email")
    config["user.email"] = email
    git_utils.write_config(config)
    return postfix


def change_remote_url(remote_name=None, postfix=None, push_only=None):
    url, remote_name = git_utils.read_remote_url(remote_name)
    if not url:
        return
    fetch_url, push_url = git_utils.parse_git_url(url, postfix)
    command = ["git", "remote", "set-url"]
    if push_only:
        subprocess.check_call(command + [remote_name, fetch_url])
        command += ["--push"]
    else:
        fetch_url = push_url
    command += [remote_name, push_url]
    subprocess.check_call(command)
    print(f"Changed {remote_name} (fetch) url to {fetch_url}")
    print(f"Changed {remote_name} (push)  url to {push_url}")


def git_profile(
    config_path=None, remote_name=None, postfix=None, email=None, push_only=None
):
    postfix = write_profile_config(config_path, postfix, email)
    change_remote_url(remote_name, postfix, push_only)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config-path")
    parser.add_argument("-r", "--remote-name")
    parser.add_argument("-p", "--postfix")
    parser.add_argument("-e", "--email")
    parser.add_argument("-po", "--push-only", action="store_true")
    args = parser.parse_args()
    git_profile(
        args.config_path, args.remote_name, args.postfix, args.email, args.push_only
    )


if __name__ == "__main__":
    main()
