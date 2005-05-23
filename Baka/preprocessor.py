#!/usr/bin/env python2.4
# encoding: latin-1

# copyright (c) domenico carbotta <domenico.carbotta@gmail.com>, 2005
# code released under the gnu gpl, see license.txt

'''
preproccessor.py

Risolve i cammini complessi (contenenti StarStep, UpStep, BridgeStep e
BridgeAttribStep) trasformandoli in cammini semplici, contenenti solo
SimpleStep ed AttribStep.
'''

from walk import *
from atom import *


class State (object):
	
	def __init__(self, preprocessor, steps=None, context=None):
		if steps is None:
			steps = []
		if context is None:
			context = {}
		self.steps = steps
		self.context = context
		self.preprocessor = preprocessor
	
	def copy(self):
		return State(self.preprocessor, self.steps[:], self.context.copy())
	
	def add(self, steps_addition, context_addition):
		self.steps.extend(steps_addition)
		self.context.update(context_addition)
		return self
	
	def fork(self, steps_addition, context_addition):
		return self.copy().add(steps_addition, context_addition)
	
	def __repr__(self):
		return '<%r, %r>' % (self.steps, self.context)
	
	def render(self):
		rv = 'state:\n'
		rv += '\tsteps:\n'
		for step in self.steps:
			rv += '\t\t' + step.render() + '\n'
		rv += '\tcontext:\n'
		rv += '\t\t' + repr(self.context)[1:-1]
		return rv


class Preprocessor (object):
		
	def __init__(self, document):
		self.document = document
		self.varcount = 0
		self.varformat = 'LinVar%02d'
	
	def new_var(self):
		self.varcount += 1
		return self.varformat % self.varcount
	
	def remove_stars(self, steps):
		resolver = self.document.resolver
		states = [State(self)]
		
		for step in steps:
			
			print step.render()
			
			# <spaghetti_code>

			if isinstance(step, (SimpleStep, BridgeStep)):
				for state in states:
					state.add([step], {step.id: step.qualifier})
			
			elif isinstance(step, (AttribStep, BridgeAttribStep)):
				for state in states:
					state.add([step], {step.id: '$'})
						
			elif isinstance(step, StarStep):
				rv = []
				start_el = state.context[step.start]
				for state in states:
					for type in resolver.resolve_star(start_el):
						tx = [SimpleStep(type, step.id, step.start)]
						rv.append(state.fork(tx, {step.id: type}))
				states = rv
			
			elif isinstance(step, UpStep):
				rv = []
				start_el = state.context[step.start]
				for state in states:
					for type in resolver.resolve_up(start_el):
						new_id = self.new_var()
						tx = [BridgeStep(type, new_id),
							AttribStep('$parent', new_id, step.id)]
						rv.append(state.fork(tx, {new_id: type}))
					states = rv
				
			elif isinstance(step, BridgeAttribStep):
				pass
			
			elif isinstance(step, Comparison):
				for state in states:
					state.add([step], {})
			
			else:
				raise Exception, step
			
			# </spaghetti_code>
						
			for state in states:
				print state.render()
			print



if __name__ == '__main__':
	
	import baka
	
	document, steps = baka.main(['', 'integration test/azienda.sdd',
			'integration test/check_stipendio.xpl'])
	
	steps_a = [BridgeStep('dirigenza', 'A'), StarStep('B', start='A')]
	steps_b = [BridgeStep('retribuzione', 'C'), UpStep('D', start='C')]
	print
	print '---'
	print
	
	pp = Preprocessor(document)
	pp.remove_stars(steps_a)
	
	print
	print '...'
	print
	
	pp.remove_stars(steps_b)
