#!/usr/bin/env python2.4
# encoding: utf-8

# copyright (c) domenico carbotta <domenico.carbotta@gmail.com>, 2005
# code released under the gnu gpl, see license.txt


__all__ = ['DTDParser']


from ima.languages.toolchain import *
from ima.classes.doctype import *
from ima.classes.resolver import Resolver


class DTDParser (Parser):
    
    def __init__(self, factory=None, start='minidtd'):
        Parser.__init__(self, start)
        
        self.documents = {}
        self.doctypes = {}
        
        self.first_el = None
        self.sdd_elements = {}
        self.sdd_edges = []
        self.sdd_pcdata_elements = []
    
    def p_minidtd(self, args):
        '''
            minidtd ::= document_defs
        '''
        return DTCollection(self.documents, self.doctypes)
    
    def p_document_defs(self, args):
        '''
            document_defs ::= document_defs document_def
            document_defs ::=
        '''
        pass
    
    def p_document_def(self, args):
        '''
            document_def ::=
                    OPENCOMMENT
                    KW_DOCTYPE ID OPENPAREN files CLOSEPAREN
                    CLOSECOMMENT
                    instructions
        '''
        
        id = args[2].value
        self.root_el = id
        
        if id not in self.sdd_elements:
            self.sdd_elements[id] = []
        
        for fn in args[4]:
            if len(fn) == 0:
                errmsg = 'Trying to define an unnamed document.'
                raise DTDParsingException, errmsg
            if fn in self.documents:
                errmsg = 'Document %s is already attached to a DocType.'
                raise DTDParsingException, errmsg % (fn)
            
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
    
    def p_instructions(self, args):
        '''
            instructions ::= instructions instruction
            instructions ::= instruction
        '''
        pass
    
    def p_instruction(self, args):
        '''
            instruction ::= element
            instruction ::= attlist
        '''
        pass
    
    def p_element(self, args):
        '''
            element ::=
                    OPENTRI KW_ELEMENT ID
                    contents_or_empty
                    CLOSETRI
        '''
        id = args[2].value
        
        contents = args[3]
        
        if type(contents) is list:
            for child in args[3]:
                self.sdd_edges.append((id, child))
        elif contents == 'PCDATA':
            self.sdd_pcdata_elements.append(id)
    
    def p_attlist(self, args):
        '''
            attlist ::= OPENTRI KW_ATTLIST ID attributes CLOSETRI
        '''
        id = args[2].value
        self.sdd_elements[id] = args[3]
    
    def p_contents_or_empty_1(self, args):
        '''
            contents_or_empty ::= OPENPAREN contents CLOSEPAREN STAR
        '''
        return args[1]
    
    def p_contents_or_empty_3(self, args):
        '''
            contents_or_empty ::= OPENPAREN PCDATA CLOSEPAREN
        '''
        return 'PCDATA'
    
    def p_contents_or_empty_2(self, args):
        '''
            contents_or_empty ::= EMPTY
        '''
        return None
    
    def p_contents(self, args):
        '''
            contents ::= ID BAR contents
            contents ::= ID
        '''
        if len(args) == 1:
            return [args[0].value]
        else:
            return [args[0].value] + args[2]
    
    def p_attributes(self, args):
        '''
            attributes ::= ID CDATA REQUIRED attributes
            attributes ::=
        '''
        if len(args) == 0:
            return []
        else:
            return [args[0].value] + args[3]
