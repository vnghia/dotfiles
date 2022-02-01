# Should always be sourced at end so no one will override it!

# Editor
export VISUAL="code --wait"
export EDITOR="vim"

# Language
export LANG="en_US.UTF-8"
export LANGUAGE="en"
export LC_ALL="en_US.UTF-8"

# Python
export PIP_REQUIRE_VIRTUALENV="true"
export PYTHONSTARTUP="$DOTFILES_PYTHON_SCRIPT/pythonrc.py"

# Git
export GIT_CONFIG_GLOBAL="$DOTFILES_GIT_HOME/.gitconfig"

# System command

## ls with color (https://geoff.greer.fm/lscolors/)
export CLICOLOR=1
# MacOS / FreeBSD
export LSCOLORS="gxfxbxdxcxegedabagacad"
# GNU Linux
export LS_COLORS="di=36:ln=35:so=31:pi=33:ex=32:bd=34;46:cd=34;43:su=30;41:sg=30;46:tw=30;42:ow=30;43"

# Alias
source "$DOTFILES_SHELL_HOME/alias.sh"

# Local configuration / path / everything else that is specific to each machine
LOCAL_SH="$DOTFILES_SHELL_HOME/.local.sh" && test -f $LOCAL_SH && source $LOCAL_SH
