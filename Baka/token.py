#!/usr/bin/env python2.4
# encoding: latin-1

# copyright (c) domenico carbotta <domenico.carbotta@gmail.com>, 2005
# code released under the gnu gpl, see license.txt

'''
token.py

Classe che rappresenta un token prodotto dagli scanner XPathLog e SDD.
'''

class Token (object):
	
	def __init__(self, type, value=None):
		self.type = type
		self.value = value
	
	def __cmp__(self, other):
		return cmp(self.type, other)
	
	def __repr__(self):
		if self.value is None:
			return 'Token(%r)' % self.type
		else:
			return 'Token(%r, %r)' % (self.type, self.value)
