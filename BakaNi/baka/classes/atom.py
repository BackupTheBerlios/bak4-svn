#!/usr/bin/env python2.4
# encoding: utf-8

# copyright (c) domenico carbotta <domenico.carbotta@gmail.com>, 2005
# code released under the gnu gpl, see license.txt


__all__ = ['Atom', 'AuxAtom']


from ima.util.vargenerator import *


def quote(container):
    
    def q(x):
        if x.startswith('?') or x == '_':
            # le pseudocostanti e le variabili anonime non devono subire
            # escaping
            return x
        elif not x[0].isalnum():
            # simboli speciali hanno bisogno di apici e di un prefisso
            # costituito da una lettera minuscola (prolog li deve riconoscere
            # come costanti)
            return "'x_" + x + "'"
        else:
            # business as usual
            return "'" + x + "'"
        
    if type(container) is list:
        rv = []
        for v in container:
            rv.append(q(v))
        return rv
    elif type(container) is dict:
        rv = {}
        for k, v in container.iteritems():
            rv[k] = q(v)
        return rv


class Atom (object):
    
    def __init__(self, doctype, element, parameters=None):
        self.doctype = doctype
        self.element = element
        
        if parameters is None:
            self.parameters = {}
        else:
            self.parameters = parameters
        
        # costruzione del template
        if True: # 20050906
            self.required_parameters = []
        else:
            self.required_parameters = ['$id', '$pos', '$parent']
        self.required_parameters += self.doctype.elements[self.element]
        
        interp = '%%(%s)s'
        args = ', '.join([interp % par for par in self.required_parameters])
        
        if doctype.id is not None:
            at_document = '@' + doctype.id
        else:
            at_document = ''
        self.template = "'" + element + at_document + "'(" + args + ")"
    
    def copy(self):
        return Atom(self.doctype, self.element, self.parameters.copy())
    
    def compatible_with(self, other):
        if(isinstance(other, Atom) and self.doctype == other.doctype and
                        self.element == other.element):
                        
            # due atomi sono compatibili se fanno riferimento allo stesso
            # tipo di elemento dello stesso tipo di documento e hanno
            # lo stesso id.
            
            if ('$id' in self.parameters and
                    '$id' in other.parameters and
                    self.parameters['$id'] == other.parameters['$id']):
                return True
        
        return False
    
    def join(self, other):
        # prerequisito: i due atomi devono essere compatibili
        
        # genero atomi di comparazione per i valori presenti in entrambe
        # gli atomi passati come parametro.
        overlapping = [(self.parameters[x], other.parameters[x])
                        for x in self.parameters if x in other.parameters]
        overlapping = [x for x in overlapping if x[0] != x[1]]
        explain_overlapping = [AuxAtom('=', x) for x in overlapping]
        
        # unisco le informazioni contenute nelle due liste dei parametri.
        params = self.parameters.copy()
        params.update(other.parameters)
        
        return Atom(self.doctype, self.element, params), explain_overlapping
    
    def render(self, var_factory=None, human_readable=False):        
        if var_factory is None:
            var_factory = VarGenerator.factory('X')
        params = self.parameters.copy()
        for p in self.required_parameters:
            if p not in params:
                if human_readable:
                    params[p] = '_'
                else:
                    params[p] = var_factory()
        return self.template % quote(params)
    
    def __str__(self):
        return self.render(human_readable=True)
    
    def __repr__(self):
        return self.render(human_readable=True)


class AuxAtom (object):
    
    def __init__(self, op, parameters, negated=False):
        self.op = op
        self.parameters = list(parameters)
        self.negated = negated
    
    def render(self):
        rv = "'" + self.op + "'"
        rv += '(' + ', '.join(quote(self.parameters)) + ')'
        if self.negated:
            return '~' + rv
        else:
            return rv
        
    def copy(self):
        return AuxAtom(self.op, self.parameters, self.negated)
    
    def __str__(self):
        return self.render()
    
    def __repr__(self):
        return 'AuxAtom(%s, %s, %s)' % (self.op,
                ', '.join(map(repr, self.parameters)), self.negated)
