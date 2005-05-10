#!/usr/bin/env python2.4
# encoding: latin-1

# copyright (c) domenico carbotta <domenico.carbotta@gmail.com>, 2005
# code released under the gnu gpl, see license.txt

'''
sddscanner.py

Lexer per il linguaggio Simple Document Definition.
Per la specifica completa del linguaggio fare riferimento alla documentazione
che accompagna il programma.
'''

from spark07 import GenericScanner
from token import Token


class SDDScannerException (Exception):
	'''
		Eccezione sollevata dalla classe SDDScanner
	'''
	pass


class SDDScanner (GenericScanner):
	'''
		Questa classe implementa uno scanner per le Simple Document Definitions
		utilizzando la libreria SPARK sviluppata da John Aycock della University 
		of Calgary.
		
		Per ulteriori informazioni su SPARK:
			http://pages.cpsc.ucalgary.ca/~aycock/spark/
	'''
	
	def __init__(self):
		GenericScanner.__init__(self)
	
	def tokenize(self, input):
		self.rv = []
		self.lineno = 1
		self.input_length = len(input)
		GenericScanner.tokenize(self, input)
		return self.rv
	
	def t_newline(self, s):
		r' \n+ '
		self.lineno += len(s)
	
	def t_ignore(self, s):
		r' \s+ '
		pass
	
	def t_ignore_UTF8_BOM(self, s):
		r' \ufeff '
		pass
	
	def t_id(self, s):
		r' [a-z][a-zA-Z0-9_]* '
		self.rv.append(Token('ID', s))
	
	def t_arrow(self, s):
		r' -> '
		self.rv.append(Token('ARROW', s))
	
	def t_openpar(self, s):
		r' \( '
		self.rv.append(Token('OPENPAR', s))
	
	def t_closepar(self, s):
		r' \) '
		self.rv.append(Token('CLOSEPAR', s))
	
	def t_semicolon(self, s):
		r' ; '
		self.rv.append(Token('SEMICOLON', s))
	
	def t_comma(self, s):
		r' , '
		self.rv.append(Token('COMMA', s))
	
	def t_pcdata(self, s):
		r' \#PCDATA '
		self.rv.append(Token('PCDATA', s))
	
	def t_default(self, s):
		r' ( . | \n )* '
		errlen = min(len(s), 10)
		raise SDDScannerException, 'Error at line %d: %r' % \
				(self.lineno, s[:errlen])

if __name__ == '__main__':
	
	try:
		s = raw_input()
	except EOFError:
		s = '''id1 id2 #PCDATA ( ) ; , ->
		abc Abcdef'''
		print s
		print
	
	for token in SDDScanner().tokenize(s):
		print token

