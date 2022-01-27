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

# Local configuration / path / everything else that is specific to each machine
LOCAL_SH="$DOTFILES_SHELL_HOME/.local.sh" && test -f $LOCAL_SH && source $LOCAL_SH
