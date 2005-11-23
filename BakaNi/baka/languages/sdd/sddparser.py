#!/usr/bin/env python2.4
# encoding: utf-8

# copyright (c) domenico carbotta <domenico.carbotta@gmail.com>, 2005
# code released under the gnu gpl, see license.txt


__all__ = ['SDDParser']


from baka.languages.toolchain import *
from baka.classes.doctype import *
from baka.classes.resolver import Resolver


class SDDParser (Parser):
    
    def __init__(self, factory=None, start='sdplus'):
        Parser.__init__(self, start)
        
        self.documents = {}
        self.doctypes = {}
        
        self.first_el = None
        self.sdd_elements = {}
        self.sdd_edges = []
        self.sdd_pcdata_elements = []
    
    def p_sdplus(self, args):
        '''
                sdplus ::= document_defs
        '''
        return DTCollection(self.documents, self.doctypes)
    
    def p_document_defs(self, args):
        '''
            document_defs ::= document_def document_defs
            document_defs ::=
        '''
        pass
    
    def p_document_def(self, args):
        '''
            document_def ::=
                KW_DOCTYPE ID OPENPAREN files CLOSEPAREN
                OPENBRACE elements CLOSEBRACE
        '''
        
        id = args[1].value
        
        for fn in args[3]:
            if len(fn) == 0:
                errmsg = 'Trying to define an unnamed document.'
                raise SDDParsingException, errmsg
            if fn in self.documents:
                errmsg = 'Document %s is already attached to a DocType.'
                raise SDDParsingException, errmsg % (fn)
            
            self.documents[fn] = id
        
        self.doctypes[id] = DocType(id, self.sdd_elements, self.root_el,
                        self.sdd_edges, self.sdd_pcdata_elements)
        
        self.root_el = None
        self.sdd_elements = {}
        self.sdd_edges = []
        self.sdd_pcdata_elements = []
    
    def p_files(self, args):
        '''
                files ::= STRING COMMA files
                files ::= STRING
        '''
        if args[0].value != '!default':
            x = '__'
        else:
            x = ''
        if len(args) == 3:
            return [x + args[0].value] + args[2]
        else:
            return [x + args[0].value]
    
    def check(self):
        elements = self.sdd_elements
        edges = self.sdd_edges
        pcdata_elements = self.sdd_pcdata_elements
        for el_a, el_b in edges:
            if el_b not in elements:
                errmsg = 'Element %s (referenced as child of element %s) '\
                                'does not exist.'
                raise SDDParsingException, errmsg % (el_b, el_a)
    
    def p_elements(self, args):
        '''
            elements ::= element SEMICOLON elements
            elements ::= element SEMICOLON
        '''
        pass
    
    def p_element(self, args):
        '''
            element ::= ID ARROW attribute_list contents
        '''
        id = args[0].value
        attributes = args[2]
        allows_pcdata, children = args[3]
        
        self.sdd_elements[id] = attributes
        if allows_pcdata:
            self.sdd_pcdata_elements.append(id)
        else:
            for child in children:
                self.sdd_edges.insert(0, (id, child))
        
        self.root_el = args[0].value
    
    def p_attribute_list(self, args):
        '''
            attribute_list ::= OPENPAREN idlist CLOSEPAREN
            attribute_list ::=
        '''
        if len(args) == 0:
            return []
        else:
            return args[1]
    
    def p_contents_1(self, args):
        '''
            contents ::= idlist
        '''
        return False, args[0]
    
    def p_contents_2(self, args):
        '''
            contents ::= KW_PCDATA
        '''
        return True, None
    
    def p_idlist(self, args):
        '''
            idlist ::= idlist_full
            idlist ::=
        '''
        if len(args) == 0:
            return []
        else:
            return args[0]
    
    def p_idlist_full(self, args):
        '''
            idlist_full ::= ID COMMA idlist_full
            idlist_full ::= ID
        '''
        if len(args) == 1:
            return [args[0].value]
        else:
            args[2].insert(0, args[0].value)
            return args[2]


if __name__ == '__main__':
    
    sdp = '''
    
    !doctype libro ("!default") {
            libro -> (isbn, titolo) autore;
            autore -> (nome);
    }
    
    !doctype collezione ("collezione.xml") {
            collezione -> (proprietario) libro;
            libro -> copia, titolo, autore;
            copia -> (num_inventario, isbn, stanza, scaffale);
            titolo -> (lingua) !PCDATA;
            autore -> (nome);
    }
    
    !doctype store ("amazon.xml", "barnesandnoble.xml") {
            store -> (nome, url, contatto) oggetto;
            oggetto -> (codice, prezzo) !PCDATA;
    }
    
    !doctype ordini ("ordini.xml") {
            ordini -> ordine;
            ordine -> (data, store) acquisto;
            acquisto -> (quantita, codice) !PCDATA;
    }
    
    '''
    
    from sddscanner import SDDScanner
    processor(SDDScanner, SDDParser)(string=sdp, debug=True)
