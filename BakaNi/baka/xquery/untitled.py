#!/usr/bin/env python2.4
# encoding: latin-1

# copyright (c) domenico carbotta <domenico.carbotta@gmail.com>, 2005
# code released under the gnu gpl, see license.txt


__all__ = ['datalog_to_xquery']


from baka.util.vargenerator import *
from baka.classes.atom import *


def make_xquery_thingie(dl_var):
    if dl_var.startswith('B_'):
        return VarGenerator().new_var('$_')
    elif dl_var.startswith('V_'):
        return '$' + dl_var[2:]
    elif dl_var.startswith('s_'):
        return '"' + dl_var[2:] + '"'
    else:
        return dl_var


class Clause (object):
    
    def __init__(self, start, body, id):
        self.id = id
        self.start = start
        self.body = body
    
    def __str__(self):
        if self.start is None:
            return '%s in %s' % (self.id, self.body)
        else:
            return '%s in %s%s' % (self.id, self.start, self.body)
    
    def __repr__(self):
        return 'Clause(%r, %r, %r)' % (self.start, self.body, self.id)
    
    def depends_upon(self, other):
        if isinstance(other, Clause):
            return self.start == other.body
        else:
            return False


def classify_atoms(atoms):
    is_doc_atom = lambda x: isinstance(x, AuxAtom) and x.op == '!document'
    is_cmp_atom = lambda x: isinstance(x, AuxAtom) and x.op in ['<', '=']
    documents = filter(is_doc_atom, atoms)
    comparisons = filter(is_cmp_atom, atoms)
    others = [x for x in atoms if x not in documents and x not in comparisons]
    return documents, [x for x in atoms if x not in documents]


def make_clauses(atoms):
    existence_clauses = []
    comparison_clauses = []
    
    for atom in atoms:
        if isinstance(atom, AuxAtom):
            continue
        element_id = atom.parameters['$id']
        existence_clauses.append(
                Clause(atom.parameters['$parent'], '/' + atom.element,
                        element_id))
        
        for pname, pvalue in atom.parameters.iteritems():
            if pname in ['$parent', '$id']:
                continue
            elif pname == '$pos':
                comparison_clauses.append(
                        Clause(element_id, '/pos()', pvalue))
            elif pname == '$text':
                comparison_clauses.append(
                        Clause(element_id, '/text()', pvalue))
            else:
                existence_clauses.append(
                        Clause(element_id, '/@' + pname, pvalue))
    
    return sort(existence_clauses), sort(comparison_clauses)


def sort(clauses):
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


def datalog_to_xquery(atoms, vars, literals, parameters):
    
    documents, comparisons = classify_atoms(atoms)
    existence_clauses, comparison_clauses = make_clauses(atoms)
    
    for clause in existence_clauses + comparison_clauses:
        print clause


if __name__ == '__main__':
    
    from baka.languages.datalog import dltest
    
    for results in dltest():
        datalog_to_xquery(*results)
