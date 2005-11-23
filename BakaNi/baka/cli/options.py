#!/usr/bin/env python2.4
# encoding: utf-8

# copyright (c) domenico carbotta <domenico.carbotta@gmail.com>, 2005
# code released under the gnu gpl, see license.txt


from optparse import OptionParser


def get_options():
    
    option_parser = OptionParser()
    
    option_parser.add_option("-d", "--denial", dest="denial_filename",
                    help="legge il denial contenuto in DENIAL_FILE",
                    metavar="DENIAL_FILE")
    
    option_parser.add_option("-s", "--sdd", dest="sdd_filename",
                    help="legge la descrizione dei documenti da SDD_FILE",
                    metavar="SDD_FILE")
    
    option_parser.add_option("-l", "--location", dest="loc_filename",
                    help="legge la descrizione del punto di inserimento da LOC_FILE",
                    metavar="LOC_FILE")
    
    option_parser.add_option("-x", "--xml", dest="xml_filename",
                    help="legge il frammento da XML_FILE",
                    metavar="XML_FILE")
    
    option_parser.add_option("-q", "--quiet",
                    action="store_false", dest="verbose", default=True,
                    help="fa meno casino possibile")
    
    return option_parser.parse_args()[0]
