#!/usr/bin/env python2.4
# encoding: latin-1

# copyright (c) domenico carbotta <domenico.carbotta@gmail.com>, 2005
# code released under the gnu gpl, see license.txt

'''
atom.py

Rappresentazione astratta di un atomo Prolog generato a partire da un
elemento XML.
'''

def quote_prolog_vars(dictionary):
	'''
	Restituisce una copia del dizionario passato come parametro nella quale i
	valori che rappresentano variabili Prolog (ossia tutti quelli che iniziano
	con la maiuscola...) sono virgolettati, come richiesto dai programmi a
	velementse. 
	'''
	d = dictionary.copy()    # non tocchiamo il dizionario originale!
	for k, i in d.iteritems():
		if i[0].isupper():
			d[k] = "'" + i + "'"
	return d


class Atom (object):
	
	def __init__(self, document, element, parameters=None):
		self.document = document
		
		self.element = element
		
		if parameters is None:
			self.parameters = {}
		else:
			self.parameters = parameters

		# costruzione del template
		self.required_parameters = ['$id', '$pos']
		
		if self.document.has_parent(self.element):
			self.required_parameters.append('$parent')
		
		self.required_parameters.extend(self.document.elements[self.element])
		
		if self.element in self.document.pcdata:
			self.required_parameters.append('$text')
		
		args = ', '.join(['%%(%s)s' % x for x in self.required_parameters])
		self.template = element + '(' + args + ')'
		
	def render(self, format='Var%02d', start_at=1):
		n = start_at
		params = self.parameters.copy()
		for p in self.required_parameters:
			if p not in params:
				params[p] = format % n
				n += 1
		return self.template % quote_prolog_vars(params), n
	
	def __str__(self):
		l = self.required_parameters
		d = dict(zip(l, ['_'] * len(l))) 
		return self.template % d
