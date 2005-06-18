#!/usr/bin/env python2.4
# encoding: latin-1

# copyright (c) domenico carbotta <domenico.carbotta@gmail.com>, 2005
# code released under the gnu gpl, see license.txt

'''
testhelper.py

Contiene oggetti utili in fase di testing.
'''

import sddparser, sddscanner
import xplparser, xplscanner
import document
import atom
from xml.dom import minidom


def parse(scanner, parser, what):
	return parser.parse(scanner.tokenize(what))

sdd_scanner = sddscanner.SDDScanner()
sdd_parser = sddparser.SDDParser()

xpl_scanner = xplscanner.XPathLogScanner()
xpl_parser = xplparser.XPathLogParser()

def get_document(what):
	return parse(sdd_scanner, sdd_parser, what)

def get_query(what):
	return parse(xpl_scanner, xpl_parser, what)

sdd_azienda = get_document(open('integration test/azienda.sdd').read())

update = '''
<dipendente grado="impiegato" nome="?nome" cognome="?cognome">
	<retribuzione>
		<stipendio mensilita="13" importo_mensile="?stipendio" />	
		<benefit>auto aziendale</benefit>
	</retribuzione>
</dipendente>
'''
update_dom = minidom.parseString(update).documentElement
