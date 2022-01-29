import os
from pathlib import Path

HOME = Path.home()

DOTFILES_HOME = Path(os.environ["DOTFILES_HOME"])

DOTFILES_PYTHON_HOME = Path(os.environ["DOTFILES_PYTHON_HOME"])
DOTFILES_PYTHON_SCRIPT = Path(os.environ["DOTFILES_PYTHON_SCRIPT"])
DOTFILES_PYTHON_REQUIREMENTS_HOME = DOTFILES_PYTHON_HOME / "requirements"
DOTFILES_PYTHON_REQUIREMENTS_DOTFILES = DOTFILES_PYTHON_REQUIREMENTS_HOME / "dotfiles"

CODE_HOME = Path(os.environ["CODE_HOME"])
CODE_LOCAL = Path(os.environ["CODE_LOCAL"])
CODE_BIN = Path(os.environ["CODE_BIN"])

PYVENV_HOME = Path(os.environ["PYVENV_HOME"])
PYVENV_LOCAL = Path(os.environ["PYVENV_LOCAL"])
PYVENV_BIN = Path(os.environ["PYVENV_BIN"])

SSH_HOME = HOME / ".ssh"
SSH_KEY = SSH_HOME / "key"
SSH_CONFIG_DIR = SSH_HOME / "config_dir"
DOTFILES_SSH_HOME = Path(os.environ["DOTFILES_SSH_HOME"])
