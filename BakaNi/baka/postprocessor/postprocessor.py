#!/usr/bin/env python2.4
# encoding: utf-8

# copyright (c) domenico carbotta <domenico.carbotta@gmail.com>, 2005
# code released under the gnu gpl, see license.txt


__all__ = ['Postprocessor']


from baka.classes.step import *
from baka.classes.atom import *
from baka.classes.ppstate import *
from baka.util.vargenerator import VarGenerator


class Postprocessor (object):
    '''
        VERY deprecated.
    '''
    
    def __init__(self, dtcollection, var_factory=None, debug=True):
        self.dtcollection = dtcollection
        if var_factory is None:
            print 'no no no'
            self.new_var = VarGenerator.factory('Lin')
        else:
            print 'ok'
            self.new_var = var_factory
        self.debug_enabled = debug
    
    def debug(self, msg):
        if self.debug_enabled:
            print 'pp>\t', msg
    
    def process(self, steps):
        st = self.remove_stars(steps)
        return self.build_bridges(st)
    
    def remove_stars(self, steps):
        
        self.debug('removing stars...')
        
        states = [PPState()]
        
        for step in steps:
            
            if isinstance(step, AuxAtom):
                context_add = {}
                if step.op == '!document':
                    doc_var = step.parameters[0]
                    doctype = self.dtcollection.get(step.parameters[1])
                    context_add = {doc_var: (doctype.id, Document)}
                for state in states: state.add([step], context_add)
                continue
            
            doctype = self.dtcollection.get(step.doctype)
            resolver = doctype.resolver
            
            if isinstance(step, (LinearStep, BridgeStep)):
                for state in states:
                    state.add([step],
                                    {step.id: (step.doctype, step.qualifier)})
            
            elif isinstance(step, (AttribStep, BridgeAttribStep)):
                for state in states:
                    state.add([step], {step.id: Text})
            
            elif isinstance(step, StarStep):
                rv = []
                for state in states:
                    start_el = state.context[step.start][1]
                    for steps, context in resolver.resolve_star(start_el, step,
                                    self.new_var):
                        rv.append(state.fork(steps, context))
                states = rv
            
            elif isinstance(step, UpStep):
                rv = []
                for state in states:
                    start_el = state.context[step.start][1]
                    for steps, context in resolver.resolve_up(start_el, step,
                                    doctype.id, self.new_var):
                        rv.append(state.fork(steps, context))
                states = rv
            
            else:
                raise Exception, step
            
            self.debug(step.render())
            for state in states:
                self.debug(state.render())
        
        return states
    
    
    def build_bridges(self, states):
        
        self.debug('building bridges...')
        
        rv = []
        
        for state in states:
            
            state_expansions = [PPState([], state.context)]
            self.debug(state_expansions[0])
            for step in state.steps:
                
                if isinstance(step, AuxAtom):
                    for exp in state_expansions:
                        exp.add([step], {})
                    continue
                
                doctype = self.dtcollection.get(step.doctype)
                resolver = doctype.resolver
                
                if isinstance(step, BridgeStep):
                    start_el = state.context[step.start][1]
                    new_expansions = []
                    for steps, context in resolver.resolve_bridge(start_el,
                                    step, self.new_var):
                        new_expansions.extend([exp.fork(steps, context)
                                        for exp in state_expansions])
                    state_expansions = new_expansions
                
                elif isinstance(step, BridgeAttribStep):
                    start_el = state.context[step.start][1]
                    new_expansions = []
                    for steps, context in resolver.resolve_bridge_attrib(
                                    start_el, step, self.new_var):
                        new_expansions.extend([exp.fork(steps, context)
                                        for exp in state_expansions])
                    state_expansions = new_expansions
                
                else:
                    for exp in state_expansions:
                        exp.add([step], {})
                
                self.debug(step.render())
                for state in state_expansions:
                    self.debug(state.render())
            
            rv.extend(state_expansions)
        
        
        return rv
