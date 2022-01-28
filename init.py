import argparse
import subprocess
from pathlib import Path

HOME = Path.home()
DOTFILES_HOME = Path()
DOTFILES_SHELL_HOME = Path()

REPO_URL = "https://github.com/vnghia/dotfiles.git"
GIT_SUBMODULES = {
    "zsh": [
        "zsh/custom/themes/powerlevel10k",
        "zsh/custom/plugins/zsh-syntax-highlighting",
        "zsh/custom/plugins/zsh-autosuggestions",
        "zsh/.oh-my-zsh",
    ]
}


def clone_dotfiles():
    DOTFILES_HOME.mkdir(parents=True, exist_ok=True)
    subprocess.check_call(["git", "init"], cwd=DOTFILES_HOME)
    subprocess.check_call(["git", "switch", "-C", "main"], cwd=DOTFILES_HOME)
    subprocess.run(["git", "remote", "rm", "origin"], cwd=DOTFILES_HOME)
    subprocess.check_call(
        ["git", "remote", "add", "origin", REPO_URL], cwd=DOTFILES_HOME
    )
    subprocess.check_call(["git", "pull", "origin", "main"], cwd=DOTFILES_HOME)


def init_submodule(shell):
    subprocess.check_call(
        ["git", "submodule", "update", "--init"] + GIT_SUBMODULES[shell],
        cwd=DOTFILES_HOME,
    )


def generate_startup_file_zsh(code):
    with open(HOME / ".zshenv", "w") as f:
        ZDOTDIR = DOTFILES_HOME / "zsh"
        f.write("# AUTO GENERATED FILE. DO NOT EDIT\n\n")
        f.write(f"export DOTFILES_HOME={DOTFILES_HOME}\n")
        f.write(f"export CODE_HOME={code}\n")
        f.write(f"export ZDOTDIR={ZDOTDIR}\n")
        f.write(f"export DOTFILES_SHELL_HOME={DOTFILES_SHELL_HOME}\n")


def generate_startup_file(shell, code):
    if shell == "zsh":
        generate_startup_file_zsh(code)


def print_install_font():
    print("Please install Jetbrains Mono font at:")
    print("  https://github.com/JetBrains/JetBrainsMono")
    print(
        "  https://github.com/ryanoasis/nerd-fonts/tree/master/patched-fonts/JetBrainsMono/Ligatures/Regular"
    )


def init():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--dotfiles", default=HOME / ".dotfiles")
    parser.add_argument("-c", "--code", default=HOME / "code")
    parser.add_argument("-s", "--shell", default="zsh", choices=["zsh"])
    args = parser.parse_args()

    global DOTFILES_HOME
    DOTFILES_HOME = Path(args.dotfiles).expanduser().resolve()
    global DOTFILES_SHELL_HOME
    DOTFILES_SHELL_HOME = DOTFILES_HOME / "sh"

    shell = args.shell
    code = Path(args.code).expanduser().resolve()
    clone_dotfiles()
    init_submodule(shell)
    print_install_font()
    generate_startup_file(shell, code)
    print("Please restart your shell and run upgrade.py !")


if __name__ == "__main__":
    init()
