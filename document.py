#!/usr/bin/env python2.4

# copyright (c) domenico carbotta <domenico.carbotta@gmail.com>, 2005
# code released under the gnu gpl, see license.txt

'''
docinfo.py

Classi che effettuano per il mapping gerarchico -> relazionale dello schema
del documento XML.
'''

class TranslationError (Exception):
	'''
	Errore di traduzione. Tutte le eccezioni sollevate da questo modulo sono
	derivate da questa classe.
	'''
	pass

class NoSuchElement (TranslationError):
	pass

class NoSuchAttribute (TranslationError):
	pass

def quote(dictionary):
	'''
	Restituisce una copia del dizionario passato come parametro nella quale i
	valori che rappresentano variabili Prolog (ossia tutti quelli che iniziano
	con la maiuscola...) sono virgolettati, come richiesto dai programmi a
	valle. 
	'''
	d = dictionary.copy()
	for k, i in d.iteritems():
		if i[0].isupper():
			d[k] = "'" + i + "'"
	return d

class Document (object):
	'''
	Questa classe contiene le informazioni sulla struttura del documento ed
	effettua il mapping gerarchico -> relazionale degli elementi.
	'''

	def __init__(self, all, forward_mapping, attributes, pcdata):
		self.all = all
		self.forward_mapping = forward_mapping
		self.backwards_mapping = {}
		for element, children in self.forward_mapping.iteritems():
			for child in children:
				if child not in self.backwards_mapping:
					self.backwards_mapping[child] = [element]
				else:
					self.backwards_mapping[child].append(element)
		print self.backwards_mapping
		self.attributes = attributes
		self.pcdata = pcdata
	
	def check_element(self, element):
		'''
		Solleva un'eccezione di tipo NoSuchElement se l'elemento passato
		come parametro non è presente nella descrizione della struttura.
		'''
		if element not in self.all:
			raise NoSuchElement(element)
	
	def check_attribute(self, element, attribute):
		'''
		Solleva un'eccezione di tipo NoSuchException se l'elemento specificato
		come primo parametro non possiede l'attributo indicato come secondo
		parametro.
		'''
		if attribute not in self.attributes[element]:
			raise NoSuchAttribute(element + '.' + attribute)
	
	def has_parent(self, element):
		'''
		Restituisce un valore booleano che indica se il nodo selezionato ha un
		padre nella gerarchia del documento.
		'''
		self.check_element(element)
		return element in self.backwards_mapping
		
	
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
		if element in self.attributes:
			m = map(lambda x: '%(' + x + ')s', self.attributes[element])
			rv = rv + ', ' + ', '.join(m)
		if element in self.pcdata:
			rv = rv + ', %(_text)s'
		rv = element + '(' + rv + ')'
		return rv
	
	def create_atom(self, element, values, start_at=None, format='Foo%d'):
		'''
		Inserisce nel dizionario elementi senza nome corrispondenti a campi e
		attributi non presenti come chiavi nel dizionario.
		'''
		self.check_element(element)
		n = 1
		if start_at is not None:
			n = start_at
		values = values.copy()		# non sporchiamo il dizionario originale!
		if 'pos' not in values:
			values['pos'] = format % n
			n += 1
		if self.has_parent(element):
			if 'idpadre' not in values:
				values['idpadre'] = format % n
				n += 1
		if element in self.attributes:
			for attrib in self.attributes[element]:
				if attrib not in values or values[attrib] == '_':
					values[attrib] = format % n
					n += 1
		if element in self.pcdata:
			if '_text' not in values:
				values['_text'] = format % n
				n += 1
		return self.create_empty_atom(element) % quote(values), n
