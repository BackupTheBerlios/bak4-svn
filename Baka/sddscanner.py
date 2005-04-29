#!/usr/bin/env python2.4

# copyright (c) domenico carbotta <domenico.carbotta@gmail.com>, 2005
# code released under the gnu gpl, see license.txt

'''
Lexer per il linguaggio Simple Document Definition.
Per la specifica completa del linguaggio fare riferimento alla documentazione
che accompagna il programma.
'''

from spark import GenericScanner
from token import Token, LexerException


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
		GenericScanner.tokenize(self, input)
		return self.rv
	
	def t_ignore(self, s):
		r' \s+ '
		pass
	
	def t_id(self, s):
		r' [a-z][a-zA-Z0-9_]* '
		self.rv.append(Token('ID', s))
	
	def t_colon(self, s):
		r' \: '
		self.rv.append(Token('COLON', s))
	
	def t_openpar(self, s):
		r' \( '
		self.rv.append(Token('OPENPAR', s))
	
	def t_closepar(self, s):
		r' \) '
		self.rv.append(Token('CLOSEPAR', s))
	
	def t_semicolon(self, s):
		r' ; '
		self.rv.append(Token('SEMICOLON', s))
	
	def t_pcdata(self, s):
		r' \#PCDATA '
		self.rv.append(Token('PCDATA', s))


if __name__ == '__main__':
	
	try:
		s = raw_input()
	except EOFError:
		s = 'id1 id2 #PCDATA ( ) ; '
		print s
		print
	
	for token in SDDScanner().tokenize(s):
		print token

