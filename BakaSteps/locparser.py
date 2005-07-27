#!/usr/bin/env python2.4
# encoding: latin-1

# copyright (c) domenico carbotta <domenico.carbotta@gmail.com>, 2005
# code released under the gnu gpl, see license.txt

'''
locparser.py

Parser per una versione semplificata del linguaggio XPathLog utilizzata per
localizzare il nodo su cui viene effettuato l'update.
Per la specifica completa del linguaggio fare riferimento alla documentazione
che accompagna il programma.
'''

from spark07 import GenericParser
from xplscanner import XPathLogScanner
from mytoken import Token
from step import * 
from atom import AuxAtom


def join(step, step_list):
	if len(step_list) > 0:
		step_list[0].start = step.id
	return [step] + step_list


class LocParsingException (Exception):
	'''
		Eccezione sollevata dal parser in caso di errore.
	'''
	pass


class LocParser (GenericParser):
	'''
		Questa classe implementa un parser per una versione ridotta del
		linguaggio XPathLog utilizzata per localizzare il nodo su cui viene
		effettuato l'update, utilizzando la libreria SPARK sviluppata da
		John Aycock della University of Calgary.
		
		Per ulteriori informazioni su SPARK:
			http://pages.cpsc.ucalgary.ca/~aycock/spark/
	'''
	
	def __init__(self, start='location'):
		GenericParser.__init__(self, start)
		self.aux_atoms = []
		self.generated_id_count = 0
		self.generated_var_count = 0
	
	def new_id(self):
		rv = '?i%d' % self.generated_id_count
		self.generated_id_count += 1
		return rv
	
	def new_var(self):
		rv = 'JoinVar%d' % self.generated_var_count
		self.generated_var_count += 1
		return rv
	
	def p_location(self, args):
		'''
			location ::= abbr_path
			location ::= abs_path
		'''
		return args[0] + self.aux_atoms
	
	def p_abs_path(self, args):
		'''
			abs_path ::= DOCUMENT OPENPAR STRINGVALUE CLOSEPAR path_cnt
		'''
		docname = self.new_id()
		self.aux_atoms.append(AuxAtom('$document', args[2].value, docname))
		args[4][0].start = docname
		return args[4]
	
	def p_abbr_path(self, args):
		'''
			abbr_path ::= DSLASH ELEMENT filter path_cnt
		'''
		return join(BridgeStep(Ground, args[1].value, args[2]), args[3])
	
	def p_path_cnt_1(self, args):
		'''
			path_cnt ::= SLASH ELEMENT filter path_cnt
		'''
		return join(LinearStep(None, args[1].value, args[2]), args[3])
	
	def p_path_cnt_2(self, args):
		'''
			path_cnt ::= DSLASH ELEMENT filter path_cnt
		'''
		return join(BridgeStep(None, args[1].value, args[2]), args[3])
	
	def p_path_cnt_3(self, args):
		'''
			path_cnt ::=
		'''
		return []
	
	def p_filter_1(self, args):
		'''
			filter ::= OPENSQR expressions CLOSESQR
		'''
		rv = self.new_id()
		for atom in args[1]:
			atom.start = rv
		self.aux_atoms.extend(args[1])
		return rv
		
	def p_filter_2(self, args):
		'''
			filter ::=
		'''
		return self.new_id()
	
	def p_comparisons_1(self, args):
		'''
			expressions ::= expression COMMA expressions
		'''
		return args[0] + args[2]

	def p_comparisons_2(self, args):
		'''
			expressions ::= expression
		'''
		return args[0]
	
	def p_binding(self, args):
		'''
			expression ::= ATTRIBUTE ARROW VAR
			expression ::= CALL ARROW VAR
		'''
		return [AttribStep(Floating, args[0].value, args[2].value)]
	
	def p_comparison(self, args):
		'''
			expression ::= comparable COMPARE comparable
		'''
		return [AuxAtom(args[1].value, args[0][0], args[2][0])] + \
				args[0][1] + args[2][1]
	
	def p_comparable_1(self, args):
		'''
			comparable ::= ATTRIBUTE
			comparable ::= CALL
		'''
		nv = self.new_var()
		return nv, [AttribStep(Floating, args[0].value, nv)]
	
	def p_comparable_2(self, args):
		'''
			comparable ::= NUMVALUE
			comparable ::= STRINGVALUE
			comparable ::= VAR
		'''
		return args[0].value, []
	
	def error(self, token):
		raise LocParsingException, 'Error: unexpected token near "%s".' \
			% token.value


from xplscanner import *

xps = XPathLogScanner()
locp = LocParser()

s = '''
		//azienda[@nome = "Rossi"]//reparto[@nome = "R&D"]
'''

h = xps.tokenize(s)
k = locp.parse(h)
for i in k: print i

print 'ok'
