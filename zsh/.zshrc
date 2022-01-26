# Source activate firstmost !
source "$ZDOTDIR/activate.zsh"

# Oh-my-zsh
export ZSH="$ZDOTDIR/.oh-my-zsh"
export ZSH_CUSTOM="$ZDOTDIR/custom"

## Theme
export ZSH_THEME="powerlevel10k/powerlevel10k"

## Plugins
plugins=(
  zsh-syntax-highlighting
  zsh-autosuggestions
  sudo
  web-search
  copydir
  copyfile
  history
)

source $ZSH/oh-my-zsh.sh

# Source config in the end !
source "$ZDOTDIR/config.zsh"
