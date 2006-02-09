#!/usr/bin/env python2.4
# encoding: utf-8

# copyright (c) domenico carbotta <domenico.carbotta@gmail.com>, 2005
# code released under the gnu gpl, see license.txt


__all__ = ['generate_hypotheses']


from ima.classes.atom import *
from ima.util.vargenerator import *


def core(atom):
    return atom.doctype.create_atom(
                    atom.element, {'$id': atom.parameters['$id']})


def is_var(x):
    return type(x) is str and x[0].isupper()


def is_ground(x):
    return type(x) is str and not x[0].isupper()
    
    
def generate_hypotheses(atoms, var_format='Hyp'):
    '''
        Riformula la conoscenza espressa negli atomi passati come
        parametro sotto forma di un insieme di denials.
    '''
    
    new_var = VarGenerator.factory(var_format)
    negate_op = {
            '<': '>=',
            '<=': '>',
            '=': '~=',
            '~=': '=',
            '>=': '<',
            '>': '<='}
    
    aux_atoms = []
    vars = {}
    hypotheses = []
    
    for atom in atoms:
        if isinstance(atom, AuxAtom):
            if atom.op in negate_op:
                neg = AuxAtom(negate_op[atom.op], atom.parameters)
                aux_atoms.append(neg)
            elif atom.op == '!document':
                pass
        elif isinstance(atom, Atom):
            for param, value in atom.parameters.iteritems():
                if not is_var(value) and param != '$id':
                    premise = core(atom)
                    nv = new_var()
                    premise.parameters[param] = nv
                    comparison = AuxAtom('~=', (nv, value))
                    hypotheses.append([premise, comparison])
                else:
                    if value not in vars:
                        vars[value] = (core(atom), param)
    
    for atom in aux_atoms:
        hyp = []
        for p in atom.parameters:
            if is_var(p):
                definition, position = vars[p]
                premise = definition.copy()
                premise.parameters[position] = p
                hyp.append(premise)
        hyp.append(atom)
        hypotheses.append(hyp)
    
    for denial in hypotheses: #-#
        print '<-', ', '.join(map(str, denial)) #-#
    
    return hypotheses
