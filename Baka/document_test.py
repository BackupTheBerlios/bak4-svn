#!/usr/bin/env python2.4
# encoding: latin-1

# copyright (c) domenico carbotta <domenico.carbotta@gmail.com>, 2005
# code released under the gnu gpl, see license.txt

'''
document_test.py

Test delle funzionalità degli oggetti Document.
'''

from document import Document

def test_corsi():

	elements = {
		'sede': ['nome'],
		'corso': [],
		'docente': ['assunzione', 'contratto'],
		'titolo': []
	}
	edges = [('sede', 'corso'), ('corso', 'titolo'), ('corso', 'docente')]
	pcdata = ['titolo', 'docente']

	doc = Document(elements, edges, pcdata)
	
	params = {'id': 'Id', 'pos': 'Pos'}
	x = None
	for element in elements:
		atom, x = doc.create_atom(element, params, start_at=x)
		print atom


def test_html():

	elements = {
		'html': ['lang'],
		'head': [],
		'title': [],
		'link': ['rel', 'href'],
		'body': [],
		'ul': [],
		'ol': ['style'],
		'li': []
	}
	edges = [('html', 'head'), ('html', 'body'), ('head', 'title'),
		('head', 'meta'), ('body', 'ul'), ('body', 'ol'), ('ul', 'li'),
		('ol', 'li')]
	pcdata = ['title', 'li']
	
	doc = Document(elements, edges, pcdata)
	
	for element in doc.elements:
		print doc.create_empty_atom(element)
