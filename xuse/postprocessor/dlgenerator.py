#!/usr/bin/env python2.4
# encoding: utf-8

# copyright (c) domenico carbotta <domenico.carbotta@gmail.com>, 2005
# code released under the gnu gpl, see license.txt


__all__ = ['DatalogGenerator', 'generate_datalog']


from xuse.classes.step import *
from xuse.classes.atom import *
from xuse.util.vargenerator import VarGenerator


class DatalogGenerator (object):
    
    def __init__(self, dtcollection, var_factory=None):
        self.dtcollection = dtcollection
        if var_factory is None:
            self.new_var = VarGenerator.factory('X')
        else:
            self.new_var = var_factory
    
    def generate(self, steps, context):
        rv = []
        print '<><><>' #-#
        print context #-#
        
        for step in steps:
            print 'generating', step #-#
            if isinstance(step, AuxAtom):
                rv.append(step)
                continue
            doctype = self.dtcollection.doctypes[context[step.start][0]]
            if isinstance(step, LinearStep):
                a = doctype.create_atom(step.qualifier,
                                {'$id': step.id, '$parent': step.start})
            elif isinstance(step, AttribStep):
                a = doctype.create_atom(context[step.start][-1],
                                {'$id': step.start, step.qualifier: step.id})
            print '\t generated', a #-#
            rv.append(a)
        return rv
    
    def translate(self, states):
        datalog_expr = []
        
        for state in states:
            atoms = []
            atoms = self.generate(state.steps, state.context)
            atoms = simplify_linear(atoms)
            datalog_expr.append(atoms)
        
        return datalog_expr


def simplify_linear(datalog_expr):
    comparisons = []
    hashes = {}
    
    for atom in datalog_expr:
        if isinstance(atom, AuxAtom):
            comparisons.append(atom)
            continue
        atom_hash = atom.element, atom.parameters.get('$id', None)
        if atom_hash in hashes:
            hashes[atom_hash], rest = hashes[atom_hash].join(atom)
            comparisons.extend(rest)
        else:
            hashes[atom_hash] = atom
    
    return hashes.values() + comparisons


def generate_datalog(states, sdd):
    return DatalogGenerator(sdd).translate(states)