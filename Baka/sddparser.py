#!/usr/bin/env python2.4

# copyright (c) domenico carbotta <domenico.carbotta@gmail.com>, 2005
# code released under the gnu gpl, see license.txt

'''
Parser per il linguaggio Simple Document Definition.
Per la specifica completa del linguaggio fare riferimento alla documentazione
che accompagna il programma.
'''

from spark import GenericParser
from sddlexer import SDDScanner
from token import Token


class SDDParsingException (Exception):
	'''
		Eccezione sollevata dal parser in caso di errore.
	'''
	pass


class SDDParser (GenericParser):
	'''
		Questa classe implementa un parser per le Simple Document Definitions
		utilizzando la libreria SPARK sviluppata da
		John Aycock della University of Calgary.
		
		Per ulteriori informazioni su SPARK:
			http://pages.cpsc.ucalgary.ca/~aycock/spark/
	'''
	
	def __init__(self, start='definition'):
		GenericParser.__init__(self, start)
		
	def p_definition(self, args):
		'''
			definition ::= elements
			
			elements ::= element SEMICOLON elements
			elements ::= element SEMICOLON
			
			element ::= ID COLON OPENPAR idlist CLOSEPAR idlist allowspcdata
			
			idlist ::= ID idlist
			idlist ::=
			
			allowspcdata ::= PCDATA
			allowspcdata ::=
		'''
		pass


if __name__ == '__main__':
	
	pass
