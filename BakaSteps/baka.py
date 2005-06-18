#!/usr/bin/env python2.4
# encoding: latin-1

# copyright (c) domenico carbotta <domenico.carbotta@gmail.com>, 2005
# code released under the gnu gpl, see license.txt

'''
baka.py
'''

import sddscanner, sddparser
import xplscanner, xplparser
import preprocessor
import dlgenerator
import sys


def main(argv=None):

	# Leggo gli argomenti dalla riga di comando.
	
	if argv is None:
		argv = sys.argv	
	sdd_file = None
	xpl_file = None
	try:
		sdd_file = argv[1]
		xpl_file = argv[2]
	except IndexError:
		print >> sys.stderr, 'usage: %s SDDFILE XPLFILE' % \
				argv[0].split('/')[-1]
		raise SystemExit
	
	# Leggo il contenuto dei file, esco in caso di errore.
	
	try:
		document_descr = open(sdd_file).read()
	except IOError:
		print >> sys.stderr, 'unable to open', sdd_file
		raise SystemExit

	try:
		denial_text = open(xpl_file).read()
	except IOError:
		print >> sys.stderr, 'unable to open', xpl_file
		raise SystemExit
	
	# Creo un oggetto Document a partire dalla descrizione SDD del documento.
	
	sdd_scanner = sddscanner.SDDScanner()
	sdd_parser = sddparser.SDDParser()
	
	document = sdd_parser.parse(sdd_scanner.tokenize(document_descr))
	
	# Creo una rappresentazione semplificata dell'espressione XPathLog.
	
	xpl_scanner = xplscanner.XPathLogScanner()
	xpl_parser = xplparser.XPathLogParser()
	
	steps = xpl_parser.parse(xpl_scanner.tokenize(denial_text))
	
	pp = preprocessor.Preprocessor(document)
	dlgen = dlgenerator.DatalogGenerator(document)
	
	linearizations = pp.process(steps)
	for x in linearizations:
		print x.render()
	for x in dlgen.translate(linearizations):
		print '<~\t' + x

	
if __name__ == '__main__':
	
	main([None, 'integration test/azienda.sdd',
			'integration test/check_alfabetico.xpl'])
