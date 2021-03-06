import shutil
import sys

# ---------------------------------------------------------------------------- #
#                                    String                                    #
# ---------------------------------------------------------------------------- #


def add_prefix(string, prefix):
    if string and not string.startswith(prefix):
        string = prefix + string
    return string


def add_postfix(string, postfix):
    if string and not string.endswith(postfix):
        string = string + postfix
    return string


def remove_prefix(string, prefix):
    if string and string.startswith(prefix):
        string = string[len(prefix) :]
    return string


def remove_postfix(string, postfix):
    if string and string.endswith(postfix):
        string = string[: -len(postfix)]
    return string


# ---------------------------------------------------------------------------- #
#                                   PLatform                                   #
# ---------------------------------------------------------------------------- #


def is_android():
    return shutil.which("termux-setup-storage") is not None


def platform():
    return "android" if is_android() else sys.platform
