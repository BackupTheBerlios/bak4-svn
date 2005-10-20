#!/usr/bin/env python2.4
# encoding: latin-1

# copyright (c) domenico carbotta <domenico.carbotta@gmail.com>, 2005
# code released under the gnu gpl, see license.txt


__all__ = ['MappingError', 'DocType', 'DTCollection', 'DefaultDocument']


from baka.classes.resolver import *
from baka.classes.atom import *
from baka.classes.ppstate import Document
from baka.util.symbol import *


DefaultDocument = '!default'


class MappingError (Exception):
    pass


class DocType (object):
    '''
    Questa classe contiene le informazioni sulla struttura del documento ed
    effettua il mapping gerarchico -> relazionale degli elementi.
    '''
    
    def __init__(self, id, elements, root_el, edges, pcdata):
        self.id = id
        self.elements = elements
        self.root_el = root_el
        self.edges = edges + [(Document, id)]
        if True: # 20050906
            for element, attributes in elements.iteritems():
                attributes[0:0] = ['$id', '$pos', '$parent']
                if element in pcdata:
                    attributes.append('$text')
        else:
            for element in pcdata:
                self.elements[element].append('$text')
        self.resolver = Resolver(self)
    
    def __contains__(self, other):
        return other in self.elements
    
    def check_element(self, element, throw=True):
        '''
        Solleva un'eccezione di tipo NoSuchElement se l'elemento passato
        come parametro non è presente nella descrizione della struttura.
        '''
        if element not in self:
            if throw:
                msg = 'Element %s does not exist in doctype %s.'
                raise MappingError(msg % (element, self.id))
            else:
                return False
        return True
    
    def check_attribute(self, element, attribute, throw=True):
        '''
        Solleva un'eccezione di tipo NoSuchException se l'elemento specificato
        come primo parametro non possiede l'attributo indicato come secondo
        parametro.
        '''
        if attribute not in self.elements[element]:
            if throw:
                msg = 'Attribute %s of element %s does not exist in doctype %s.'
                raise MappingError(msg % (attribute, element, self.id))
            else:
                return False
        return True
    
    def has_parent(self, element):
        '''
        Restituisce un valore booleano che indica se il nodo selezionato ha un
        padre nella gerarchia del documento.
        '''
        self.check_element(element)
        return len(filter(lambda x: x[1] == element, self.edges)) != 0
    
    def create_atom(self, element, parameters=None):
        '''
        Crea un atomo Datalog -- sotto forma di un oggetto di tipo Atom -- che
        si riferisce all'elemento indicato.
        '''
        self.check_element(element)
        return Atom(self, element, parameters)


class DTCollection (object):
    
    def __init__(self, documents, doctypes):
        self.documents = documents
        self.doctypes = doctypes
    
    # deprecated!
    def get(self, doc_name):
        return self.get_by_document(doc_name)
    
    def get_by_document(self, doc_name):
        return self.doctypes[self.documents[doc_name]]
    
    def get_by_dtid(self, dtid):
        return self.doctypes[dtid]
    