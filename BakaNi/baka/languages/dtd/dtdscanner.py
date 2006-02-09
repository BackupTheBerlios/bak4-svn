#!/usr/bin/env python2.4
# encoding: utf-8

# copyright (c) domenico carbotta <domenico.carbotta@gmail.com>, 2005
# code released under the gnu gpl, see license.txt


__all__ = ['DTDScanner']


from ima.languages.toolchain import *


class DTDScanner (Scanner):
    
    def t_z_required(self, s):
        r' REQUIRED '
        self.push('REQUIRED', s)
    
    def t_a_id(self, s):
        r' ([a-zA-Z]+\:)?[a-zA-Z][a-zA-Z0-9_]* '
        self.push('ID', s)
    
    def t_blockdelimiters(self, s):
        r' ( \( | \) | <(!--)? | (--)?> ) '
        names = {
            '(': 'OPENPAREN',
            ')': 'CLOSEPAREN',
            '<': 'OPENTRI',
            '>': 'CLOSETRI',
            '<!--': 'OPENCOMMENT',
            '-->': 'CLOSECOMMENT'
        }
        self.push(names[s], s)
    
    def t_semicolon(self, s):
        r' ; '
        self.push('SEMICOLON', s)
    
    def t_comma(self, s):
        r' , '
        self.push('COMMA', s)
    
    def t_cdata(self, s):
        r' \#CDATA '
        self.push('CDATA', s)
    
    def t_pcdata(self, s):
        r' \#PCDATA '
        self.push('PCDATA', s)
    
    def t_empty(self, s):
        r' \#EMPTY '
        self.push('EMPTY')
    
    def t_keyword(self, s):
        r' \![a-zA-Z]+ '
        self.push('KW_' + s[1:].upper(), s)
    
    def t_string(self, s):
        r' " [^"]* " '
        self.push('STRING', s[1:-1])
    
    def t_bar(self, s):
        r' \| '
        self.push('BAR', s)
    
    def t_star(self, s):
        r' \* '
        self.push('STAR', s)
