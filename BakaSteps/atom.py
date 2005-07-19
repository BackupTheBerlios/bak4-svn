#!/usr/bin/env python2.4
# encoding: latin-1

# copyright (c) domenico carbotta <domenico.carbotta@gmail.com>, 2005
# code released under the gnu gpl, see license.txt

'''
atom.py

Rappresentazione astratta di un atomo Prolog generato a partire da un
elemento XML.
'''

def quote_prolog_vars(container):
	'''
	Restituisce una copia del dizionario o della lista passato/a come parametro
	nella quale i valori che rappresentano variabili Datalog o parametri (ossia
	tutti quelli che iniziano con la maiuscola o con un punto interrogativo)
	vengono racchiuse tra apici, come richiesto dai programmi a valle. 
	'''
	if type(container) is dict:
		# non tocchiamo il dizionario originale!
		d = container.copy()
		for k, i in d.iteritems():
			if i[0].isupper():
				d[k] = "'%s'" % i
		return d
	elif type(container) is list:
		rv = []
		for i in container:
			if i[0].isupper():
				rv.append("'%s'" % i)
			else:
				rv.append(i)
		return rv


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
				
		args = ', '.join(['%%(%s)s' % x for x in self.required_parameters])
		self.template = element + '(' + args + ')'
	
	def copy(self):
		return Atom(self, self.document, element, parameters.copy())
	
	def render(self, format='EscVar%d', start_at=1):
		n = start_at
		params = self.parameters.copy()
		for p in self.required_parameters:
			if p not in params:
				params[p] = format % n
				n += 1
		return self.template % quote_prolog_vars(params), n
	
	def compatible_with(self, other):
		# due atomi sono compatibili sse fanno riferimento allo stesso
		# tipo di elemento dello stesso documento e hanno lo stesso id.
		return (isinstance(other, Atom) and
				self.document is other.document and
				self.element == other.element and
				'$id' in self.parameters and
				'$id' in other.parameters and
				self.parameters['$id'] == other.parameters['$id'])
	
	def join(self, other):
		# genero atomi di comparazione per i valori presenti in entrambe
		# gli atomi passati come parametro.
		overlapping = [(self.parameters[x], other.parameters[x])
				for x in self.parameters if x in other.parameters]
		overlapping = [x for x in overlapping if x[0] != x[1]]
		explain_overlapping = [MathAtom('=', *x) for x in overlapping]
		
		# unisco le informazioni contenute nelle due liste dei parametri.
		params = self.parameters.copy()
		params.update(other.parameters)
		
		return Atom(self.document, self.element, params), explain_overlapping

	def render_unescaped(self):
		params = self.required_parameters
		# creo un dizionario che contiene come chiavi i parametri dell'atomo
		# e come valori caratteri underscore.
		unescaped = dict.fromkeys(params, '_')
		unescaped.update(self.parameters)
		return self.template % unescaped
	
	def __str__(self):
		return self.render_unescaped()


class MathAtom (object):
	
	def __init__(self, op, *parameters):
		self.op = op
		self.parameters = list(parameters)
	
	def render(self):
		return "'" + self.op + "'(" + \
				', '.join(quote_prolog_vars(self.parameters)) + ")"
	
	def __str__(self):
		return self.render()
