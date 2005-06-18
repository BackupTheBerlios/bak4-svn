#!/usr/bin/env python2.4
# encoding: latin-1

# copyright (c) domenico carbotta <domenico.carbotta@gmail.com>, 2005
# code released under the gnu gpl, see license.txt

'''
dlgenerator.py

Genera espressioni Datalog a partire da cammini XPathLog semplificati.
'''

from walk import *
from atom import *


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
			
			elif isinstance(step, MathAtom):
				rv.append(step)
		
		return rv
	
	def translate(self, states, start_at=0):
		datalog_expr = []
		start_at = start_at
		for state in states:
			rendered_atoms = []
			atoms = self.generate(state.steps, state.context)
			atoms = simplify_linear(atoms)
			for atom in atoms:
				print atom, type(atom)
				if isinstance(atom, MathAtom):
					rendered_atoms.append(atom.render())
					continue
				res, start_at = atom.render(start_at=start_at)
				rendered_atoms.append(res)
			datalog_expr.append(',\n'.join(rendered_atoms))
		return datalog_expr	


def simplify_linear(datalog_expr):
	# XXX
	comparisons = []
	hashes = {}
	
	for atom in datalog_expr:
		if isinstance(atom, MathAtom):
			comparisons.append(atom)
			continue
		atom_hash = atom.element, atom.parameters.get('$id', None)
		if atom_hash in hashes:
			hashes[atom_hash], rest = hashes[atom_hash].join(atom)
			comparisons.extend(rest)
		else:
			hashes[atom_hash] = atom
	
	return hashes.values() + comparisons

'''
import testhelper

doc = testhelper.sdd_azienda

atom_a = doc.create_atom('dipendente', {'$id': 'Id', 'grado': 'X',
	'nome': '"Pippo"'})
atom_b = doc.create_atom('dipendente', {'$id': 'Id', 'grado': 'Y',
	'cognome': '"Pluto"'})

for i in simplify([atom_a, atom_b]):
	print i
print '---'
for i in simplify_linear([atom_a, atom_b]):
	print i
'''
