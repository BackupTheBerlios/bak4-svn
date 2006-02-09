#!/usr/bin/env python2.4
# encoding: utf-8

# copyright (c) domenico carbotta <domenico.carbotta@gmail.com>, 2005
# code released under the gnu gpl, see license.txt


__all__ = ['datalog_to_xquery']


from ima.util.vargenerator import *
from ima.classes.atom import *


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
    return [filter(f, atoms) for f in (is_doc_atom, is_cmp_atom, is_cls_atom)]


def make_clauses(atoms):
    el_clauses = []
    attr_clauses = []
    pos_clauses = []
    
    already_used = []
    equivalences = []
    unique_var = VarGenerator.factory('Uniq')
    
    def make_unique(var):
        if var in already_used:
            nv = unique_var()
            equivalences.append(AuxAtom('=', (nv, var)))
            return nv
        else:
            already_used.append(var)
            return var
        
    for atom in atoms:
        assert isinstance(atom, Atom)
        
        element_id = make_unique(atom.parameters['$id'])
        el_clauses.append(
                Clause(atom.parameters['$parent'], '/' + atom.element,
                        element_id))
        
        for pname, pvalue in atom.parameters.iteritems():
            
            if pname in ['$parent', '$id']:
                continue
            elif pname == '$pos':
                pos_clauses.append(
                        Clause(element_id, '/pos()', make_unique(pvalue)))
            elif pname == '$text':
                attr_clauses.append(
                        Clause(element_id, '/text()', make_unique(pvalue)))
            else:
                attr_clauses.append(
                        Clause(element_id, '/@' + pname, make_unique(pvalue)))
    
    return (el_clauses, attr_clauses + pos_clauses, equivalences)


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


def datalog_to_xquery(atoms):
    
    documents, comparisons, clause_atoms = classify_atoms(atoms)
    comp_clauses, opt_clauses, equivalences = make_clauses(clause_atoms)
    
    comparisons += equivalences
    
    for c in comp_clauses + opt_clauses:
        print c #-#
    
    print '===' #-#
    
    used_ids = []
    for cmp in comparisons:
        used_ids.extend(cmp.parameters)
    
    opt_clauses = [x for x in opt_clauses if x.id in used_ids]
    
    clauses = comp_clauses + opt_clauses
    print 'some' #-#
    print ',\n'.join('\t' + str(x) for x in clauses) #-#
    print 'satisfies' #-#
    print ' and\n'.join('\t$%s %s $%s' % #-#
            (c.parameters[0], c.op, c.parameters[1]) for c in comparisons)



if __name__ == '__main__':
    
    from ima.languages.datalog import dltest
    
    for results in dltest():
        datalog_to_xquery(results)


    