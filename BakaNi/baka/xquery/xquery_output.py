#!/usr/bin/env python2.4
# encoding: utf-8

# copyright (c) domenico carbotta <domenico.carbotta@gmail.com>, 2005
# code released under the gnu gpl, see license.txt


__all__ = ['datalog_to_xquery']


from baka.util.vargenerator import *
from baka.classes.atom import *
from baka.classes.equivalence_classes import *


class Clause (object):
    
    def __init__(self, start, body, id):
        self.id = id
        self.start = start
        self.body = body
    
    def __str__(self):
        if self.start is None:
            return '$%s in $%s' % (self.id, self.body)
        else:
            return '$%s in $%s%s' % (self.id, self.start, self.body)
    
    def __repr__(self):
        return 'Clause(%r, %r, %r)' % (self.start, self.body, self.id)
    
    def depends_upon(self, other):
        if isinstance(other, Clause):
            return self.start == other.body
        else:
            return False


def classify_atoms(atoms):
    is_doc_atom = lambda x: isinstance(x, AuxAtom) and x.op == '!document'
    is_cmp_atom = lambda x: isinstance(x, AuxAtom) and x.op != '!document'
    is_cls_atom = lambda x: isinstance(x, Atom)
    filter_atoms = lambda f: [x for x in atoms if f(x)]
    return map(filter_atoms, [is_doc_atom, is_cmp_atom, is_cls_atom])


def make_clauses(atoms):
    el_clauses = []
    attr_clauses = []
    pos_clauses = []
    
    equivalences = []
    
    for atom in atoms:
        assert isinstance(atom, Atom)
        
        element_id = atom.parameters['$id']
        el_clauses.append(
                Clause(atom.parameters['$parent'], '/' + atom.element,
                        element_id))
        
        for pname, pvalue in atom.parameters.iteritems():
            
            if pname in ['$parent', '$id']:
                continue
            elif pname == '$pos':
                pos_clauses.append(
                        Clause(element_id, '/pos()', pvalue))
            elif pname == '$text':
                opt_clauses.append(
                        Clause(element_id, '/text()', pvalue))
            else:
                attr_clauses.append(
                        Clause(element_id, '/@' + pname, pvalue))
    
    return map(sort_clauses, (el_clauses, attr_clauses, pos_clauses))


def sort_clauses(clauses):
    ordered_list = []
    
    while True:
        if len(clauses) == 0:
            return ordered_list
        
        zero_dep = []
        for clause in clauses:
            if len(filter(clause.depends_upon, clauses)) == 0:
                zero_dep.append(clause)
                clauses.remove(clause)
        
        if len(zero_dep) == 0:
            raise ValueError(clauses)
        
        ordered_list += zero_dep


def simplify(opt_clauses, comparisons):
    candidates = dict([(x.id, x) for x in opt_clauses])
    for cmp in comparisons:
        for op in cmp.parameters:
            if op in candidates:
                del candidates[op]
    return candidates.values()


def standardize_apart(atoms):
    
    synonyms = {}
    new_std_var = VarGenerator.factory('Std_', auto_prefix=False)
    
    for atom in atoms:
        atom = atom.copy
        if not isinstance(atom, Atom):
            continue
        
        for param, value in atom.parameters.iteritems:
            nv = new_std_var()
            atom.parameters[param] = nv
            if value in vars:
                synonyms[value].append(nv)
            else:
                synonyms[value] = [nv]
    
    return atoms, synonyms


def datalog_to_xquery(atoms):
        
    documents, comparisons, clause_atoms = classify_atoms(atoms)
    clause_atoms, synonyms = standardize_apart(clause_atoms)
    el_clauses, attr_clauses, pos_clauses = make_clauses(clause_atoms)
    
    # TODO -- sono qui


if __name__ == '__main__':
    
    from baka.languages.datalog import dltest
    
    for results in dltest():
        datalog_to_xquery(results)
