#!/usr/bin/env python2.4
# encoding: utf-8

# copyright (c) domenico carbotta <domenico.carbotta@gmail.com>, 2005
# code released under the gnu gpl, see license.txt


__all__ = ['XMLTranslator']


from xml.dom import minidom
from xuse.classes.doctype import *
from xuse.classes.atom import *
from xuse.languages.xmltranslator.smallerthandom import *
from xuse.util.vargenerator import *


class XMLTranslator (object):
    
    def __init__(self, dtcollection, var_factory=None):
        self.dtcollection = dtcollection
        if var_factory is None:
            self.new_var = VarGenerator.factory('?x')
        else:
            self.new_var = var_factory
    
    def translate(self, xml_fragment, doctype, parent_type, parent_id):
        root_node = minidom.parseString(xml_fragment).documentElement
        check_fragment(root_node, self.dtcollection.get(doctype), parent_type)
        tree = tree_from_dom_node(root_node)
        return self.create_atoms_from_tree(tree, doctype, parent_id,
                        generate_pos=True)
    
    def create_atoms_from_tree(self, node, doctype, parent_id,
                    generate_pos=False):
        rv = []
        attributes = node.attributes.copy()
        for k, v in attributes.iteritems():
            if not v.isdigit() and not v.startswith('?'):
                attributes[k] = 's_' + v
        id = self.new_var()
        attributes['$id'] = id
        attributes['$parent'] = parent_id
        if generate_pos:
            attributes['$pos'] = self.new_var()
        rv.append(self.dtcollection.get(doctype).create_atom(node.name,
                        attributes))
        for child in node.children:
            rv.extend(self.create_atoms_from_tree(child, doctype, id))
        return rv
    
    def create_append_hyp(self, atoms, doctype, parent_type, parent_id):
        doctype = self.dtcollection.get(doctype)
        no_such_atom = []
        no_successive_atoms = []
        no_child_atoms = []
        root_atom = atoms[0]
        sibling_elements = [edge[1] for edge in doctype.edges
                        if edge[0] == parent_type]
        for sibling_element in sibling_elements:
            no_successive_atoms.append([
                    doctype.create_atom(sibling_element, {'$pos': 'P',
                            '$parent': parent_id}),
                    AuxAtom('<', (root_atom.parameters['$pos'], 'P'))
                    ])
            no_successive_atoms.append([
                    doctype.create_atom(sibling_element, {'$pos': 'P',
                            '$parent': parent_id}),
                    AuxAtom('=', ('P', root_atom.parameters['$pos']))
                    ])
        for atom in atoms:
            id = atom.parameters['$id']
            no_such_atom.append([doctype.create_atom(atom.element,
                            {'$id': id})])
            child_elements = [edge[1] for edge in doctype.edges
                    if edge[0] == atom.element]
            for child_element in child_elements:
                no_child_atoms.append([doctype.create_atom(child_element,
                                {'$parent': id})])
        hyp = no_successive_atoms + no_child_atoms + no_such_atom
        return hyp
