#!/usr/bin/env python2.4
# encoding: utf-8

# copyright (c) domenico carbotta <domenico.carbotta@gmail.com>, 2005
# code released under the gnu gpl, see license.txt


__all__ = ['DatalogScanner']


from baka.languages.toolchain import *


class DatalogScanner (Scanner):
    
    def t_pseudoconst(self, s):
        r' [a-zA-Z0-9_?.]+ '
        self.push('STRING', s)
    
    def t_quoted(self, s):
        ''' '[^"']*' '''
        self.push('STRING', s[1:-1])
    
    def t_infix_op(self, s):
        r' ( < | = | ~= ) '
        self.push('INFIX_OP', s)
    
    def t_comma(self, s):
        r' , '
        self.push('COMMA', s)
    
    def t_parentheses(self, s):
        r' ( \[ | \] | \( | \) | { | } )'
        if s == '[':
            optype = 'OPENBRACKET'
        if s == ']':
            optype = 'CLOSEBRACKET'
        elif s == '(':
            optype = 'OPENPAREN'
        elif s == ')':
            optype = 'CLOSEPAREN'
        elif s == '{':
            optype = 'OPENBRACE'
        elif s == '}':
            optype = 'CLOSEBRACE'
        self.push(optype, s)
    
    def t_not(self, s):
        r' ~(?!=) '
        self.push('NOT', s)
