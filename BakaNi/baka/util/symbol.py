#!/usr/bin/env python2.4
# encoding: latin-1

# copyright (c) domenico carbotta <domenico.carbotta@gmail.com>, 2005
# code released under the gnu gpl, see license.txt


def symbol(string):
    class __Symbol_Class (object):
        def __str__(self): return '__' + string + '__'
        def __repr__(self): return string
        def __add__(self, other): return str.__add__(str(self), other)
    return __Symbol_Class()
