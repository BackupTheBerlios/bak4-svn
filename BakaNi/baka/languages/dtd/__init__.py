#!/usr/bin/env python2.4
# encoding: utf-8

# copyright (c) domenico carbotta <domenico.carbotta@gmail.com>, 2005
# code released under the gnu gpl, see license.txt


__all__ = ['process_dtd']


from dtdparser import DTDParser
from dtdscanner import DTDScanner
from ima.languages.toolchain import processor


process_dtd = processor(DTDScanner, DTDParser)


dtd_collection = '''

<!-- !DOCTYPE prova ("file.xml") -->

<!ELEMENT prova (ciao)*>
<!ATTLIST prova pluto #CDATA REQUIRED>
<!ELEMENT ciao (#PCDATA)>
'''

print process_dtd(dtd_collection)