#!/usr/bin/env python2.4
# encoding: latin-1

# copyright (c) domenico carbotta <domenico.carbotta@gmail.com>, 2005
# code released under the gnu gpl, see license.txt


__all__ = ['XPLParser']


from baka.languages.toolchain import *
from baka.languages.xpathlog.xplscanner import *
from baka.util.vargenerator import *
from baka.classes.atom import AuxAtom
from baka.classes.step import *
from baka.classes.doctype import DefaultDocument


def join_steps(step, step_list):
    if len(step_list) > 0:
        step_list[0].start = step.id
    return [step] + step_list


class XPLParser (Parser):
    
    def __init__(self, start='denial', var_generator=None):
        Parser.__init__(self, start)
        self.comparisons = []
        self.filters = []
        if var_generator is None:
            self.create_var = VarGenerator.create_var
        else:
            self.create_var = var_generator.create_var
        self.documents = {DefaultDocument: self.create_var('B_Doc')}
    
    def p_denial(self, args):
        '''
                denial ::= expressions
        '''
        doc_atoms = []
        for docname, docid in self.documents.iteritems():
            doc_atoms.append(AuxAtom('!document', (docid, docname)))
        rv = sort_steps(doc_atoms + args[0] + self.filters + self.comparisons)
        self.debug(rv)
        return rv
    
    def p_expressions_1(self, args):
        '''
                expressions ::= expression COMMA expressions
                rel_expressions ::= rel_expression COMMA rel_expressions
        '''
        self.debug(args[0] + args[2])
        return args[0] + args[2]
    
    def p_expressions_2(self, args):
        '''
                expressions ::= expression
                rel_expressions ::= rel_expression
        '''
        self.debug(args[0])
        return args[0]
    
    def p_expression_1(self, args):
        '''
                expression ::= path
                expression ::= comparison
                
                rel_expression ::= expression
                rel_expression ::= rel_path
                rel_expression ::= rel_comparison
        '''
        self.debug(args[0])
        return args[0]
    
    def p_comparison(self, args):
        '''
                comparison ::= comparable COMPARE comparable
                rel_comparison ::= rel_comparable COMPARE rel_comparable
        '''
        self.comparisons.append(
                        AuxAtom(args[1].value, (args[0][0], args[2][0])))
        return args[0][1] + args[2][1]
    
    def p_comparable_1(self, args):
        '''
                comparable ::= path
                rel_comparable ::= rel_path
        '''
        self.debug(args[0][-1].id)
        return args[0][-1].id, args[0]
    
    def p_comparable_2(self, args):
        '''
                comparable ::= VAR
                comparable ::= STRING
                comparable ::= NUMBER
        '''
        self.debug(args[0].value)
        return args[0].value, []
    
    def p_rel_comparable_1(self, args):
        '''
                rel_comparable ::= comparable
        '''
        self.debug(args[0])
        return args[0]
    
    def p_path_1(self, args):
        '''
                path ::= document path_c
        '''
        args[1][0].start = args[0]
        self.debug(args[1])
        return args[1]
    
    
    def p_path_2(self, args):
        '''
                path ::= VAR path_c
        '''
        args[1][0].start = args[0].value
        self.debug(args[1])
        return args[1]
    
    def p_path_3(self, args):
        '''
                path ::= path_c
        '''
        args[0][0].start = self.documents[DefaultDocument]
        self.debug(args[0])
        return args[0]
    
    def p_rel_path_1(self, args):
        '''
                rel_path ::= path
        '''
        self.debug(args[0])
        return args[0]
    
    def p_rel_path_2(self, args):
        '''
                rel_path ::= rel_path_c
        '''
        if args[0][0].start is None:
            args[0][0].start = FilterRoot
        self.debug(args[0])
        return args[0]
    
    def p_path_c_1(self, args):
        '''
                path_c ::= step path_c
                rel_path_c ::= rel_step path_c
        '''
        self.debug(join_steps(args[0], args[1]))
        return join_steps(args[0], args[1])
    
    def p_path_c_2(self, args):
        '''
                path_c ::= step
                path_c ::= final_step
                rel_path_c ::= rel_step
                rel_path_c ::= rel_final_step
        '''
        self.debug(args)
        return args
    
    def p_step_1(self, args):
        '''
                step ::= SLASH ELEMENT spec
        '''
        self.debug(LinearStep(Undefined, args[1].value, args[2]))
        return LinearStep(Undefined, args[1].value, args[2])
    
    def p_step_2(self, args):
        '''
                step ::= DOUBLESLASH ELEMENT spec
        '''
        self.debug(BridgeStep(Undefined, args[1].value, args[2]))
        return BridgeStep(Undefined, args[1].value, args[2])
    
    def p_step_3(self, args):
        '''
                step ::= SLASH DOUBLEDOT spec
        '''
        self.debug(UpStep(Undefined, args[2]))
        return UpStep(Undefined, args[2])
    
    def p_step_4(self, args):
        '''
                step ::= SLASH STAR spec
        '''
        self.debug(StarStep(Undefined, args[2]))
        return StarStep(Undefined, args[2])
    
    def p_final_step_1(self, args):
        '''
                final_step ::= SLASH ATTRIBUTE bind
        '''
        self.debug(AttribStep(Undefined, args[1].value, args[2]))
        return AttribStep(Undefined, args[1].value, args[2])
    
    def p_final_step_2(self, args):
        '''
                final_step ::= DOUBLESLASH ATTRIBUTE bind
        '''
        self.debug(BridgeAttribStep(Undefined, args[1].value, args[2]))
        return BridgeAttribStep(Undefined, args[1].value, args[2])
    
    
    def p_rel_step_1(self, args):
        '''
                rel_step ::= ELEMENT spec
        '''
        self.debug(LinearStep(FilterRoot, args[0].value, args[1]))
        return LinearStep(FilterRoot, args[0].value, args[1])
    
    def p_rel_step_2(self, args):
        '''
                rel_step ::= DOUBLEDOT spec
        '''
        self.debug(UpStep(FilterRoot, args[1]))
        return UpStep(FilterRoot, args[1])
    
    def p_rel_step_3(self, args):
        '''
                rel_step ::= STAR spec
        '''
        self.debug(UpStep(FilterRoot, args[1]))
        return UpStep(FilterRoot, args[1])
    
    def p_rel_step_4(self, args):
        '''
                rel_final_step ::= ATTRIBUTE bind
        '''
        self.debug(AttribStep(FilterRoot, args[0].value, args[1]))
        return AttribStep(FilterRoot, args[0].value, args[1])
    
    def p_document(self, args):
        '''
                document ::= KW_DOCUMENT OPENPAREN STRING CLOSEPAREN
        '''
        doc = args[2].value
        if doc not in self.documents:
            self.documents[doc] = self.create_var('B_Doc')
        self.debug(self.documents[doc])
        return self.documents[doc]
    
    def p_spec_1(self, args):
        '''
                spec ::= OPENBRACKET rel_expressions CLOSEBRACKET bind
        '''
        self.debug(args[1])
        for step in args[1]:
            if step.start is FilterRoot:
                step.start = args[3]
        self.filters += args[1]
        self.debug(args[3])
        return args[3]
    
    def p_spec_2(self, args):
        '''
                spec ::= bind
        '''
        self.debug(args[0])
        return args[0]
    
    def p_bind(self, args):
        '''
                bind ::= ARROW VAR
                bind ::=
        '''
        if len(args) == 0:
            rv = self.create_var('B_Step')
            self.debug(rv)
            return rv
        else:
            self.debug(args[1].value)
            return args[1].value


if __name__ == '__main__':
    
    from timeit import Timer
    
    proc = processor(XPLScanner, XPLParser)
    def do_it():
        proc(string='''//dipendente[@nome->$N, pos()->$P,
                        ../*[@nome > $N, pos() < $P]->$Z],
                        $Z/@grado ~= "dirigente",
                        !document("pippo.xml")/ciao->$H > 3''', debug=True)
    
    ## t = Timer('do_it()', 'from __main__ import do_it')
    ## rv = t.repeat(200, 1)
    ## print sum(rv) / len(rv)
    
    do_it()
