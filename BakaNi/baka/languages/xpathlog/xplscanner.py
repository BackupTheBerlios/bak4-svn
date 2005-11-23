#!/usr/bin/env python
# encoding: utf-8

# copyright (c) domenico carbotta <domenico.carbotta@gmail.com>, 2005
# code released under the gnu gpl, see license.txt


__all__ = ['XPLScanner']


from baka.languages.toolchain import *


class XPLScanner (Scanner):
    '''
            Questa classe implementa uno scanner per una versione ridotta del
            linguaggio XPathLog utilizzando la libreria SPARK sviluppata da
            John Aycock della University of Calgary.
            
            Per ulteriori informazioni su SPARK:
                    http://pages.cpsc.ucalgary.ca/~aycock/spark/
    '''
    
    def t_A_call(self, s):
        r' (pos|text) \( \) '
        self.push('ATTRIBUTE', '$' + s[:-2])
    
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
    
    def t_compare(self, s):
        r' ( < (?! = ) | <= | = | ~= | >= | (?<! - ) > )'
        self.push('COMPARE', s)
    
    def t_comma(self, s):
        r' \, '
        self.push('COMMA', s)
    
    def t_number(self, s):
        r' ( \.\d+ | \d+(\.\d+)? ) '
        self.push('NUMBER', s)
    
    def t_string(self, s):
        ''' ( "[^"']*" ) '''
        self.push('STRING', 's_' + s[1:-1])
    
    def t_element(self, s):
        r' ([a-zA-Z]+\:)?[a-zA-Z][a-zA-Z0-9_]* '
        self.push('ELEMENT', s)
    
    def t_var(self, s):
        r' \$[a-zA-Z][a-zA-Z0-9_]* '
        self.push('VAR', 'Var_' + s[1:])
    
    def t_metaconst(self, s):
        r' \?[a-zA-Z][a-zA-Z0-9_]* '
        self.push('VAR', s)
    
    def t_attribute(self, s):
        r' @([a-zA-Z]+\:)?[a-zA-Z][a-zA-Z0-9_]* '
        self.push('ATTRIBUTE', s[1:])
    
    def t_keyword(self, s):
        r' \![a-zA-Z]+ '
        self.push('KW_' + s[1:].upper(), s)
    
    def t_arrow(self, s):
        r' -> '
        self.push('ARROW', s)
    
    def t_slash(self, s):
        r' / (?!/) '
        self.push('SLASH', s)
    
    def t_doubleslash(self, s):
        r' // '
        self.push('DOUBLESLASH', s)
    
    def t_doubledot(self, s):
        r' \.\. '
        self.push('DOUBLEDOT', s)
    
    def t_star(self, s):
        r' \* '
        self.push('STAR', s)
