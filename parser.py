#!/usr/bin/env python2.4

# copyright (c) domenico carbotta <domenico.carbotta@gmail.com>, 2005
# code released under the gnu gpl, see license.txt


import yacc

from lexer import tokens


def p_expression_list(p):
	'''expression_list : expression COMMA expression_list
			| expression'''
	pass

def p_expression(p):
	'''expression : path_expression COMPARE path_expression
			| path_expression COMPARE VALUE
			| path_expression'''
	pass

def p_path_expression(p):
	'''path_expression : NOT path_expression
			| path_expression_start path_expression_cnt
			| path_expression_cnt'''
	pass

def p_path_expression_start(p):
	'''path_expression_start : ELEMENT
			| VAR
			| ATTRIBUTE
			| CALL'''
	pass

def p_path_expression_cnt(p):
	'''path_expression_cnt : SLASH ELEMENT filter bind path_expression_cnt
			| DBLSLASH ELEMENT filter bind path_expression_cnt
			| SLASH STAR filter bind path_expression_cnt
			| SLASH UP filter bind path_expression_cnt
			| SLASH CALL
			| SLASH ATTRIBUTE'''
	pass

def p_empty(p):
	'empty :'
	pass
	
def p_filter(p):
	'''filter : OPENSQR expression_list CLOSESQR
			| empty'''
	pass

def p_bind(p):
	'''bind : BIND VAR
			| empty'''
	pass

yacc.yacc(method='LALR')
