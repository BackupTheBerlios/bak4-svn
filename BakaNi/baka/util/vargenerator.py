#!/usr/bin/env python2.4
# encoding: latin-1

# copyright (c) domenico carbotta <domenico.carbotta@gmail.com>, 2005
# code released under the gnu gpl, see license.txt


__all__ = ['VarGenerator']


import threading


class VarGenerator (object):
    
    indexes = {}
    TheLock = threading.Lock()
    
    @classmethod
    def create_var(cls, var_format):
        '''
            Restituisce una nuova variabile nel formato indicato
        '''
        cls.TheLock.acquire()
        
        if '%' not in var_format:
            var_format += '%d'
        if var_format not in cls.indexes:
            cls.indexes[var_format] = 0
        i = cls.indexes[var_format]
        cls.indexes[var_format] += 1
        
        cls.TheLock.release()
        
        if var_format[0] in ['$', '?'] or var_format[0].islower():
            return var_format % i
        else:
            return 'B_' + var_format % i
    
    @classmethod
    def factory(cls, var_format):
        '''
            Restituisce una funzione che ad ogni chiamata restituisce una
            nuova variabile nel formato indicato.
        '''
        if '%' not in var_format:
            var_format += '%d'
        def f():
            return cls.create_var(var_format)        
        return f
