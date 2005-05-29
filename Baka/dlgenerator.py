#!/usr/bin/env python2.4
# encoding: latin-1

# copyright (c) domenico carbotta <domenico.carbotta@gmail.com>, 2005
# code released under the gnu gpl, see license.txt

'''
dlgenerator.py

Genera espressioni Datalog a partire da cammini XPathLog semplificati.
'''

from walk import *


class DatalogGenerator (object):
	
	def __init__(self, document, varcount=0):
		self.document = document
		
	def generate(self, steps, context):
		print steps
		print context
		
		rv = []
		
		for step in steps:
			
			if isinstance(step, SimpleStep):
				rv.append(self.document.create_atom(step.qualifier,
						{'$id': step.id, '$parent': step.start}))
			
			elif isinstance(step, AttribStep):
				rv.append(self.document.create_atom(context[step.start],
						{'$id': step.start, step.qualifier: step.id}))
			
			elif isinstance(step, BridgeStep) and step.start is None:
				rv.append(self.document.create_atom(step.qualifier,
						{'$id': step.id}))
		return rv
	
	
	def translate(self, states, start_at=0):
		datalog_expr = []
		start_at = start_at
		for state in states:
			rendered_atoms = []
			atoms = self.generate(state.steps, state.context)
			atoms = simplify(atoms)
			for atom in atoms:
				res, start_at = atom.render(start_at=start_at)
				rendered_atoms.append(res)
			datalog_expr.append(',\n'.join(rendered_atoms))
		return datalog_expr


def simplify(datalog_expr):
	rv = []
	
	for atom_a in datalog_expr:
		joined = False
		for atom_b in rv:
			if atom_a.compatible_with(atom_b):
				rv.remove(atom_b)
				rv.append(atom_a.join(atom_b))
				joined = True
				print '%s %s OK' % (atom_a, atom_b)
			else:
				print '%s %s NO' % (atom_a, atom_b)
		if not joined:
			rv.append(atom_a)
	
	return rv
