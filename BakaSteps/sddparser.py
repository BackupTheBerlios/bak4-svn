#!/usr/bin/env python2.4
# encoding: latin-1

# copyright (c) domenico carbotta <domenico.carbotta@gmail.com>, 2005
# code released under the gnu gpl, see license.txt

'''
sddparser.py

Parser per il linguaggio Simple Document Definition.
Per la specifica completa del linguaggio fare riferimento alla documentazione
che accompagna il programma.
'''

from spark07 import GenericParser
from sddscanner import SDDScanner
from mytoken import Token
from document import Document

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
		self.sdd_elements = {}
		self.sdd_edges = []
		self.sdd_pcdata_elements = []
		
	def p_definition(self, args):
		'''
			definition ::= elements
		'''
		self.check()
		return Document(self.sdd_elements, self.sdd_edges,
				self.sdd_pcdata_elements)
	
	def check(self):
		elements = self.sdd_elements
		edges = self.sdd_edges
		pcdata_elements = self.sdd_pcdata_elements
		for el_a, el_b in edges:
			if el_b not in elements:
				errmsg = 'Element %s (referenced as child of element %s) '\
						'does not exist.' 
				raise SDDParsingException, errmsg % (el_b, el_a)
		
	def p_elements(self, args):
		'''
			elements ::= element SEMICOLON elements
			elements ::= element SEMICOLON
			elements ::= element
		'''
		pass
	
	def p_element(self, args):
		'''
			element ::= ID ARROW attribute_list contents
		'''
		id = args[0].value
		attributes = args[2]
		allows_pcdata, children = args[3]
		
		self.sdd_elements[id] = attributes
		if allows_pcdata:
			self.sdd_pcdata_elements.append(id)
		else:
			for child in children:
				self.sdd_edges.insert(0, (id, child))
	
	def p_attribute_list(self, args):
		'''
			attribute_list ::= OPENPAR idlist CLOSEPAR
			attribute_list ::=
		'''
		if len(args) == 0:
			return []
		else:
			return args[1]
	
	def p_contents_1(self, args):
		'''
			contents ::= idlist
		'''
		return False, args[0]
	
	def p_contents_2(self, args):
		'''
			contents ::= PCDATA
		'''
		return True, None
	
	def p_idlist(self, args):
		'''
			idlist ::= idlist_full
			idlist ::=
		'''
		if len(args) == 0:
			return []
		else:
			return args[0]
	
	def p_idlist_full(self, args):
		'''
			idlist_full ::= ID COMMA idlist_full
			idlist_full ::= ID
		'''
		if len(args) == 1:
			return [args[0].value]
		else:
			args[2].insert(0, args[0].value)
			return args[2]
		
	def error(self, token):
		raise SDDParsingException, 'Error: unexpected token "%s".' \
			% token.value
