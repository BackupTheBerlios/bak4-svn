#!/usr/bin/env python2.4
# encoding: latin-1

# copyright (c) domenico carbotta <domenico.carbotta@gmail.com>, 2005
# code released under the gnu gpl, see license.txt

'''
walk.py

Comprende le classi che costituiscono una rappresentazione astratta
delle espressioni XPathLog.
'''

class Walk (object):
	
	def __init__(self, refers_to=None):
		self.refers_to = refers_to
		self.steps = []
	
	def insert(self, pos, step):
		self.steps.insert(pos, step)
		return self
	
	def __repr__(self):
		s = ""
		s += 'Walk'
		if self.refers_to is not None:
			s += ' (starting from %s)' % self.refers_to
		s += ':\n'
		for i in self.steps:
			s += '\t' + repr(i) + '\n'
		return s


class Step (object):

	def __init__(self, qualifier, id, start=None):
		self.qualifier = qualifier
		self.id = id
		self.start = start
	
	def render(self):
		raise NotImplementedException


class SimpleStep (Step):
	
	def __init__(self, qualifier, id, start=None):
		Step.__init__(self, qualifier, id, start)
	
	def __repr__(self):
		return 'SimpleStep(%r, %r, %r)' % (self.qualifier, self.id, self.start)
	
	def render(self):
		return self.start + '/' + self.qualifier + '->' + self.id 


class StarStep (Step):
	
	def __init__(self, id, start=None):
		Step.__init__(self, '*', id, start)

	def __repr__(self):
		return 'StarStep(%r, %r)' % (self.id, self.start)

	def render(self):
		return self.start + '/*->' + self.id 


class BridgeStep (Step):
	
	def __init__(self, qualifier, id, start=None):
		Step.__init__(self, qualifier, id, start)

	def __repr__(self):
		return 'BridgeStep(%r, %r, %r)' % (self.qualifier, self.id, self.start)

	def render(self):
		if self.start is None:
			return '//' + self.qualifier + '->' + self.id
		else:
			return self.start + '//' + self.qualifier + '->' + self.id 


class UpStep (Step):
	
	def __init__(self, id, start=None):
		Step.__init__(self, '..', id, start)

	def __repr__(self):
		return 'UpStep(%r, %r)' % (self.id, self.start)
	
	def render(self):
		return self.start + '/..->' + self.id 


class AttribStep (Step):
	
	def __init__(self, qualifier, id, start=None):
		Step.__init__(self, qualifier, id, start)

	def __repr__(self):
		return 'AttribStep(%r, %r, %r)' % (self.qualifier, self.id, self.start)

	def render(self):
		if self.qualifier.startswith('$'):
			return self.start + '/' + self.qualifier[1:] + '()->' + self.id
		else:
			return self.start + '/@' + self.qualifier + '->' + self.id 



class BridgeAttribStep (Step):
	
	def __init__(self, qualifier, id, start=None):
		Step.__init__(self, qualifier, id, start)

	def __repr__(self):
		return 'BridgeAttribStep(%r, %r, %r)' % \
				(self.qualifier, self.id, self.start)
	
	def render(self):
		if self.start is None:
			if self.qualifier.startswith('$'):
				return '//@' + self.qualifier + '->' + self.id 
			else:
				return '//' + self.qualifier[1:] + '()->' + self.id
		else:
			if self.qualifier.startswith('$'):
				return self.start + '//@' + self.qualifier + '->' + self.id 
			else:
				return self.start + '//' + self.qualifier[1:] + '()->' + self.id

class Comparison (object):
	
	def __init__(self, lhs, op, rhs):
		self.lhs = lhs
		self.op = op
		self.rhs = rhs
	
	def __repr__(self):
		return "Comparison('%s', '%s', '%s')" % (self.lhs, self.op, self.rhs)
	
	def render(self):
		return self.lhs + ' ' + self.op + ' ' + self.rhs
