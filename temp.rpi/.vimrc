" Make 256 colors wwork with Vim (hopefully)
set t_Co=256
autocmd FileType python setlocal expandtab shiftwidth=4 softtabstop=4
" map leader key
let mapleader = "'"
set smartindent
" Turn on smart indent for automatic indentation in python files
" Install pathogen file manager to make things easy to install/controll.
    filetype on                 " try to detect filetypes
   "filetype plugin indent on   " enable loading indent file for filetype
    call pathogen#runtime_append_all_bundles()
    call pathogen#helptags()
    set expandtab
    set textwidth=79
    set tabstop=8
    set softtabstop=4
    set shiftwidth=4
    set autoindent
    set foldmethod=indent
    set foldlevel=99
    :syntax on
":colorscheme darkblue

nmap <Leader>m :w<CR>:!sh make<CR>
nmap <Leader>b :!sh ~/temp.rpi/backup.sh<CR>
nmap <Leader>e :!sudo ./IRcamera<CR>

" map Ctrl+W+movement keys to Ctrl+movement
map <c-j> <c-w>j
map <c-k> <c-w>k
map <c-l> <c-w>l
map <c-h> <c-w>h

" Map <Leader> movement to move windows.
map <Leader>j <c-w>j
map <Leader>k <c-w>k
map <Leader>l <c-w>l
map <Leader>h <c-w>h

" map space and shift-space to page up and down
noremap <S-space> <C-b>
noremap <space> <C-f>

" set a save-every-write
"inoremap <Esc> <Esc>:w<CR>
" use jk to get back to normal/command mode
imap jk <Esc>
"
" enable code completion
"au Filetype python set omnifunc=pythoncomplete#Complete
"let g:SuperTabDefaultCompletionType = "context"
"set completeopt=menuone,longest,preview         " enables menu, documentation.
" commented out for YouCompleteMe

" keep longer history
set history=100
" set title
set title



" highlight search terms
set hlsearch
set incsearch "highlights as typed

" Hit ENTER to continue, etc shortened :help shortmess for more info
set shortmess=a



if has('gui_running')
    " scroll when you get to a couple lines before bottom of screen
    set scrolloff=8
    set background=dark
    colorscheme solarized
    set relativenumber
else
    set background=dark
  " let g:solarized_termcolors=256
    colorscheme solarized
    set bg=light
    set rnu
endif


colorscheme solarized

" set up sage files to have the same highlighting as python files

" added from vim-latex website
" insure that MacVim can make backups
" put all backup files, etc in a central folder
set backupdir=~/.vim/backups


"   " The Latex stuff
"   " REQUIRED. This makes vim invoke Latex-Suite when you open a tex file.
"   filetype plugin on

"   " IMPORTANT: win32 users will need to have 'shellslash' set so that latex
"   " can be called correctly.
"   " set shellslash

"   " IMPORTANT: grep will sometimes skip displaying the file name if you
"   " search in a singe file. This will confuse Latex-Suite. Set your grep
"   " program to always generate a file-name.
"   " set grepprg=grep\ -nH\ $*


set incsearch       " search as you type
set hlsearch        " highlight search terms
set ignorecase      " case insensitive search

"clearing highlighted search. press " '' c" to clear search terms. leader twice.
"(leader leader clear)
nmap <silent> <leader><leader>c :nohlsearch<CR>

"folding settings
set foldmethod=indent   "fold based on indent
set foldnestmax=10      "deepest fold is 10 levels
set nofoldenable        "dont fold by default
set foldlevel=9         "set max. folding depth.
" press zc (-close) and zo (-open) to fold functions

"nnoremap <leader>r :GundoToggle<CR>

" remap paragraphs so they're easier to do
nnoremap <leader>g gqip

" the annoying noindent comment thing in python
set nosmartindent

" allow easy folding of functions
nnoremap <Space> za

" set the default to be tmux instead of screen
let g:slime_target = "tmux"
let g:Imap_UsePlaceHolders = 0

" make it act like write room
" goes to the mapping of the VimroomToggle function
"g:vimroom_background=dark
nnoremap <silent> <Leader>r :set nonumber<CR>

" get rainbow parens to work right
let g:rbpt_colorpairs = [
    \ ['brown',       'RoyalBlue3'],
    \ ['Darkblue',    'SeaGreen3'],
    \ ['darkgray',    'DarkOrchid3'],
    \ ['darkgreen',   'firebrick3'],
    \ ['darkcyan',    'RoyalBlue3'],
    \ ['darkred',     'SeaGreen3'],
    \ ['darkmagenta', 'DarkOrchid3'],
    \ ['brown',       'firebrick3'],
    \ ['gray',        'RoyalBlue3'],
    \ ['black',       'SeaGreen3'],
    \ ['darkmagenta', 'DarkOrchid3'],
    \ ['Darkblue',    'firebrick3'],
    \ ['darkgreen',   'RoyalBlue3'],
    \ ['darkcyan',    'SeaGreen3'],
    \ ['darkred',     'DarkOrchid3'],
    \ ['red',         'firebrick3'],
    \ ]
"let g:rbpt_max = 16
"let g:rbpt_loadcmd_toggle = 0
au VimEnter * RainbowParenthesesToggle
au VimEnter * RainbowParenthesesToggle
au VimEnter * RainbowParenthesesToggle
au Syntax   * RainbowParenthesesLoadRound
au Syntax   * RainbowParenthesesLoadSquare
au Syntax   * RainbowParenthesesLoadBraces
" end of getting rainbow parens to work right"

noremap <Leader>w vipJ<CR>

" setting up vundle
set nocompatible               " be iMproved
filetype off                   " required!
set rtp+=~/.vim/bundle/vundle/
call vundle#rc()
Bundle 'gmarik/vundle'
filetype plugin indent on 
" Brief help
" :BundleList          - list configured bundles
" :BundleInstall(!)    - install(update) bundles
" :BundleSearch(!) foo - search(or refresh cache first) for foo
" :BundleClean(!)      - confirm(or auto-approve) removal of unused
"
" see :h vundle for more details or wiki for FAQ
" NOTE: comments after Bundle command are not allowed..

" this makes my life a lot easier for my UROP (with Jarvis)
"
" setting a nice status line
set statusline=%t%=\ %P
set laststatus=2

" from "Vim after 11 years"
nmap j gj
nmap k gk

"setting up Ctrl-P
"set runtimepath^=~/.vim/bundle/ctrlp.vim
"let g:ctrlp_map = '<c-p>'
"let g:ctrlp_cmd = 'CtrlP'
"let g:ctrlp_working_path_mode = 'ra'
"let g:ctrlp_clear_cache_on_exit = 0

" Set <Leader>r to toggle the *full* history
nnoremap <leader>r :GundoToggle<CR>

" comment out python code blocks nicely
" comment line, selection with Ctrl-N,Ctrl-N
" make sure that jk is ESC
" imap jk <Esc>
"
" Make comments work nicely
" nmap <Leader>cc NERDComToggleComment
" <Leader>c<Space> toggles comment (based on first line)

" make compile nice

" make alighing/tab nice
vnoremap <Leader>t :Tabular<space>/
:set bg=light

" set up nice tab-completion
"filetype plugin on
"let g:pydiction_location = '~/.vim/bundle/pydiction/complete-dict'

" moving around easier
let g:seek_subst_disable = 1

" move swp files. use full file names
set dir=~/.vim/tmp


" color the current column -- useful for python
"
" setting up unite.vim

set mouse=a
