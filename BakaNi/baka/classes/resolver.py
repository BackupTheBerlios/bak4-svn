#!/usr/bin/env python2.4
# encoding: latin-1

# copyright (c) domenico carbotta <domenico.carbotta@gmail.com>, 2005
# code released under the gnu gpl, see license.txt


__all__ = ['RecursiveSchemaException', 'Resolver', 'StepExpansionError']


from baka.util.vargenerator import VarGenerator
from baka.classes.step import *
from baka.classes.ppstate import *


class RecursiveSchemaException (Exception):
    pass


def transitive_expansion(edges):
    expansion = []
    for edge_a in edges:
        for edge_b in edges:
            if edge_a[-1] == edge_b[0]:
                new_edge = edge_a[:-1] + edge_b
                # attenzione agli schemi con riferimenti circolari!
                if new_edge[0] == new_edge[-1]:
                    raise RecursiveSchemaException, new_edge
                if new_edge not in edges and new_edge not in expansion:
                    expansion.append(new_edge)
    if len(expansion) == 0:
        return edges
    else:
        return transitive_expansion(edges + expansion)


##      def generate_graph(edges, filename, dir='./'):
##              from os.path import expanduser
##              dotfile = open(expanduser(dir + filename), 'w')
##              print >> dotfile, 'digraph {'
##              print >> dotfile, '\t', 'node [fontname=helvetica]'
##              print >> dotfile, '\t', 'edge [fontname=helvetica]'
##              for edge in edges:
##                      style = ''
##                      if len(edge) > 2:
##                              style = '[style=dashed]'
##                      print >> dotfile, '\t', edge[0], '->', edge[-1], style
##              print >> dotfile, '}'


class StepExpansionError (Exception):
    pass


class Resolver (object):
    
    def __init__(self, doctype):
        self.doctype = doctype
        self.elements = doctype.elements
        self.edges = transitive_expansion(doctype.edges)
    
    def resolve_bridge(self, from_type, step, var_factory=None):
        assert isinstance(step, BridgeStep)
        bridge_filter = (lambda x:
                x[0] == from_type and x[-1] == step.qualifier)
        return self.resolution_walks(bridge_filter, step.start, step.id,
                        step.doctype, var_factory)
    
    
    def resolve_up(self, from_type, step, var_factory=None):
        assert isinstance(step, UpStep)
        up_filter = lambda x: len(x) == 2 and x[1] == from_type
        return self.resolution_walks(up_filter, step.id, step.start,
                        step.doctype, var_factory)
    
    def resolve_star(self, from_type, step, var_factory=None):
        assert isinstance(step, StarStep)
        star_filter = lambda x: len(x) == 2 and x[0] == from_type
        return self.resolution_walks(star_filter, step.start, step.id,
                        step.doctype, var_factory)
    
    def resolve_bridge_attrib(self, from_type, step, var_factory=None):
        assert isinstance(step, BridgeAttribStep)
        
        bridge_var = self.new_var()
        bridge_arrivals = filter(
                lambda x: step.qualifier in self.elements[x],
                self.elements)
        forged_steps = [BridgeStep(step.start, arrival, bridge_var,
                step.doctype, var_factory) for arrival in bridge_arrivals]
        solutions = [resolve_bridge(from_type, forged_step, var_factory)
                for forged_step in forged_steps]
        
        for steps, context in solutions:
            steps.append(AttribStep(bridge_var, step.qualifier, step.id,
                    step.doctype))
            context[step.qualifier] = Text
        
        return solutions
    
    def resolution_walks(self, filter_cond, start_id, end_id, doctype,
            var_factory=None):
        walks = filter(filter_cond, self.edges)
        
        if len(walks) == 0:
            raise StepExpansionError, (start_id, end_id)
        
        return [create_walk(walk, start_id, end_id, doctype, var_factory)
                for walk in walks]
