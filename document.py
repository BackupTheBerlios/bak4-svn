#!/usr/bin/env python2.4

# copyright (c) domenico carbotta <domenico.carbotta@gmail.com>, 2005
# code released under the gnu gpl, see license.txt

'''
document.py

Classi che effettuano il mapping gerarchico -> relazionale degli elementi che
costituiscono il documento XML e permettono la risoluzione dei cammini
complessi attraverso il modulo resolver.
'''

import resolver


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


def quote_prolog_vars(dictionary):
	'''
	Restituisce una copia del dizionario passato come parametro nella quale i
	valori che rappresentano variabili Prolog (ossia tutti quelli che iniziano
	con la maiuscola...) sono virgolettati, come richiesto dai programmi a
	velementse. 
	'''
	d = dictionary.copy()    # non tocchiamo il dizionario originale!
	for k, i in d.iteritems():
		if i[0].isupper():
			d[k] = "'" + i + "'"
	return d


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
	
	def create_empty_atom(self, element):
		'''
		Crea il template di un atomo Prolog che riguarda l'elemento specificato.
		Il template generato è una stringa che può essere formattata con l'uso
		di un dizionario così strutturato:
		id -> identificativo del nodo
		pos -> posizione del nodo
		idpadre -> identificativo del nodo padre, se richiesto
		[nome attributo] -> [valore attributo]
		_text -> contenuto dell'elemento (se contiene #PCDATA)
		'''
		self.check_element(element)
		rv = '%(id)s, %(pos)s'
		if self.has_parent(element):
			rv = rv + ', %(idpadre)s'
		attributes = self.elements[element]
		if len(attributes) != 0:
			m = map(lambda x: '%(' + x + ')s', attributes)
			rv = rv + ', ' + ', '.join(m)
		if element in self.pcdata:
			rv = rv + ', %(_text)s'
		rv = element + '(' + rv + ')'
		return rv
	
	def create_atom(self, element, values, start_at=None, format='Var%02d'):
		'''
		Inserisce nel dizionario elementi senza nome corrispondenti a campi e
		attributi non presenti come chiavi nel dizionario.
		Restituisce l'atomo creato e il numero corrispondente alla prima 
		variabile accessoria libera (da passare eventualmente come parametro
		start_at alle chiamate successive).
		'''
		self.check_element(element)
		n = 1
		if start_at is not None:
			n = start_at
		values = values.copy()    # non tocchiamo il dizionario originale!
		if 'pos' not in values:
			values['pos'] = format % n
			n += 1
		if self.has_parent(element):
			if 'idpadre' not in values:
				values['idpadre'] = format % n
				n += 1
		for attrib in self.elements[element]:
			if attrib not in values or values[attrib] == '_':
				values[attrib] = format % n
				n += 1
		if element in self.pcdata:
			if '_text' not in values:
				values['_text'] = format % n
				n += 1
		return self.create_empty_atom(element) % quote_prolog_vars(values), n


if __name__ == '__main__':
	
	import document_test
	
	document_test.test_corsi()
	## document_test.test_html()
