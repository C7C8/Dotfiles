syntax on
set autoindent
set nowrap
set hlsearch
set nocp
set backspace=indent,eol,start
set number
set ruler
au BufNewFile,BufRead *.cpp set syntax=cpp11
execute pathogen#infect()
filetype plugin indent on

"For Vim-LaTeX plugin
filetype plugin on
set grepprg=grep\ -nh\ $*
filetype indent on
let g:tex_flavor='latex'

"Custom Vim-LaTeX Macros
augroup MyIMAPs
	au!
	au VimEnter * call IMAP('SUM', '\sum\limits_{<++>}^{<++>} <++>', 'tex')
	au VimEnter * call IMAP('LIM', '\lim\limits_{<++>} <++>', 'tex')
	au VimEnter * call IMAP('INF', '\infty', 'tex')
	au VimEnter * call IMAP('DRV', '\frac{d<++>}{d<++>}', 'tex')
	au VimEnter * call IMAP('INT', '\int\limits_{<++>}^{<++>} <++>', 'tex')
	au VimEnter * call IMAP('FRA', '\frac{<++>}{<++>} <++>', 'tex') 
augroup END


