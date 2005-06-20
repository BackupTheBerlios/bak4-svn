#!/usr/bin/env python2.4
# encoding: latin-1

# copyright (c) domenico carbotta <domenico.carbotta@gmail.com>, 2005
# code released under the gnu gpl, see license.txt

'''
steps.py

Comprende le classi che costituiscono una rappresentazione astratta
delle espressioni XPathLog.
'''


class __GroundSingleton (object):
	def __repr__(self): return 'Ground'

Ground = __GroundSingleton()


class __FloatingSingleton (object):
	def __repr__(self): return 'Floating'
Floating = __FloatingSingleton()


class CircularDependencyException (Exception):
	pass


class Step (object):

	Name = None
	
	def __init__(self, start, id):
		self.start = start
		self.id = id
	
	def render(self):
		raise NotImplementedException
	
	def __str__(self):
		return self.render()
	
	def __repr__(self):
		return '%s(%r, %r)' % (self.Name, self.start, self.id)
	
	def __cmp__(self, other):
		if not isinstance(other, Step):
			return -1
		if self.start == other.id:
			if self.id == other.start:
				raise CircularDependancyException, (self.start, other.start)
			return 1
		elif self.id == other.start:
			return -1
		else:
			return cmp(self.start, other.start)


class QualifiedStep (Step):
	
	def __init__(self, start, qualifier, id):
		Step.__init__(self, start, id)
		self.qualifier = qualifier
	
	def __repr__(self):
		return '%s(%r, %r, %r)' % (self.Name, self.start, self.qualifier,
				self.id)


class LinearStep (QualifiedStep):
	
	Name = 'LinearStep'
	
	def render(self):
		return self.start + '/' + self.qualifier + '->' + self.id 


class StarStep (Step):
	
	Name = 'StarStep'
	
	def render(self):
		return self.start + '/*->' + self.id 


class BridgeStep (QualifiedStep):
		
	Name = 'BridgeStep'

	def render(self):
		if self.start is Ground:
			return '//' + self.qualifier + '->' + self.id
		else:
			return self.start + '//' + self.qualifier + '->' + self.id 


class UpStep (Step):
		
	Name = 'UpStep'

	def render(self):
		return self.start + '/..->' + self.id 


class AttribStep (QualifiedStep):

	Name = 'AttribStep'
	
	def render(self):
		if self.qualifier.startswith('$'):
			return self.start + '/' + self.qualifier[1:] + '()->' + self.id
		else:
			return self.start + '/@' + self.qualifier + '->' + self.id 


class BridgeAttribStep (QualifiedStep):
	
	Name = 'BridgeAttribStep'
	
	def render(self):
		if self.start is Ground:
			if self.qualifier.startswith('$'):
				return '//@' + self.qualifier + '->' + self.id 
			else:
				return '//' + self.qualifier[1:] + '()->' + self.id
		else:
			if self.qualifier.startswith('$'):
				return self.start + '//@' + self.qualifier + '->' + self.id 
			else:
				return self.start + '//' + self.qualifier[1:] + '()->' + self.id
