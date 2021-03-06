dotfilesenv
===
[![MIT License](http://img.shields.io/badge/license-MIT-blue.svg?style=flat)](LICENSE)

`dotfilesenv` is the awesome cli to manage dotfiles.  
It is so awesome that you can management your dotfiles (e.g. `.zshrc`, `.vimrc`).  
Although the tool is already very awesome, developing is work in progress.  

## Installation

```zsh
$ pip install git+https://github.com/yush1ga/dotfilesenv.git
```

## Usage

### create symbolic link

```zsh
$ dotfilesenv link vimrc ~/.vimrc
```

`~/.vimrc` is moved to `~/.dotfilesenv/vimrc` and `~/vimrc` becomes the symbolic link of it.

### view your dotfiles list

```zsh
$ dotfilesenv list
```

### delete your link

```zsh
$ dotfilesenv delete vimrc
```

The link is deleted and the source file/directory is moved to former place.

### restore your .dotfiles

```zsh
$ dotfilesenv restore
```

Symbolic links are created from `~/.dotfilesenv` .

## You don't have fundamental human rights (Python 3.5 or later) ?

How poor!  
It happens sometimes in remote environment and so on.  
However, you can get command to restore from `~/.dotfilesenv`.

```zsh
$ dotfilesenv restore --command
ln -s ~/.dotfilesenv/zshrc/.zshrc ~/.zshrc
ln -s ~/.dotfilesenv/vimrc/.vimrc ~/.vimrc
```


## Auto completions (only zsh)

Use [my zsh-completions](https://github.com/yush1ga/zsh-completions)!

## Contribution

Please feel free to send pull requests to this awesome repository.

## Licence

[MIT](https://github.com/yush1ga/dotfilesenv/blob/master/LICENSE)

## Author

[yush1ga](https://github.com/yush1ga)
