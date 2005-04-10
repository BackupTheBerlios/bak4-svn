#!/usr/bin/env python2.4

# copyright (c) domenico carbotta <domenico.carbotta@gmail.com>, 2005
# code released under the gnu gpl, see license.txt

'''
Lexer per una versione semplificata del linguaggio XPathLog. Per la specifica
completa del linguaggio fare riferimento alla documentazione che accompagna il
programma.
'''

import lex

__all__ = ['tokenize', 'LexerException']

tokens = (
	'ATTRIBUTE',
	'BIND',
	'CALL',
	'CLOSEFLT',
	'COMMA',
	'COMPARE',
	'DBLSLASH',
	'EL',
	'NOT',
	'OPENFLT',
	'SLASH',
	'STAR',
	'UP',
	'VALUE',
	'VAR',
)

t_ignore = ' \t'

def t_newline(t):
    r'\n+'
    t.lineno += len(t.value)

class LexerException (Exception):
	'''
	Eccezione sollevata dal lexer in caso di errore.
	'''
	pass

def t_error(t):
	raise LexerException, t.value

t_ATTRIBUTE	= '@[a-zA-Z][a-zA-Z0-9_]*'
t_BIND		= r'->'
t_CALL		= r'([a-z][a-zA-Z0-9_]*)\(\)'
t_CLOSEFLT	= r'\]'
t_COMMA		= ','
t_COMPARE	= r'(<|<=|=|~=|>=|>)'
t_DBLSLASH	= '//'
t_EL		= '[a-z][a-zA-Z0-9_]*'
t_NOT		= '~'
t_OPENFLT	= r'\['
t_SLASH		= '/'
t_STAR		= r'\*'
t_UP		= r'\.\.'
t_VALUE		= '( "[^"]*" | [0-9]+(.[0-9]+)? )'
t_VAR		= '[A-Z][a-zA-Z0-9_]*'


def tokenize(source):
	'''
	Restituisce una lista contenente la sequenza dei token generati a partire
	dalla stringa passata come parametro; solleva una LexerException in caso di
	errore.
	'''
	lexer = lex.lex()
	lexer.input(source)
	rv = []
	while 1:
		t = lexer.token()
		if t is None:
			return rv
		rv.append(t)

if __name__ == '__main__':
	token_stream = tokenize("/hope/this->works")
	for i in token_stream:
		print i
