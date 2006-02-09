#!/usr/bin/env python2.4
# encoding: utf-8

# copyright (c) domenico carbotta <domenico.carbotta@gmail.com>, 2005
# code released under the gnu gpl, see license.txt


__all__ = ['DatalogParser']


from ima.languages.toolchain import *
from ima.util.vargenerator import *
from ima.classes.atom import *
from ima.classes.equivalence_classes import *


def is_number(x):
    # str.isdigit() doesn't work for floating point numbers...
    try:
        float(x)
        return True
    except ValueError:
        return False


class DatalogParser (Parser):
    
    def __init__(self, start='simp_output'):
        Parser.__init__(self, start)
        self.equivalences = []
        self.new_lit_var = VarGenerator.factory('Lit_%d', auto_prefix=False)
        self.new_std_var = VarGenerator.factory('Std_%d', auto_prefix=False)
        
    def standardize(self, string):
        if string.startswith('s_') or is_number(x):
            nv = self.new_lit_var()
            self.equivalences.append(AuxAtom('=', (nv, string)))
            return nv
        elif (string.startswith('Auto_') or string.startswith('Var_') or
                string.startswith('?') or string.startswith('x_')):
            nv = self.new_std_var()
            self.equivalences.append(AuxAtom('=', (nv, string)))
            return nv
        else:
            raise ValueError(string)
    
    standardize = lambda s, x: x
    def p_simp_output(self, args):
        '''
            simp_output ::= OPENBRACKET denial_list CLOSEBRACKET
        '''
        return [args[1]]
    
    def p_denial_list_1(self, args):
        '''
            denial_list ::= OPENBRACKET predicates CLOSEBRACKET
                    COMMA denial_list
        '''
        print args[1] #-#
        rv = args[1] + self.equivalences
        self.equivalences = []
        return rv + args[4]
    
    def p_denial_list_2(self, args):
        '''
            denial_list ::= OPENBRACKET predicates CLOSEBRACKET
        '''
        rv = args[1] + self.equivalences
        self.equivalences = []
        return rv
    
    def p_predicates_1(self, args):
        '''
            predicates ::=
        '''
        return []
    
    def p_predicates_2(self, args):
        '''
            predicates ::= predicates_nonempty
        '''
        return args[0]
    
    def p_predicates_nonempty_1(self, args):
        '''
            predicates_nonempty ::= predicate COMMA predicates_nonempty
        '''
        return [args[0]] + args[2]
    
    def p_predicates_nonempty_2(self, args):
        '''
            predicates_nonempty ::= predicate
        '''
        return args
    
    def p_predicate_1(self, args):
        '''
            predicate ::= STRING INFIX_OP STRING
        '''
        return AuxAtom(args[1].value, (args[0].value, args[2].value))
    
    def p_predicate_2(self, args):
        '''
            predicate ::= STRING OPENPAREN stringlist CLOSEPAREN
        '''
        pred_name = args[0].value
        if '@' not in pred_name:
            rv = AuxAtom(pred_name, args[2])
            print rv #-#
            return rv
        else:
            pred_name, dtid = pred_name.split('@')
            doctype = DatalogParser.dtcollection.get_by_dtid(dtid)
            
            # build arguments dictionary by combining element attributes
            # and predicate arguments.
            parameters = dict(zip(doctype.elements[pred_name], args[2]))
            print parameters #-#
            rv = Atom(doctype, pred_name, parameters)
            print rv #-#
            return rv
    
    def p_stringlist(self, args):
        '''
            stringlist ::=
        '''
        return []
    
    def p_stringlist_2(self, args):
        '''
            stringlist ::= stringlist_nonempty
        '''
        return args[0]
    
    def p_stringlist_nonempty(self, args):
        '''
            stringlist_nonempty ::= STRING COMMA stringlist_nonempty
            stringlist_nonempty ::= STRING
        '''
        if len(args) == 1:
            return [self.standardize(args[0].value)]
        else:
            return [self.standardize(args[0].value)] + args[2]
