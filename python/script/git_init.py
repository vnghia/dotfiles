#!/usr/bin/env python3

import argparse
import subprocess

import git_utils
from constants import DOTFILES_GIT_HOME


def git_init(branch=None, local=None):
    branch = branch or "main"
    git_version = git_utils.get_git_version()
    if git_version[1] <= 27:
        subprocess.check_call(["git", "init"])
        subprocess.check_call(["git", "checkout", "-b", branch])
    else:
        subprocess.check_call(["git", "init", "--initial-branch", branch])

    config = {}
    if git_version[1] <= 31 or local:
        config.update(git_utils.read_config(DOTFILES_GIT_HOME / ".gitconfig"))
    git_utils.write_config(config)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-b", "--branch")
    parser.add_argument("-l", "--local", action="store_true")
    args = parser.parse_args()
    git_init(args.branch, args.local)
    print("Please call git pr !")


if __name__ == "__main__":
    main()
