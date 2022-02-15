#!/usr/bin/env python3

import argparse
import subprocess

import utils
from constants import GIT_USERNAME


def git_clone(repo, username=None, host=None, method=None, postfix=None, options=None):
    repo = utils.add_postfix(repo, ".git")
    username = username or GIT_USERNAME
    host = host or "github.com"
    if not method:
        if username == GIT_USERNAME:
            method = "ssh"
        else:
            method = "https"
    postfix = postfix or "personal"
    postfix = utils.add_prefix(postfix, ".")
    options = options or []

    url = ""
    if method == "ssh":
        url = f"git@{utils.add_postfix(host, postfix)}:{username}/{repo}"
    else:
        url = f"https://{host}/{username}/{repo}"
    subprocess.check_call(["git", "clone", url] + options)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("repo")
    parser.add_argument("-u", "--username")
    parser.add_argument("-ho", "--host")
    parser.add_argument("-m", "--method")
    parser.add_argument("-p", "--postfix")
    args, options = parser.parse_known_args()
    git_clone(args.repo, args.username, args.host, args.method, args.postfix, options)


if __name__ == "__main__":
    main()
