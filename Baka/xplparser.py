#!/usr/bin/env python2.4
# encoding: latin-1

# copyright (c) domenico carbotta <domenico.carbotta@gmail.com>, 2005
# code released under the gnu gpl, see license.txt

'''
xplparser.py

Parser per una versione semplificata del linguaggio XPathLog.
Per la specifica completa del linguaggio fare riferimento alla documentazione
che accompagna il programma.
'''

from spark07 import GenericParser
from xplscanner import XPathLogScanner
from mytoken import Token
from walk import * 


class XPLParsingException (Exception):
	'''
		Eccezione sollevata dal parser in caso di errore.
	'''
	pass


class XPathLogParser (GenericParser):
	'''
		Questa classe implementa un parser per una versione ridotta del
		linguaggio XPathLog utilizzando la libreria SPARK sviluppata da
		John Aycock della University of Calgary.
		
		Per ulteriori informazioni su SPARK:
			http://pages.cpsc.ucalgary.ca/~aycock/spark/
	'''
	
	def __init__(self, start='denial'):
		GenericParser.__init__(self, start)
		self.filters = []
		self.comparisons = []
		self.walks = []
		self.generated_var_count = 0
	
	def postprocess(self, walks):
		rv = []
		for item in walks:
			if not isinstance(item, Walk):
				rv.append(item)
				continue
			steps = item.steps[:]
			last_step = item.refers_to
			for step in steps:
				step.start = last_step
				last_step = step.id
			rv.extend(steps)
		return rv
		
	def p_denial(self, args):
		'''
			denial ::= expression_list
		'''
		self.walks = args[0]
		self.walks.extend(self.filters)
		return self.postprocess(self.walks + self.comparisons)
	
	def p_expression_list_1(self, args):
		'''
			expression_list ::= expression COMMA expression_list
		'''
		if args[2] is not None:
			args[2].insert(0, args[0])
		return args[2]
	
	def p_expression_list_2(self, args):
		'''
			expression_list ::= expression
		'''
		if args[0] is None:
			return []
		else:
			return args
	
	def p_expression_1(self, args):
		'''
			expression ::= VAR COMPARE comparison_rhs
		'''
		# in teoria, l'AP non-deterministico corrispondente a questa grammatica
		# riconoscerebbe la stringa in due rami di esecuzione diversi
		# (questo e il prossimo);  l'AP deterministico implementato
		# da SPARK si "accontenta" di espandere questa produzione.
		# è il comportamento che desideriamo.
		self.comparisons.append(Comparison(args[0].value, args[1].value,
			args[2].value))
		
	def p_expression_2(self, args):
		'''
			expression ::= path COMPARE comparison_rhs
			expression ::= path
		'''
		if len(args) == 3:
			last_step_id = args[0].steps[-1].id
			self.comparisons.append(Comparison(last_step_id, args[1].value,
				args[2].value))
		return args[0]
	
	def p_path_1(self, args):
		'''
			path ::= VAR path_cnt
		'''
		if len(args[1].steps) == 0:
			return None
		else:
			args[1].refers_to = args[0].value
			return args[1]
	
	def p_path_2(self, args):
		'''
			path ::= DSLASH ELEMENT spec path_cnt
		'''
		return args[3].insert(0, BridgeStep(args[1].value, args[2]))
	
	def p_path_3(self, args):
		'''
			path ::= UP spec path_cnt
		'''
		return args[2].insert(0, UpStep(args[1]))

	def p_path_4(self, args):
		'''
			path ::= STAR spec path_cnt
		'''
		return args[2].insert(0, StarStep(args[1]))
	
	def p_path_5(self, args):
		'''
			path ::= ELEMENT spec path_cnt
		'''
		return args[2].insert(0, SimpleStep(args[0].value, args[1]))
	
	def p_path_6(self, args):
		'''
			path ::= ATTRIBUTE bind
			path ::= CALL bind
		'''
		return Walk().insert(0, AttribStep(args[0].value, args[1]))
	
	def p_path_7(self, args):
		'''
			path ::= DSLASH ATTRIBUTE bind
		'''
		return Walk().insert(0, BridgeAttribStep(args[1].value, args[2]))
	
	def p_path_cnt_1(self, args):
		'''
			path_cnt ::= SLASH ELEMENT spec path_cnt
		'''
		return args[3].insert(0, SimpleStep(args[1].value, args[2]))
	
	def p_path_cnt_2(self, args):
		'''
			path_cnt ::= DSLASH ELEMENT spec path_cnt
		'''
		return args[3].insert(0, BridgeStep(args[1].value, args[2]))
	
	def p_path_cnt_3(self, args):
		'''
			path_cnt ::= SLASH UP spec path_cnt
		'''
		return args[3].insert(0, UpStep(args[2]))
	
	def p_path_cnt_4(self, args):
		'''
			path_cnt ::= SLASH STAR spec path_cnt
		'''
		return args[3].insert(0, StarStep(args[2]))
	
	def p_path_cnt_5(self, args):
		'''
			path_cnt ::= SLASH ATTRIBUTE bind
			path_cnt ::= SLASH CALL bind
		'''
		return Walk().insert(0, AttribStep(args[1].value, args[2]))
	
	def p_path_cnt_6(self, args):
		'''
			path_cnt ::= DSLASH ATTRIBUTE bind
			path_cnt ::= DSLASH CALL bind
		'''
		return Walk().insert(0, BridgeAttribStep(args[1].value, args[2]))		

	def p_path_cnt_7(self, args):
		'''
			path_cnt ::=
		'''
		return Walk()
	
	def p_spec(self, args):
		'''
			spec ::= OPENSQR expression_list CLOSESQR bind
			spec ::= bind
		'''
		if len(args) == 1:
			return args[0]
		else:
			for expression in args[1]:
				expression.refers_to = args[3]
			self.filters.extend(args[1])
			return args[3]
	
	def p_bind(self, args):
		'''
			bind ::= ARROW VAR
			bind ::=
		'''
		if len(args) == 2:
			return args[1].value
		else:
			rv = 'StepVar%d' % self.generated_var_count
			self.generated_var_count += 1
			return rv
	
	def p_math(self, args):
		'''
			comparison_rhs ::= math_expr
			comparison_rhs ::= string_expr
			
			string_expr ::= string_operand PLUS string_expr
			string_expr ::= string_operand
			string_operand ::= STRINGVALUE
			string_operand ::= VAR
			
			math_expr ::= math_prod PLUS math_expr
			math_expr ::= math_prod MINUS math_expr
			math_expr ::= math_prod
			
			math_prod ::= math_factor STAR math_prod
			math_prod ::= math_factor SLASH math_prod
			math_prod ::= math_factor
			
			math_factor ::= MINUS math_operand
			math_factor ::= math_operand
			
			math_operand ::= NUMVALUE
			math_operand ::= VAR
			math_operand ::= OPENPAR math_expr CLOSEPAR
		'''
		# queste sono produzioni "standard" che danno luogo a due tipi di
		# operazione: espressioni aritmetiche tra numeri e variabili o, in
		# alternativa, operazioni di concatenazione tra stringhe e variabili.
		# la valutazione delle espressioni è lasciata come esercizio
		# all'interprete XQuery.
		return Token(None, ' '.join([x.value for x in args]))
	
	def error(self, token):
		raise XPLParsingException, 'Error: unexpected token "%s".' \
			% token.value
	

def main(ask_for_return=False):
	import sys
	interactive = '--stdin' in sys.argv
	
	xps = XPathLogScanner()
	xpp = XPathLogParser()
	
	if interactive:
		s = raw_input()
	else:
		s = open('integration test/check_alfabetico.xpl').read()
		print s
	
	k = xpp.parse(xps.tokenize(s))
	
	if ask_for_return:
		return k
	
	for i in k:
		print i


if __name__ == '__main__':
	main()	
