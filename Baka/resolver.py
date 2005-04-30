#!/usr/bin/env python2.4

# copyright (c) domenico carbotta <domenico.carbotta@gmail.com>, 2005
# code released under the gnu gpl, see license.txt

'''
resolver.py

Classi e funzioni per la risoluzione dei passi complessi nelle espressioni
XPathLog.
'''

class RecursiveSchemaException (Exception):
	pass


def transitive_expansion(edges):
	expansion = []
	for edge_a in edges:
		for edge_b in edges:
			if edge_a[-1] == edge_b[0]:
				new_edge = edge_a[:-1] + edge_b
				# attenzione agli schemi con riferimenti circolari
				if new_edge[0] == new_edge[-1]:
					raise RecursiveSchemaException, new_edge
				if new_edge not in edges and new_edge not in expansion:
					expansion.append(new_edge)
	if len(expansion) == 0:
		return edges
	else:
		return transitive_expansion(edges + expansion)


def generate_graph(edges, filename, dir='~/Desktop/dots/'):
	from os.path import expanduser
	dotfile = open(expanduser(dir + filename), 'w')
	print >> dotfile, 'digraph {'
	print >> dotfile, '\t', 'node [fontname=helvetica]'
	print >> dotfile, '\t', 'edge [fontname=helvetica]'
	for edge in edges:
		style = ''
		if len(edge) > 2:
			style = '[style=dashed]'
		print >> dotfile, '\t', edge[0], '->', edge[-1], style
	print >> dotfile, '}'


class Resolver (object):
	
	def __init__(self, document, generate_graphs=False):
		# sanity check...
		self.elements = document.elements
		self.edges = transitive_expansion(document.edges)
		if generate_graphs:
			generate_graph(document.edges, 'edges.dot')
			generate_graph(self.edges, 'expansion.dot')
	
	def resolve_bridge(self, node_a, node_b):
		return filter(lambda x: x[0] == node_a and x[-1] == node_b,
			self.edges)
	
	def resolve_up(self, node_from):
		return map(lambda x: x[0],
			filter(lambda x: len(x) == 2 and x[1] == node_from, self.edges))
	
	def resolve_star(self, node_from):
		return map(lambda x: x[1],
			filter(lambda x: len(x) == 2 and x[0] == node_from, self.edges))
