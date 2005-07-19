#!/usr/bin/env python2.4
# encoding: latin-1

# copyright (c) domenico carbotta <domenico.carbotta@gmail.com>, 2005
# code released under the gnu gpl, see license.txt

'''
smallerthandom.py
'''

from xml.dom import minidom


class InvalidFragmentException (Exception):
	'''
		Eccezione sollevata in caso di frammento non rispondente al tipo del
		documento.
	'''
	pass


class MixedElementException (InvalidFragmentException):
	'''
		Eccezione sollevata in caso di presenza di mixed elements.
	'''
	pass


class MyNode (object):
	
	def __init__(self, name, attributes, pos=None, children=None):
		self.name = name
		self.attributes = attributes
		if pos is not None:
			self.attributes['$pos'] = str(pos)
		if children is None:
			self.children = []
		else:
			self.children = children
	
	def render(self, indent=0):
		rv = '%s%s -> %r' % ('\t' * indent, self.name, self.attributes)
		for child in self.children:
			rv += '\n' + child.render(indent + 1)
		return rv
	
	def __str__(self):
		return self.render()


def check_fragment(node, document=None, parent=None):
	# controlliamo che node non sia un mixed element: se contiene pi�
	# di un nodo figlio, tutti i nodi di tipo Text devono essere composti
	# soltanto da whitespace
	if len(node.childNodes) > 1:
		for n in node.childNodes:
			if isinstance(n, minidom.Text):
				if len(n.data.strip()) != 0:
					raise MixedElementException, n.tagName

	if document is not None:
		# controlliamo se il tipo dell'elemento � valido
		if not document.check_element(node.tagName, throw=False):
			raise InvalidFragmentException, \
					'%s not found in document' % node.tagName
		
		# se � specificato il tipo dell'elemento padre, controlliamo
		# che la relazione padre-figlio sia valida
		if parent is not None:
			if (parent, node.tagName) not in document.edges:
				raise InvalidFragmentException, \
						'%s element doesn\'t allow %s as a child element.' % \
						(parent, node.tagName)
		
 	 	# controlliamo che siano specificati gli attributi richiesti,
 	 	# tutti gli attributi richiesti e soltanto gli attributi richiesti.
 	 	# dica "lo giuro".
		found = get_attributes(node)
		expected = document.elements[node.tagName]
		invalid = [x for x in found if x not in expected]
		missing = [x for x in expected if x not in found]
		if len(invalid) != 0:
			raise InvalidFragmentException, \
					'%s element doesn\'t allow attribute(s) %s.' % \
					(node.tagName, invalid)
		if len(missing) != 0:
			raise InvalidFragmentException, \
					'%s element lacks attribute(s) %s.' % \
					(node.tagName, missing)
		
	# e ora controlliamo i nodi figlio
	for idx, child in get_children(node):
		check_fragment(child, document, node.tagName)
	
	# tutto ok...
	return True


def get_attributes(node):
	rv = {}
	
	for i in range(node.attributes.length):
		a = node.attributes.item(i)
		rv[str(a.nodeName)] = str(a.nodeValue)
	
	if len(node.childNodes) == 1 \
			and isinstance(node.childNodes[0], minidom.Text):
		rv['$text'] = str(node.childNodes[0].data.strip())
	
	return rv


def get_children(node):
	idx = 0
	rv = []
	for child in node.childNodes:
		if not isinstance(child, minidom.Text):
			rv.append((idx, child))
			idx += 1
	return rv


def build_abstract_tree(node, pos=None):
	rv = MyNode(node.tagName, get_attributes(node), pos)
	for idx, child in get_children(node):
		rv.children.append(build_abstract_tree(child, idx))
	return rv
