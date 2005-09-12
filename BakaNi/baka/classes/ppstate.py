#!/usr/bin/env pythonw2.4
# encoding: latin-1

# copyright (c) domenico carbotta <domenico.carbotta@gmail.com>, 2005
# code released under the GNU General Public License


from baka.util.symbol import symbol


Text = symbol('Text')
Document = symbol('Document')


class PPState (object):
    
    def __init__(self, steps=None, context=None):
        if steps is None:
            steps = []
        if context is None:
            context = {}
        self.steps = steps
        self.context = context
    
    def copy(self):
        return PPState(self.steps[:], self.context.copy())
    
    def add(self, steps_addition, context_addition):
        if type(steps_addition) not in (tuple, list):
            steps_addition = [steps_addition]
        self.steps.extend(steps_addition)
        self.context.update(context_addition)
        return self
    
    def fork(self, steps_addition, context_addition):
        return self.copy().add(steps_addition, context_addition)
    
    def __repr__(self):
        return self.render()
    
    def render(self):
        rv = 'state:\n'
        rv += '\tsteps:\n'
        for step in self.steps:
            rv += '\t\t' + step.render() + '\n'
        rv += '\tcontext:\n'
        for var, type in self.context.iteritems():
            rv += '\t\t%s: %s\n' % (var, type)
        return rv
