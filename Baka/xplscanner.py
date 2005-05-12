#!/usr/bin/env python2.4
# encoding: latin-1

# copyright (c) domenico carbotta <domenico.carbotta@gmail.com>, 2005
# code released under the gnu gpl, see license.txt

'''
xplscanner.py

Lexer per una versione semplificata del linguaggio XPathLog.
Per la specifica completa del linguaggio fare riferimento alla documentazione
che accompagna il programma.
'''

from spark07 import GenericScanner
from re import UNICODE
from token import Token


class XPLScannerException (Exception):
	'''
		Eccezione sollevata dalla classe SDDScanner
	'''
	pass


class XPathLogScanner (GenericScanner):
	'''
		Questa classe implementa uno scanner per una versione ridotta del
		linguaggio XPathLog utilizzando la libreria SPARK sviluppata da
		John Aycock della University of Calgary.
		
		Per ulteriori informazioni su SPARK:
			http://pages.cpsc.ucalgary.ca/~aycock/spark/
	'''
	
	def __init__(self):
		GenericScanner.__init__(self, UNICODE)
	
	def tokenize(self, input):
		self.rv = []
		self.lineno = 1
		GenericScanner.tokenize(self, input)
		return self.rv
		
	def t_newline(self, s):
		r' \n+ '
		self.lineno += len(s)
	
	def t_ignore_UTF8_BOM(self, s):
		r' \ufeff '
		pass
	
	def t_ignore(self, s):
		r' \s+ '
		pass
	
	def t_call(self, s):
		r' \$ ( pos | text ) '
		self.rv.append(Token('CALL', s))
	
	def t_operator(self, s):
		r' ( \+ | \- (?! >) | \( | \) )'
		if s == '+':
			optype = 'PLUS'
		if s == '-':
			optype = 'MINUS'
		elif s == '(':
			optype = 'OPENPAR'
		elif s == ')':
			optype = 'CLOSEPAR'
		self.rv.append(Token(optype, s))
	
	def t_compare(self, s):
		r' ( < (?! = ) | <= | = | \!= | >= | (?<! - ) > )'
		self.rv.append(Token('COMPARE', s))
	
	def t_not(self, s):
		r' \! (?! = ) '
		self.rv.append(Token('NOT', s))
	
	def t_comma(self, s):
		r' \, '
		self.rv.append(Token('COMMA', s))
	
	def t_opensqr(self, s):
		r' \[ '
		self.rv.append(Token('OPENSQR', s))
	
	def t_closesqr(self, s):
		r' \] '
		self.rv.append(Token('CLOSESQR', s))
	
	def t_numvalue(self, s):
		r' ( \.\d+ | \d+(\.\d+)? ) '
		self.rv.append(Token('NUMVALUE', s))
	
	def t_stringvalue(self, s):
		' ( "[^"]*" ) '
		self.rv.append(Token('STRINGVALUE', s))
	
	def t_element(self, s):
		r' [a-z][a-zA-Z0-9_àèéìòù]* '
		self.rv.append(Token('ELEMENT', s))
	
	def t_var(self, s):
		r' [A-Z][a-zA-Z0-9_àèéìòù]* '
		self.rv.append(Token('VAR', s))
	
	def t_attribute(self, s):
		r' @[a-zA-Z0-9_àèéìòù]* '
		self.rv.append(Token('ATTRIBUTE', s[1:]))
	
	def t_arrow(self, s):
		r' -> '
		self.rv.append(Token('ARROW', s))
	
	def t_slash(self, s):
		r' / (?!/) '
		self.rv.append(Token('SLASH', s))
	
	def t_dslash(self, s):
		r' // '
		self.rv.append(Token('DSLASH', s))
	
	def t_up(self, s):
		r' \.\. '
		self.rv.append(Token('UP', s))
	
	def t_star(self, s):
		r' \* '
		self.rv.append(Token('STAR', s))
	
	def t_default(self, s):
		r' ( . | \n )* '
		errlen = min(len(s), 10)
		raise XPLScannerException, 'Error at line %d: "%s"' % \
				(self.lineno, s[:errlen])

if __name__ == '__main__':
	
	try:
		s = raw_input()
	except EOFError:
		s = ', 22.4 22 .. [ ] element Id @attribute $text -> > != ! / //'
		print s
		print
	
	for token in XPathLogScanner().tokenize(s):
		print token
