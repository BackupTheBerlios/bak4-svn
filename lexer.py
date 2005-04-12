#!/usr/bin/env python2.4

# copyright (c) domenico carbotta <domenico.carbotta@gmail.com>, 2005
# code released under the gnu gpl, see license.txt

'''
Lexer per una versione semplificata del linguaggio XPathLog. Per la specifica
completa del linguaggio fare riferimento alla documentazione che accompagna il
programma.
'''

from spark import GenericScanner

from token import Token


class LexerException (Exception):
	'''
	Eccezione sollevata dal lexer in caso di errore.
	'''
	pass


class XPathLogScanner (GenericScanner):
	
	def __init__(self):
		GenericScanner.__init__(self)
	
	def tokenize(self, input):
		self.rv = []
		GenericScanner.tokenize(self, input)
		return self.rv
	
	def t_whitespace(self, s):
		r' \s+ '
		pass
	
	def t_compare(self, s):
		r' ( < | <= | = | <> | >= | (?<! - ) > )'
		self.rv.append(Token('COMPARE', s))
	
	def t_value(self, s):
		r' \d+ ( \. \d+ )? '
		## r' (\d+|"[^"]*") ' will recognize also strings -- do we need it?
		self.rv.append(Token('VALUE', s))
	
	def t_element(self, s):
		r' [a-z][a-zA-Z0-9_]* '
		self.rv.append(Token('ELEMENT', s))
	
	def t_var(self, s):
		r' [A-Z][a-zA-Z0-9_]* '
		self.rv.append(Token('VAR', s))
	
	def t_attribute(self, s):
		r' @[a-zA-Z0-9_]* '
		self.rv.append(Token('ATTRIBUTE', s[1:]))
	
	def t_call(self, s):
		r' ( pos | text ) \( \) '
		self.rv.append(Token('CALL', s[:-2]))
	
	def t_arrow(self, s):
		r' -> '
		self.rv.append(Token('ARROW'))
	
	def t_slash(self, s):
		r' / (?!/) '
		self.rv.append(Token('SLASH'))
	
	def t_dslash(self, s):
		r' // '
		self.rv.append(Token('DSLASH'))
	
	def t_up(self, s):
		r' \.\. '
		self.rv.append(Token('UP'))
	
	def t_star(self, s):
		r' \* '
		self.rv.append(Token('STAR'))


if __name__ == '__main__':
	print XPathLogScanner().tokenize(raw_input())
