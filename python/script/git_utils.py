import configparser
import itertools
import subprocess

# ---------------------------------------------------------------------------- #
#                                    Version                                   #
# ---------------------------------------------------------------------------- #


def get_git_version():
    output = subprocess.check_output(["git", "--version"], text=True)
    output = output[len("git version ") :]
    version = "".join(itertools.takewhile(lambda x: x.isdigit() or x == ".", output))
    return list(map(int, version.split(".")))


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
