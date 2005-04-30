#!/usr/bin/env python2.4

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
			s += ' (starting from %s)' % (self.refers_to)
		s += ':\n'
		for i in self.steps:
			s += '\t' + repr(i) + '\n'
		return s


class Step (object):

	def __init__(self, qualifier, id):
		self.qualifier = qualifier
		self.id = id
	
	def __repr__(self):
		return 'Step(%s, %s)' % (self.qualifier, self.id)


class StarStep (Step):
	
	def __init__(self, id):
		Step.__init__(self, '*', id)

	def __repr__(self):
		return 'StarStep(%s)' % (self.id)


class BridgeStep (Step):
	
	def __init__(self, qualifier, id):
		Step.__init__(self, qualifier, id)

	def __repr__(self):
		return 'BridgeStep(%s, %s)' % (self.qualifier, self.id)


class UpStep (Step):
	
	def __init__(self, id):
		Step.__init__(self, '..', id)

	def __repr__(self):
		return 'UpStep(%s)' % (self.id)


class AttribStep (Step):
	
	def __init__(self, qualifier, id):
		Step.__init__(self, qualifier, id)

	def __repr__(self):
		return 'AttribStep(%s, %s)' % (self.qualifier, self.id)


class Comparison (object):
	
	def __init__(self, lhs, op, rhs):
		self.lhs = lhs
		self.op = op
		self.rhs = rhs
	
	def __repr__(self):
		return 'Comparison(%s, %s, %s)' % (self.lhs, self.op, self.rhs)
