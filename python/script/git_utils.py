import configparser
import itertools
import subprocess
from posixpath import join
from urllib.parse import urlparse, urlunparse

import utils

# ---------------------------------------------------------------------------- #
#                                    Version                                   #
# ---------------------------------------------------------------------------- #


def get_git_version():
    output = subprocess.check_output(["git", "--version"], text=True)
    output = output[len("git version ") :]
    version = "".join(itertools.takewhile(lambda x: x.isdigit() or x == ".", output))
    return list(map(int, version.split(".")))


# ---------------------------------------------------------------------------- #
#                                  Remote url                                  #
# ---------------------------------------------------------------------------- #


def read_remote_url(remote_name=None):
    remote_name = remote_name or "origin"
    remotes = subprocess.check_output(["git", "remote", "-v"], text=True).splitlines()
    origins = [
        remote[len(f"{remote_name}\t") : -len(" (push)")]
        for remote in remotes
        if "push" in remote and remote_name in remote
    ]
    origin = None
    if origins:
        origin = origins[0]
    return origin, remote_name


def parse_git_url(url, postfix):
    postfix = utils.add_prefix(postfix, ".")
    host, path, port = None, None, ""
    if url.startswith("ssh://") or "://" not in url:
        url = utils.add_prefix(url, "ssh://")
        urls = urlparse(url)
        path = join(urls.netloc.split(":", 1)[1], urls.path.strip("/")).strip("/")
        host = utils.remove_postfix(urls.hostname, postfix)
    else:
        urls = urlparse(url)
        host, path = urls.hostname, urls.path.strip("/")
        port = str(urls.port) if urls.port else ""
        port = utils.add_prefix(port, ":")
    https_url = urlunparse(("https", host + port, path, None, None, None))
    host = utils.add_postfix(host, postfix)
    ssh_url = f"git@{host}:{path}"
    return https_url, ssh_url


# ---------------------------------------------------------------------------- #
#                                   Gitconfig                                  #
# ---------------------------------------------------------------------------- #


def read_config(path):
    parser = configparser.ConfigParser()
    parser.read(path)
    config = {}
    for section in parser.sections():
        for key, value in parser[section].items():
            full_key = section.replace(" ", ".") + "." + key
            config[full_key] = value.replace("\\", "").strip('"').strip("'")
    return config


def write_config(config):
    for k, v in config.items():
        subprocess.check_call(["git", "config", "--local", k, v])
