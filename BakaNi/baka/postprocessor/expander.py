#!/usr/bin/env python2.4
# encoding: utf-8

# copyright (c) domenico carbotta <domenico.carbotta@gmail.com>, 2005
# code released under the gnu gpl, see license.txt


__all__ = ['expand']


from baka.classes.atom import *
from baka.classes.step import *
from baka.util.vargenerator import *
from baka.languages.sdd import *
from baka.classes.ppstate import *
from baka.languages.xpathlog import *


is_doc = lambda x: isinstance(x, AuxAtom) and x.op == '!document'


def normalize_comparison(atom):
    '''
        Normalizza le comparazioni, restituendo una disgiunzione di predicati
        che utilizzano gli operatori "minore di" e "uguale". Simp ringrazia.
    '''
        
    if atom.op is '>':
        return [AuxAtom('<', reversed(atom.parameters))]
    elif atom.op is '<=':
        return [AuxAtom('<', atom.parameters),
                AuxAtom('=', atom.parameters)]
    elif atom.op is '>=':
        return [AuxAtom('<', reversed(atom.parameters)),
                AuxAtom('=', atom.parameters)]
    else:
        return [atom]


def debug(*msg):
    for i in msg:
        print i,
    print

def expand(steps, dtcollection, var_format='Post'):
    
    print steps
    var_factory = VarGenerator.factory(var_format)
    
    states = [PPState()]
    for step in steps:
        
        print step
        
        if is_doc(step):
            for state in states:
                doctype_name = dtcollection.get(step.parameters[1]).id
                state.steps.append(step)
                state.context[step.parameters[0]] = (doctype_name, Document)
        
        elif isinstance(step, AuxAtom):
            states_after = []
            for state in states:
                for normalized_atom in normalize_comparison(step):
                    states_after.append(state.fork(normalized_atom, {}))
            states = states_after
        
        elif isinstance(step, LinearStep):
            states_after = []
            for state in states:
                parent_type = state.context[step.start]
                doctype = dtcollection.doctypes[parent_type[0]]
                if (parent_type[-1], step.qualifier) not in doctype.edges:
                    debug(state, 'killed at step', step)
                else:
                    step_context = {step.id: parent_type + (step.qualifier,)}
                    states_after.append(state.fork(step, step_context))
            states = states_after
        
        elif isinstance(step, AttribStep):
            states_after = []
            for state in states:
                parent_type = state.context[step.start]
                doctype = dtcollection.doctypes[parent_type[0]]
                if step.qualifier in doctype.elements[parent_type[-1]]:
                    states_after.append(state.fork(step, {}))
                else:
                    debug(state, 'killed at step', step)
            states = states_after
        
        elif isinstance(step, BridgeStep):
            states_after = []
            for state in states:
                parent_type = state.context[step.start]
                doctype = dtcollection.doctypes[parent_type[0]]
                bridges = [edge for edge in doctype.resolver.edges
                        if edge[0] == parent_type[-1]
                        and edge[-1] == step.qualifier]
                if len(bridges) == 0:
                    debug(state, 'killed at step', step)
                for bridge in bridges:
                    bridge_steps, bridge_context = create_walk(
                            bridge,                 # step_sequence
                            parent_type,            # start_type
                            step.start, step.id,    # start_id, end_id
                            parent_type[0],         # doctype
                            var_format)             # var_format
                    bridge_context[step.id] = parent_type + bridge[1:]
                    states_after.append(state.fork(bridge_steps,
                            bridge_context))
            states = states_after
        
        elif isinstance(step, BridgeAttribStep):
            states_after = []
            for state in states:
                parent_type = state.context[step.start]
                doctype = dtcollection.doctypes[parent_type[0]]
                bridges = [edge for edge in doctype.resolver.edges
                        if edge[0] == parent_type[-1]
                        and step.qualifier in doctype.elements[edge[-1]]]
                if len(bridges) == 0:
                    debug(state, 'killed at step', step)
                for bridge in bridges:
                    fake_var = var_factory()
                    bridge_steps, bridge_context = create_walk(
                            bridge,                 # step_sequence
                            parent_type,            # start_type
                            step.start, fake_var,   # start_id, end_id
                            parent_type[0],         # doctype
                            var_format)             # var_format
                    bridge_context[fake_var] = parent_type + bridge[1:]
                    bridge_steps.append(AttribStep(fake_var, step.qualifier,
                            step.id))
                    states_after.append(state.fork(bridge_steps,
                            bridge_context))
            states = states_after
        
        elif isinstance(step, UpStep):
            states_after = []
            for state in states:
                print step
                parent_type = state.context[step.start]
                if parent_type[:-2] is Document:
                    debug(state, 'killed at step', step)
                else:
                    id = step.id
                    res = None
                    for other_step in state.steps:
                        if (isinstance(other_step, LinearStep) and
                                other_step.id == step.start):
                            res = AuxAtom('=', (other_step.start, id))
                            break
                    if res is None:
                        res = step
                    step_context = {id: parent_type[:-1]}
                    states_after.append(state.fork(res, step_context))
            states = states_after
        
        for state in states:
            print state
        print '---'
    
    return states
