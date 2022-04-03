# Powerlevel10k
## Hook direnv
(( ${+commands[direnv]} )) && emulate zsh -c "$(direnv export zsh)"
source $ZDOTDIR/.p10k.instant-prompt
(( ${+commands[direnv]} )) && emulate zsh -c "$(direnv hook zsh)"

# Source activate firstmost !
source "$ZDOTDIR/activate.zsh"

# Oh-my-zsh
export ZSH="$ZDOTDIR/.oh-my-zsh"
export ZSH_CUSTOM="$ZDOTDIR/custom"

## Theme
export ZLE_RPROMPT_INDENT=0
export ZSH_THEME="powerlevel10k/powerlevel10k"

## Plugins
plugins=(
  zsh-syntax-highlighting
  zsh-autosuggestions
  sudo
  web-search
  copyfile
  history
)

export DISABLE_AUTO_UPDATE="true"
source $ZSH/oh-my-zsh.sh

# Powerlevel10k
source $ZDOTDIR/.p10k.zsh

# Hightlight
source $ZDOTDIR/.highlight.zsh

# Source config in the end !
source "$ZDOTDIR/config.zsh"
