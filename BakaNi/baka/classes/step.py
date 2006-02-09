#!/usr/bin/env python2.4
# encoding: utf-8

# copyright (c) domenico carbotta <domenico.carbotta@gmail.com>, 2005
# code released under the gnu gpl, see license.txt


from ima.util.symbol import *
from ima.classes.atom import AuxAtom
from ima.util.vargenerator import *


FragmentRoot = symbol('FragmentRoot')
FilterRoot = symbol('FilterRoot')
Undefined = symbol('Undefined')


class CircularRefException (Exception):
    pass


class Step (object):
    
    Name = None
    
    def __init__(self, start, id, doctype=None):
        self.start = start
        self.id = id
        self.doctype = doctype
    
    def render(self):
        raise NotImplementedError()
    
    def __str__(self):
        rv = self.render()
        if self.doctype is not None:
            rv = '%s :: ' % self.doctype + rv
        return rv
    
    def __repr__(self):
        return '%s(%r, %r, %r)' % (self.Name, self.start, self.id, self.doctype)


class QualifiedStep (Step):
    
    def __init__(self, start, qualifier, id, doctype=None):
        Step.__init__(self, start, id, doctype)
        self.qualifier = qualifier
    
    def __repr__(self):
        return '%s(%r, %r, %r, %r)' % (self.Name, self.start, self.qualifier,
                        self.id, self.doctype)


class LinearStep (QualifiedStep):
    
    Name = 'LinearStep'
    
    def render(self):
        return self.start + '/' + self.qualifier + ' -> ' + self.id


class StarStep (Step):
    
    Name = 'StarStep'
    
    def render(self):
        return self.start + '/* -> ' + self.id


class BridgeStep (QualifiedStep):
    
    Name = 'BridgeStep'
    
    def render(self):
##              if self.start is FragmentRoot:
##                      return '//' + self.qualifier + ' -> ' + self.id
##              else:
        return self.start + '//' + self.qualifier + ' -> ' + self.id


class UpStep (Step):
    
    Name = 'UpStep'
    
    def render(self):
        return self.start + '/.. -> ' + self.id


class AttribStep (QualifiedStep):
    
    Name = 'AttribStep'
    
    def render(self):
        if self.qualifier.startswith('$'):
            return self.start + '/' + self.qualifier[1:] + '() -> ' + self.id
        else:
            return self.start + '/@' + self.qualifier + ' -> ' + self.id


class BridgeAttribStep (QualifiedStep):
    
    Name = 'BridgeAttribStep'
    
    def render(self):
        ## if self.start is FragmentRoot:
        ##     if self.qualifier.startswith('$'):
        ##         return '//' + self.qualifier[1:] + '()->' + self.id
        ##     else:
        ##         return '//@' + self.qualifier + ' -> ' + self.id
        ## else:
        if self.qualifier.startswith('$'):
            return (self.start + '//' + self.qualifier[1:] +
                            '() -> ' + self.id)
        else:
            return self.start + '//@' + self.qualifier + ' -> ' + self.id


def create_walk(step_sequence, start_type, start_id, end_id, doctype=None,
                var_format='Walk'):
    '''
        Crea una serie di passi semplici (LinearSteps) che parte da un
        elemento con ID start_id e giunge ad un elemento con ID end_id,
        seguendo il cammino definito dagli elementi in step_sequence.
    '''
    
    var_factory = VarGenerator.factory(var_format)
    
    steps = []
    context = {start_id: start_type}
    
    prev_id = start_id
    for step in step_sequence[1:-1]:
        new_id = var_factory()
        steps.append(LinearStep(prev_id, step, new_id, doctype=doctype))
        context[new_id] = context[prev_id] + (step,)
        prev_id = new_id
    steps.append(LinearStep(prev_id, step_sequence[-1], end_id, doctype))
    
    return steps, context


def dependence_list(a, step_list):
    def depends_upon(b):
        is_step = lambda x: isinstance(x, Step)
        is_doc = lambda x: isinstance(x, AuxAtom) and x.op == '!document'
        is_aux = lambda x: isinstance(x, AuxAtom) and x.op != '!document'
        
        if is_step(a):
            if is_step(b): return a.start == b.id
            if is_doc(b): return a.start == b.parameters[0]
        elif is_aux(a):
            if is_step(b): return b.id in a.parameters
    
    return filter(depends_upon, step_list)


def sort_steps(step_list):
    ordered_list = []
    
    while True:
        if len(step_list) == 0:
            return ordered_list
        
        res = None
        for step in step_list:
            dependences = dependence_list(step, step_list)
            if len(dependences) == 0:
                res = step
                break
        if res == None:
            raise CircularRefException, step_list
        
        step_list.remove(res)
        ordered_list.append(res)
