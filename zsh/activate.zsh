source "$DOTFILES_SHELL_HOME/activate.sh"

# History
export HISTFILE="$HISTFILE_HOME/.zsh_history"
export HISTSIZE=999999999
export SAVEHIST=999999999

# Compdump
export ZSH_COMPDUMP="$DUMPFILE_HOME/.zsh_compdump"

# Functions

## Common functions for every shell
fpath=($DOTFILES_SHELL_FUNCTION $fpath)
autoload -Uz $fpath[1]/*(.:t)
