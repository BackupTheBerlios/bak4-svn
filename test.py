#!/usr/bin/env python2.4

# copyright (c) domenico carbotta <domenico.carbotta@gmail.com>, 2005
# code released under the gnu gpl, see license.txt

import document

all = ['sede', 'corso', 'titolo', 'docente']

fw = {							  
	'sede': ['corso'],
	'corso': ['titolo', 'docente']
}

attr = {
	'sede': ['nome'],
	'docente': ['assunzione', 'contratto']
}

pcdata = ['titolo', 'docente']

document = document.Document(all, fw, attr, pcdata)

so_what = {'id': 'a'}
m = {}
x = None

for element in all:
	m[element], x = document.create_atom(element, so_what, start_at=x)

for element in m:
	print element, '\n\t', m[element], '\n'
