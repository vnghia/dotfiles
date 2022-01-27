import os
from pathlib import Path

HOME = Path.home()

DOTFILES_HOME = Path(os.environ["DOTFILES_HOME"])

DOTFILES_PYTHON_HOME = Path(os.environ["DOTFILES_PYTHON_HOME"])
DOTFILES_PYTHON_SCRIPT = Path(os.environ["DOTFILES_PYTHON_SCRIPT"])

PYVENV_HOME = Path(os.environ["PYVENV_HOME"])
PYVENV_LOCAL = Path(os.environ["PYVENV_LOCAL"])
PYVENV_BIN = Path(os.environ["PYVENV_BIN"])
