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

"Color stuff
syntax enable
set background=dark
colorscheme solarized


"gvim 'fullscreen' mode
function! ToggleGUI()
  if &guioptions=='i'
    exec('set guioptions=imTrL')
  else
    exec('set guioptions=i')
  endif
endfunction

"For Vim-LaTeX plugin
filetype plugin on
set grepprg=grep\ -nh\ $*
filetype indent on
let g:tex_flavor='latex'

"Custom Vim-LaTeX Macros
augroup MyIMAPs
	au!
	au VimEnter * call IMAP('SUM', '\sum\limits_{<++>}^{<++>} <++>', 'tex')
	au VimEnter * call IMAP('PRD', '\prod\limits_{<++>}^{<++>} <++>', 'tex')
	au VimEnter * call IMAP('LIM', '\lim\limits_{<++>} <++>', 'tex')
	au VimEnter * call IMAP('INF', '\infty', 'tex')
	au VimEnter * call IMAP('DRV', '\frac{d<++>}{d<++>} <++>', 'tex')
	au VimEnter * call IMAP('INT', '\int\limits_{<++>}^{<++>} <++>', 'tex')
	au VimEnter * call IMAP('FRA', '\frac{<++>}{<++>} <++>', 'tex') 
	au VimEnter * call IMAP('BSK', '\bigskip <++>', 'tex')
	au VimEnter * call IMAP('ABS', '\lvert <++> \rvert <++>', 'tex')
	au VimEnter * call IMAP('PDV', '\frac{\delta <++>}{\delta <++>} <++>', 'tex')
	au VimEnter * call IMAP('NOT', '\neg <++>', 'tex')
	au VimEnter * call IMAP('AND', '\wedge <++>', 'tex')
	au VimEnter * call IMAP('OR', '\vee <++>', 'tex')
	au VimEnter * call IMAP('XOR', '\bigoplus <++>', 'tex')
	au VimEnter * call IMAP('LCASE', '\subsection{\textit{<++>} (<++>)}<++>', 'tex')
	au VimEnter * call IMAP('MAT', '\begin{smallmatrix} <++> \end{smallmatrix}<++>', 'tex')
	au VimEnter * call IMAP('MLT', '\begin{bmatrix} <++> \end{bmatrix}<++>', 'tex')
augroup END


