#!/usr/bin/env python2.4
# encoding: latin-1

# copyright (c) domenico carbotta <domenico.carbotta@gmail.com>, 2005
# code released under the gnu gpl, see license.txt

'''
hypgenerator.py

Genera le ipotesi aggiuntive a partire da atomi Datalog positivi (usato per
il percorso di inserimento dell'update).
'''

from atom import *


def core(atom):
	return atom.document.create_atom(
			atom.element, {'$id': atom.parameters['$id']})


def is_var(x):
	return type(x) is str and x[0].isupper()


def is_ground(x):
	return type(x) is str and not x[0].isupper()


class HypGenerator (object):
	
	def __init__(self, document, start_at=0, format='HypVar%d'):
		self.document = document
		self.varcount = start_at
		self.format = format
	
	def new_var(self):
		rv = self.format % self.varcount
		self.varcount += 1
		return rv

	def generate_hypotheses(self, atoms):
		'''
		Riformula la conoscenza espressa negli atomi passati come 
		parametro sotto forma di un insieme di denials.
		'''
		
		negate_op = {'<': '>=', '<=': '>', '=': '~=', '~=': '=', '>=': '<',
				'>': '<='}
		
		aux_atoms = []
		vars = {}
		hypotheses = []
		
		for atom in atoms:
			if isinstance(atom, AuxAtom) and atom.op in negate_op:
				neg = atom.copy()
				neg.op = negate_op[atom.op]
				aux_atoms.append(neg)
			else:
				for param, value in atom.parameters.iteritems():
					if is_ground(value) and param != '$id':
						premise = core(atom)
						nv = self.new_var()
						premise.parameters[param] = nv
						comparison = AuxAtom('~=', nv, value)
						hypotheses.append([premise, comparison])
					else:
						if value not in vars:
							vars[value] = (core(atom), param)
		
		for atom in aux_atoms:
			hyp = []
			for p in atom.parameters:
				if is_var(p):
					definition, position = vars[p]
					premise = definition.copy()
					premise.parameters[position] = p
					hyp.append(premise)
			hyp.append(atom)
			hypotheses.append(hyp)
		
		for denial in hypotheses:
			print '<-', ', '.join(map(str, denial))
		
		return hypotheses


if __name__ == '__main__':
	
	from testhelper import *
	
	n = sdd_azienda.create_atom
	
	descr = [
		n('azienda', {'$id': '?A'}), 
		n('sede', {'$id': '?S', '$parent': '?A', 'citta': '"Milano"'}),
		n('reparto', {'$id': '?D', '$parent': '?S', 'nome': '"R&D"'})
	]
	
	for i in descr: print i
	
	hyp = HypGenerator(sdd_azienda).generate_hypotheses(descr)
	
