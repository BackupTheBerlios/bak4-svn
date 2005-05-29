#!/usr/bin/env python2.4
# encoding: latin-1

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
				# attenzione agli schemi con riferimenti circolari!
				if new_edge[0] == new_edge[-1]:
					raise RecursiveSchemaException, new_edge
				if new_edge not in edges and new_edge not in expansion:
					expansion.append(new_edge)
	if len(expansion) == 0:
		return edges
	else:
		return transitive_expansion(edges + expansion)


def generate_graph(edges, filename, dir='./'):
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
		self.elements = document.elements
		self.edges = transitive_expansion(document.edges)
		if generate_graphs:
			generate_graph(document.edges, 'edges.dot')
			generate_graph(self.edges, 'expansion.dot')
	
	def resolve_bridge(self, node_from, node_to):
		return [edge for edge in self.edges
				if edge[0] == node_from and edge[-1] == node_to]
	
	def resolve_up(self, node_from):
		return [edge[0] for edge in self.edges
				if len(edge) == 2 and edge[1] == node_from]
	
	def resolve_star(self, node_from):
		return [edge[1] for edge in self.edges
				if len(edge) == 2 and edge[0] == node_from]
	
	def resolve_bridge_attrib(self, node_from, attrib_to):
		goals = [element for element in self.elements
				if attrib_to in self.elements[element]]		
		rv = []
		for target in goals:
			rv.extend(self.resolve_bridge(node_from, target))
		return rv
