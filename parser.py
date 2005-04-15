#!/usr/bin/env python2.4

# copyright (c) domenico carbotta <domenico.carbotta@gmail.com>, 2005
# code released under the gnu gpl, see license.txt

'''
Parser e traduttore per una versione semplificata del linguaggio XPathLog.
Per la specifica completa del linguaggio fare riferimento alla documentazione
che accompagna il programma.
'''

from spark import GenericParser

from lexer import XPathLogScanner
from token import Token


class AST (object):
	
	def __init__(self, name, *cnt):
		self.name = name
		if cnt is None:
			self.cnt = []
		self.cnt = cnt
	
	def format(self, n=0):
		rv = '\t' * n + 'AST(%r, [\n' % self.name
		for i in self.cnt:
			if type(i) is AST:
				rv += i.format(n + 1)
			else:
				rv += '\t' * (n + 1) + repr(i) + ',\n'
		rv += '\t' * n + '])\n'
		return rv
	
	def __repr__(self):
		return self.format()


class ParsingException (Exception):
	'''
		Eccezione sollevata dal parser in caso di errore.
	'''
	pass


class Walk (object):
	
	def __init__(self, refers_to=None):
		self.refers_to = refers_to
		self.steps = []


class Step (object):

	def __init__(self, qualifier, id):
		self.qualifier = qualifier
		self.id = id


class StarStep (Step):
	
	def __init__(self, id):
		Step.__init__(self, '*', id)


class BridgeStep (Step):
	
	def __init__(self, id):
		Step.__init__(self, '//', id)


class UpStep (Step):
	
	def __init__(self, id):
		# SONO QUI
		pass


class XPathLogParser (GenericParser):
	'''
		Questa classe implementa un parser per una versione ridotta del
		linguaggio XPath attraverso tecniche di Aspect Oriented Programming.
		Enough with the buzzwords, in realtà uso semplicemente la libreria
		SPARK di John Aycock.
		
		J. Aycock, "Compiling Little Languages in Python", 7th International
		Python Conference, 1998.
	'''
	
	def __init__(self, start='denial'):
		GenericParser.__init__(self, start)
		self.filters = []
	
	def p_denial(self, args):
		'''
			denial ::= expression_list
		'''
		return args[0], self.filters
	
	def p_expression_list_1(self, args):
		'''
			expression_list ::= expression COMMA denial
		'''
		args[2].insert(0, args[0])
		return args[2]
	
	def p_expression_list_2(self, args):
		'''
			expression_list ::= expression
		'''
		# Conflitto shift-reduce ok.
		return args
	
	def p_expression_1(self, args):
		'''
			expression ::= path COMPARE VALUE
			expression ::= path COMPARE path_expression
		'''
		return AST('compare', args[0], args[2])
	
	def p_expression_2(self, args):
		'''
			expression ::= path
		'''
		# Conflitto shift-reduce ok.
		return args[0]
	
	def p_path_1(self, args):
		'''
			path ::= VAR spec path_cnt
		'''
		pass
	
	def p_path_2(self, args):
		'''
			path ::= DSLASH ELEMENT spec path_cnt
		'''
		pass
	
	def p_path_3(self, args):
		'''
			path ::= UP spec path_cnt
			path ::= STAR spec path_cnt
			path ::= ELEMENT spec path_cnt
			path ::= ATTRIBUTE bind
			path ::= CALL bind
		'''
		
	
	def p_path_cnt_1(self, args):
		'''
			path_cnt ::= SLASH ELEMENT spec path_cnt
		'''
		pass
	
	def p_path_cnt_2(self, args):
		'''
			path_cnt ::= DSLASH ELEMENT spec path_cnt
		'''
		pass
	
	def p_path_cnt_3(self, args):
		'''
			path_cnt ::= SLASH UP spec path_cnt
		'''
		pass
	
	def p_path_cnt_4(self, args):
		'''
			path_cnt ::= SLASH STAR spec path_cnt
		'''
		rv = args[3]
		rv.insert(0, ('*', args[2][1]))
		return rv
	
	def p_path_cnt_5(self, args):
		'''
			path_cnt ::= SLASH ATTRIBUTE bind
			path_cnt ::= SLASH CALL bind
		'''
		return [(args[1].value, args[2])]
	
	def p_path_cnt_6(self, args):
		'''
			path_cnt ::=
		'''
		return Walk()
	
	def p_spec(self, args):
		'''
			spec ::= OPENSQR denial CLOSESQR bind
			spec ::= bind
		'''
		### TAG EXPRESSIONLIST CLAUSES AS RELATIVE TO VARIABLE.
		pass
	
	def p_bind(self, args):
		'''
			bind ::= ARROW VAR
			bind ::=
		'''
		if len(args) == 2:
			return args[1].value
		else:
			return None


if __name__ == '__main__':

	xps = XPathLogScanner()
	xpp = XPathLogParser()
	
	try:
		s = raw_input()
	except EOFError:
		s = '//prima[pos() = 9]/prova'
		print s
		print
	
	print xpp.parse(xps.tokenize(s))
