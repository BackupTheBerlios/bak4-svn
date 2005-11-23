#!/usr/bin/env python2.4
# encoding: utf-8

# copyright (c) domenico carbotta <domenico.carbotta@gmail.com>, 2005
# code released under the gnu gpl, see license.txt


__all__ = ['SDDScanner']


from baka.languages.toolchain import *


class SDDScanner (Scanner):
    
    def t_id(self, s):
        r' ([a-zA-Z]+\:)?[a-zA-Z][a-zA-Z0-9_]* '
        self.push('ID', s)
    
    def t_arrow(self, s):
        r' \-> '
        self.push('ARROW', s)
    
    def t_parentheses(self, s):
        r' ( \[ | \] | \( | \) | { | } ) '
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
    
    def t_semicolon(self, s):
        r' ; '
        self.push('SEMICOLON', s)
    
    def t_comma(self, s):
        r' , '
        self.push('COMMA', s)
    
    def t_keyword(self, s):
        r' \![a-zA-Z]+ '
        self.push('KW_' + s[1:].upper(), s)
    
    def t_string(self, s):
        r' " [^"]* " '
        self.push('STRING', s[1:-1])
