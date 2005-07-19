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


def generate_hypotheses(document, atoms, start_at=0, format='HypVar%d'):
	
	varcount = start_at
	rv = []
	
	for atom in atoms:
		if isinstance(atom, Atom):
			atom_id = atom.parameters['$id']
			for param, value in atom.parameters.iteritems():
				if param == '$id':
					continue
				else:
					new_var = format % varcount
					varcount += 1
					hyp_a = document.create_atom(atom.element,
						{'$id': atom_id, param: new_var})
					hyp_b = MathAtom('~=', new_var, value)
					rv.append([hyp_a, hyp_b])
		elif isinstance(atom, MathAtom):
			negate_op = {'<': '>=', '<=': '>', '=': '~=', '~=': '=', '>=': '<',
				'>': '<='}
			if atom.op in negate_op:
				rv.append([MathAtom(negate_op(atom.op), *atom.parameters)])
	
	return rv


if __name__ == '__main__':

	from testhelper import *
	
	n = sdd_azienda.create_atom
	
	descr = [
		n('azienda', {'$id': '?A'}), 
		n('sede', {'$id': '?S', '$parent': '?A', 'citta': '"Milano"'}),
		n('reparto', {'$id': '?D', '$parent': '?S', 'nome': '"R&D"'})
	]
	
	hyp = generate_hypotheses(sdd_azienda, descr)
	
	for denial in hyp:
		print '<-', ', '.join(map(str, denial))
