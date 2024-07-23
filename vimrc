set nu
set cul
set ruler
set incsearch
set showmatch
set hlsearch
set showcmd

set tabstop=4
set softtabstop=4
set shiftwidth=4
set expandtab
set autoindent

colorscheme industry
au BufReadPost * if line("'\"") > 0 && line("'\"") <= line("$") | exe"normal g'\"" | endif
