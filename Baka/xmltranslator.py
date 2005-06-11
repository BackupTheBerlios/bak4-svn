#!/usr/bin/env python2.4
# encoding: latin-1

# copyright (c) domenico carbotta <domenico.carbotta@gmail.com>, 2005
# code released under the gnu gpl, see license.txt

'''
xmltranslator.py
'''

from xml.dom import minidom
from document import *
from smallerthandom import *
from atom import *


class XMLTranslator (object):
	
	def __init__(self, document, start_at=0):
		self.document = document
		self.var_count = start_at
	
	def new_var(self, format='?p%d'):
		rv = format % self.var_count
		self.var_count += 1
		return rv
	
	def translate(self, xml_fragment, parent_type, parent_id):
		root_node = minidom.parseString(xml_fragment).documentElement
		check_fragment(root_node, self.document, parent_type)
		tree = build_abstract_tree(root_node)
		return self.create_atoms_from_tree(tree, parent_id, generate_pos=True)
	
	def create_atoms_from_tree(self, node, parent_id, generate_pos=False):
		rv = []
		attributes = node.attributes.copy()
		id = self.new_var()
		attributes['$id'] = id
		attributes['$parent'] = parent_id
		if generate_pos:
			attributes['$pos'] = self.new_var()
		rv.append(self.document.create_atom(node.name, attributes))
		for child in node.children:
			rv.extend(self.create_atoms_from_tree(child, id))
		return rv
	
	def create_append_hyp(self, atoms, parent_type, parent_id,
			human_readable=False):
		document = self.document
		no_such_atom = []
		no_successive_atoms = []
		no_child_atoms = []
		root_atom = atoms[0]
		for sibling_element in document.resolver.resolve_star(parent_type):
			no_successive_atoms.append([
					document.create_atom(sibling_element,
							{'$pos': 'P', '$parent': parent_id}),
					MathAtom('>=', 'P', root_atom.parameters['$pos'])])
		for atom in atoms:
			id = atom.parameters['$id']
			# XXX
			# human_readable genera ipotesi aggiuntive relative a
			# nodi dello stesso tipo.
			for element in document.elements:
				no_such_atom.append([document.create_atom(
						element, {'$id': id})])
			for child_element in document.resolver.resolve_star(atom.element):
				no_child_atoms.append([document.create_atom(
						child_element, {'$parent': id})])
		hyp = no_successive_atoms + no_child_atoms + no_such_atom
		rv = []
		n = 0
		for denial in hyp:
			dr = []
			for atom in denial:
				if isinstance(atom, Atom):
					if human_readable:
						atom_r = atom.render_unescaped()
						dr.append(atom_r)
					else:
						atom_r, n = atom.render(start_at=n)
						dr.append(atom_r)
				elif isinstance(atom, MathAtom):
					atom_r = atom.render()
					dr.append(atom_r)
			rv.append('[' + ', '.join(dr) + ']')
		return ',\n'.join(rv)


def test():
	import testhelper
	xt = XMLTranslator(testhelper.sdd_azienda)
	xa = xt.translate(testhelper.update, 'reparto', '?rep')
	xd = xt.create_append_hyp(xa, 'reparto', '?rep', human_readable=True)
	for i in xa:
		print i
	print '---'
	print xd


if __name__ == '__main__':
	test()
