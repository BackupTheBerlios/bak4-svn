#!/usr/bin/env python2.4
# encoding: latin-1

# copyright (c) domenico carbotta <domenico.carbotta@gmail.com>, 2005
# code released under the gnu gpl, see license.txt


__all__ = ['LocParser']


from baka.languages.toolchain import *
from baka.classes.atom import *
from baka.classes.step import *
from baka.util.vargenerator import VarGenerator


def join_steps(step, step_list):
    if len(step_list) > 0:
        step_list[0].start = step.id
    return [step] + step_list


class LocParser (Parser):
    
    def __init__(self, start='location', var_generator=None):
        Parser.__init__(self, start)
        self.aux_atoms = []
        if var_generator is None:
            var_generator = VarGenerator
        self.new_id = var_generator.factory('?i')
        self.new_var = var_generator.factory('L')
    
    def p_location(self, args):
        '''
                location ::= abbr_path
                location ::= abs_path
        '''
        class Struct:
            pass
        rv = Struct()
        rv.atoms = sort_steps(args[0] + self.aux_atoms)
        rv.ip = self.ip
        rv.doctype = self.doctype
        rv.ip_type = self.ip_type
        return rv
    
    def p_abs_path(self, args):
        '''
                abs_path ::= KW_DOCUMENT OPENPAREN STRING CLOSEPAREN path_cnt
        '''
        docname = self.new_id()
        self.doctype = args[2].value
        self.aux_atoms.append(AuxAtom('!document', (args[2].value, docname)))
        args[4][0].start = docname
        return args[4]
    
    def p_abbr_path_1(self, args):
        '''
                abbr_path ::= DOUBLESLASH ELEMENT filter path_cnt
        '''
        docname = self.new_id()
        self.doctype = '!default'
        self.aux_atoms.append(AuxAtom('!document', (docname, '!default')))
        return join_steps(BridgeStep(docname, args[1].value, args[2]), args[3])
    
    def p_abbr_path_2(self, args):
        '''
                abbr_path ::= DOUBLESLASH ELEMENT filter
        '''
        self.ip = args[2]
        self.ip_type = args[1].value
        docname = self.new_id()
        self.doctype = '!default'
        self.aux_atoms.append(AuxAtom('!document', (docname, '!default')))
        return [BridgeStep(docname, args[1].value, args[2])]
    
    def p_path_cnt_1(self, args):
        '''
                path_cnt ::= SLASH ELEMENT filter path_cnt
        '''
        return join_steps(LinearStep(None, args[1].value, args[2]), args[3])
    
    def p_path_cnt_2(self, args):
        '''
                path_cnt ::= DOUBLESLASH ELEMENT filter path_cnt
        '''
        return join_steps(BridgeStep(None, args[1].value, args[2]), args[3])
    
    def p_path_cnt_3(self, args):
        '''
                path_cnt ::= SLASH ELEMENT filter
        '''
        self.ip = args[2]
        self.ip_type = args[1].value
        return [LinearStep(None, args[1].value, args[2])]
    
    def p_path_cnt_4(self, args):
        '''
                path_cnt ::= DOUBLESLASH ELEMENT filter
        '''
        self.ip = args[2]
        self.ip_type = args[1].value
        return [BridgeStep(None, args[1].value, args[2])]
    
    def p_filter_1(self, args):
        '''
                filter ::= OPENBRACKET expressions CLOSEBRACKET
        '''
        rv = self.new_id()
        for atom in args[1]:
            atom.start = rv
        self.aux_atoms.extend(args[1])
        return rv
    
    def p_filter_2(self, args):
        '''
                filter ::=
        '''
        return self.new_id()
    
    def p_comparisons_1(self, args):
        '''
                expressions ::= expression COMMA expressions
        '''
        return args[0] + args[2]
    
    def p_comparisons_2(self, args):
        '''
                expressions ::= expression
        '''
        return args[0]
    
    def p_binding(self, args):
        '''
                expression ::= ATTRIBUTE ARROW VAR
        '''
        return [AttribStep(FilterRoot, args[0].value, args[2].value)]
    
    def p_comparison(self, args):
        '''
                expression ::= comparable COMPARE comparable
        '''
        return ([AuxAtom(args[1].value, (args[0][0], args[2][0]))] +
                        args[0][1] + args[2][1])
    
    def p_comparable_1(self, args):
        '''
                comparable ::= ATTRIBUTE
        '''
        nv = self.new_var()
        return nv, [AttribStep(FilterRoot, args[0].value, nv)]
    
    def p_comparable_2(self, args):
        '''
                comparable ::= NUMBER
                comparable ::= STRING
                comparable ::= VAR
        '''
        return args[0].value, []


if __name__ == '__main__':
    from baka.languages.xpathlog.scanner import XPLScanner
    
    p = processor(XPLScanner, LocParser)('!document("prova.xml")//pippo',
                    debug=True)
