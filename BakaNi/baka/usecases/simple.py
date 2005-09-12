# encoding: latin-1

xpl = '''
    //nome[text() -> $N, pos() -> $P, ../nome[text() > $N, pos() < $P]]
'''

sdd = '''
    !doctype nomi ("!default") {
        nomi -> nome;
        nome -> !PCDATA;
    }
'''

loc = '//nomi'

fragment = '<nome>?n</nome>'