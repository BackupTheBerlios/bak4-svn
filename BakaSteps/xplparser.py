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
from atom import MathAtom


def join(step, step_list):
	if len(step_list) > 0:
		step_list[0].start = step.id
	return [step] + step_list


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
		self.generated_var_count = 0
	
	def p_denial(self, args):
		'''
			denial ::= expression_list
		'''
		rv = args[0] + self.filters + self.comparisons
		rv.sort()
		for i in rv:
			print i
		return rv
	
	def p_expression_list_1(self, args):
		'''
			expression_list ::= expression COMMA expression_list
		'''
		return args[0] + args[2]
	
	def p_expression_list_2(self, args):
		'''
			expression_list ::= expression
		'''
		return args[0]
	
	def p_expression_1(self, args):
		'''
			expression ::= compare_term COMPARE compare_term
		'''
		self.comparisons.append(
				MathAtom(args[1].value, args[0][0], args[2][0]))
		return args[0][1] + args[2][1]
	
	def p_expression_2(self, args):
		'''
			expression ::= path
		'''
		return args[0]
		
	def p_compare_term_1(self, args):
		'''
			compare_term ::= path
		'''
		return (args[0][-1].id, args[0])
	
	def p_compare_term_2(self, args):
		'''
			compare_term ::= VAR
			compare_term ::= math
		'''
		return (args[0].value, [])
	
	def p_path_1(self, args):
		'''
			path ::= VAR path_cnt_nonempty
		'''
		args[1][0].start = args[0].value
		return args[1]
	
	def p_path_2(self, args):
		'''
			path ::= DSLASH ELEMENT spec path_cnt
		'''
		return join(BridgeStep(Ground, args[1].value, args[2]), args[3])
	
	def p_path_3(self, args):
		'''
			path ::= UP spec path_cnt
		'''
		return join(UpStep(Floating, args[1]), args[2])
	
	def p_path_4(self, args):
		'''
			path ::= STAR spec path_cnt
		'''
		return join(StarStep(Floating, args[1]), args[2])
	
	def p_path_5(self, args):
		'''
			path ::= ELEMENT spec path_cnt
		'''
		return join(LinearStep(Floating, args[0].value, args[1]), args[2])
	
	def p_path_6(self, args):
		'''
			path ::= ATTRIBUTE bind
			path ::= CALL bind
		'''
		return [AttribStep(Floating, args[0].value, args[1])]
	
	def p_path_7(self, args):
		'''
			path ::= DSLASH ATTRIBUTE bind
		'''
		return [BridgeAttribStep(Ground, args[1].value, args[2])]
	
	def p_path_cnt(self, args):
		'''
			path_cnt ::= path_cnt_empty
			path_cnt ::= path_cnt_nonempty
		'''
		return args[0]
	
	def p_path_cnt_nonempty_1(self, args):
		'''
			path_cnt_nonempty ::= SLASH ELEMENT spec path_cnt
		'''
		return join(LinearStep(None, args[1].value, args[2]), args[3])
	
	def p_path_cnt_nonempty_2(self, args):
		'''
			path_cnt_nonempty ::= DSLASH ELEMENT spec path_cnt
		'''
		return join(BridgeStep(None, args[1].value, args[2]), args[3])
	
	def p_path_cnt_nonempty_3(self, args):
		'''
			path_cnt_nonempty ::= SLASH UP spec path_cnt
		'''
		return join(UpStep(None, args[2]), args[3])
	
	def p_path_cnt_nonempty_4(self, args):
		'''
			path_cnt_nonempty ::= SLASH STAR spec path_cnt
		'''
		return join(StarStep(None, args[2]), args[3])
	
	def p_path_cnt_nonempty_5(self, args):
		'''
			path_cnt_nonempty ::= SLASH ATTRIBUTE bind
			path_cnt_nonempty ::= SLASH CALL bind
		'''
		return [AttribStep(None, args[1].value, args[2])]
	
	def p_path_cnt_nonempty_6(self, args):
		'''
			path_cnt_nonempty ::= DSLASH ATTRIBUTE bind
			path_cnt_nonempty ::= DSLASH CALL bind
		'''
		return [BridgeAttribStep(None, args[1].value)]
	
	def p_path_cnt_empty(self, args):
		'''
			path_cnt_empty ::=
		'''
		return []
	
	def p_spec(self, args):
		'''
			spec ::= OPENSQR expression_list CLOSESQR bind
			spec ::= bind
		'''
		if len(args) == 1:
			return args[0]
		else:
			for step in args[1]:
				if step.start is Floating:
					step.start = args[3]
			self.filters += args[1]
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
			math ::= STRINGVALUE
			math ::= math_expr
			
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


if __name__ == '__main__':
	main()	
