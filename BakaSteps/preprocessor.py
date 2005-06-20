#!/usr/bin/env python2.4
# encoding: latin-1

# copyright (c) domenico carbotta <domenico.carbotta@gmail.com>, 2005
# code released under the gnu gpl, see license.txt

'''
preproccessor.py

Risolve i cammini complessi (contenenti StarStep, UpStep, BridgeStep e
BridgeAttribStep) trasformandoli in cammini semplici, contenenti solo
LinearStep ed AttribStep.
'''

from walk import *
from atom import *

'''


COMMENTA QUESTO MODULO PRIMA CHE SIA TROPPO TARDI!!!


'''

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
		return self.render()
	
	
	def render(self):
		rv = 'state:\n'
		rv += '\tsteps:\n'
		for step in self.steps:
			rv += '\t\t' + step.render() + '\n'
		rv += '\tcontext:\n'
		for var, type in self.context.iteritems():
			rv += '\t\t%s: %s\n' % (var, type)
		return rv


class Preprocessor (object):
	
	def __init__(self, document, varcount=0):
		self.document = document
		self.varcount = varcount
		self.varformat = 'LinVar%d'
	
	
	def process(self, steps):
		st = self.remove_stars(steps)
		return self.build_bridges(st)
	
	
	def new_var(self):
		self.varcount += 1
		return self.varformat % self.varcount
	
	
	def remove_stars(self, steps):
		resolver = self.document.resolver
		states = [State(self)]
		
		for step in steps:
	
			if isinstance(step, (LinearStep, BridgeStep)):
				for state in states:
					state.add([step], {step.id: step.qualifier})
			
			elif isinstance(step, (AttribStep, BridgeAttribStep)):
				for state in states:
					state.add([step], {step.id: '$'})
						
			elif isinstance(step, StarStep):
				rv = []
				for state in states:
					start_el = state.context[step.start]
					for type in resolver.resolve_star(start_el):
						branch = [LinearStep(step.start, type, step.id)]
						rv.append(state.fork(branch, {step.id: type}))
				states = rv
			
			elif isinstance(step, UpStep):
				rv = []			
				for state in states:
					start_el = state.context[step.start]
					for alternative in resolver.resolve_up(start_el):
						# attenzione: $A/..->$B va tradotto come
						# tipo_a($A, _, $B, ...)
						# cioè con un LinearStep che parta da step.id
						# e arrivi a step.start (totale asimmetria).
						branch = [LinearStep(step.id, state.context[step.start],
								step.start)]
						rv.append(state.fork(branch, {step.id: alternative}))
				states = rv
				
			elif isinstance(step, MathAtom):
				for state in states:
					state.add([step], {})
			
			else:
				raise Exception, step
			
			print 'XXX'
			print step.render()
			for state in states:
				print state.render()
		
		return states
	
	
	def build_bridges(self, states):
		resolver = self.document.resolver
		rv = []
		
		for state in states:
		
			state_expansions = [State(self, [], state.context)]
			
			for step in state.steps:
				
				if isinstance(step, BridgeStep) and step.start is not Ground:
					routes = resolver.resolve_bridge(state.context[step.start],
							step.qualifier)
					branches = []
					for route in routes:
						branch = []
						branch_context = {}
						last_step = step.start
						for item in route[1:-1]:
							nv = self.new_var()
							branch.append(LinearStep(item, nv, last_step))
							branch_context[nv] = item
							last_step = nv
						branch.append(LinearStep(step.qualifier, step.id,
								last_step))
						branches.append((branch, branch_context))
					
					sx_new = []
					for branch, branch_context in branches:
						sx_new.extend([exp.fork(branch, branch_context)
								for exp in state_expansions])
					state_expansions = sx_new
	
				elif isinstance(step, BridgeAttribStep) \
						and step.start is not Ground:
					
					routes = resolver.resolve_bridge_attrib(
							state.context[step.start], step.qualifier)
					branches = []
					
					for route in routes:
						branch = []
						branch_context = {}
						last_step = step.start
						for item in route[1:]:
							nv = self.new_var()
							branch.append(LinearStep(item, nv, last_step))
							branch_context[nv] = item
							last_step = nv
						branch.append(AttribStep(step.qualifier, step.id,
								last_step))
						branches.append((branch, branch_context))
					
					sx_new = []
					
					for branch, branch_context in branches:
						sx_new.extend([exp.fork(branch, branch_context)
								for exp in state_expansions])
					state_expansions = sx_new
				
				elif isinstance(step, BridgeAttribStep) and step.start is None:
					
					alternatives = [x for x in self.document.elements
						if step.qualifier in self.document.elements[x]]
					branches = []
					
					for alternative in alternatives:
						nv = self.new_var()
						branch = [BridgeAttribStep(alternative, nv, None),
								AttribStep(qualifier, id, nv)]
						branch_context = {nv: alternative, id: '$'}
						branches.append((branch, branch_context))
					
					sx_new = []
					
					for branch, branch_context in branches:
						sx_new.extend([exp.fork(branch, branch_context)
								for exp in state_expansions])
					state_expansions = sx_new
				
				else:
					for exp in state_expansions:
						exp.add([step], {})
			
			rv.extend(state_expansions[:])
		
		return rv
