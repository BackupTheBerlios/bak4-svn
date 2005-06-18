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
	print_results(doc)	


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
	
	print_results(doc)	


def print_results(doc):
	params = {'$id': 'Id', '$pos': 'Pos'}
	x = 1
	for element in doc.elements:
		print doc.create_atom(element, params)


def main():
	test_corsi()
	print
	print '---'
	print
	test_html()


if __name__ == '__main__':
	main()
