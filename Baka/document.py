#!/usr/bin/env python2.4
# encoding: latin-1

# copyright (c) domenico carbotta <domenico.carbotta@gmail.com>, 2005
# code released under the gnu gpl, see license.txt

'''
document.py

Classi che effettuano il mapping gerarchico -> relazionale degli elementi che
costituiscono il documento XML e permettono la risoluzione dei cammini
complessi attraverso il modulo resolver.
'''

import resolver
from atom import Atom


class TranslationError (Exception):
	'''
	Errore di traduzione. Tutte le eccezioni sollevate da questo modulo sono
	derivate da questa classe.
	'''
	pass


class NoSuchElement (TranslationError):
	'''
	Errore di traduzione: si sta tentando di operare su un elemento
	inesistente.
	'''
	pass


class NoSuchAttribute (TranslationError):
	'''
	Errore di traduzione: si sta tentando di operare su un attributo
	inesistente.
	'''
	pass


class Document (object):
	'''
	Questa classe contiene le informazioni sulla struttura del documento ed
	effettua il mapping gerarchico -> relazionale degli elementi.
	'''

	def __init__(self, elements, edges, pcdata):
		self.elements = elements
		self.edges = edges
		self.pcdata = pcdata
		self.resolver = resolver.Resolver(self, generate_graphs=True)
	
	def check_element(self, element):
		'''
		Solleva un'eccezione di tipo NoSuchElement se l'elemento passato
		come parametro non è presente nella descrizione della struttura.
		'''
		if element not in self.elements:
			raise NoSuchElement(element)
	
	def check_attribute(self, element, attribute):
		'''
		Solleva un'eccezione di tipo NoSuchException se l'elemento specificato
		come primo parametro non possiede l'attributo indicato come secondo
		parametro.
		'''
		if attribute not in self.elements[element][0]:
			raise NoSuchAttribute(element + '.' + attribute)
	
	def has_parent(self, element):
		'''
		Restituisce un valore booleano che indica se il nodo selezionato ha un
		padre nella gerarchia del documento.
		'''
		self.check_element(element)
		return len(filter(lambda x: x[1] == element, self.edges)) != 0
	
	def create_atom(self, element, parameters=None):
		'''
		Crea un atomo Prolog -- sotto forma di un oggetto di tipo Atom -- che
		si riferisce all'elemento indicato.
		'''
		self.check_element(element)
		return Atom(self, element, parameters)


if __name__ == '__main__':
	
	import document_test
	
	## document_test.test_corsi()
	document_test.test_html()
