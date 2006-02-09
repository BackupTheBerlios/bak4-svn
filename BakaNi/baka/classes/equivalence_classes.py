#!/usr/bin/env python2.4
# encoding: utf-8

# copyright (c) domenico carbotta <domenico.carbotta@gmail.com>, 2005
# code released under the gnu gpl, see license.txt


__all__ = ['EquivalenceClasses', 'ConstraintError']


from ima.classes.atom import AuxAtom


class ConstraintError (Exception):
    pass


class EquivalenceClasses (object):
    
    def __init__(self):
        self.classes = []
        self.disequalities = []
    
    def class_of(self, item):
        for cls in self.classes:
            if item in cls:
                return cls
    
    def disequal(self, item_a, item_b):
        return ((item_a, item_b) in self.disequalities or
                (item_b, item_a) in self.disequalities)
    
    def check_append(self, item, cls):
        for c in cls:
            if self.disequal(item, c):
                raise ConstraintError('%r conflicts with %r' % (item, c))
    
    def check_create(self, item_a, item_b):
        if self.disequal(item_a, item_b):
            raise ConstraintError('%r conflicts with %r' % (item_a, item_b))
    
    def check_merge(self, class_a, class_b):
        for a in class_a:
            for b in class_b:
                if self.disequal(a, b):
                    raise ConstraintError('%r conflicts with %r' % (a, b))
    
    def check_new_constraint(self, item_a, item_b):
        class_a = self.class_of(item_a)
        class_b = self.class_of(item_b)
        if class_a is None or class_b is None or class_a is class_b:
            return
        else:
            raise ConstraintError('%r, %r belong to the same equivalence class'
                    % (item_a, item_b))
    
    def add_equality_constraint(self, item_a, item_b):
        class_a = self.class_of(item_a)
        class_b = self.class_of(item_b)
        
        if class_a is None:
            if class_b is None:
                self.check_create(item_a, item_b)
                self.classes.append([item_a, item_b])
            else:
                self.check_append(item_a, class_b)
                class_b.append(item_a)
        elif class_b is None:
            self.check_append(item_b, class_a)
            class_a.append(item_b)
        elif class_a is not class_b:
            self.check_merge(class_a, class_b)
            self.classes.remove()
            self.classes.append(class_a + class_b)
    
    def add_disequality_constraint(self, item_a, item_b):
        self.check_new_constraint(item_a, item_b)
        self.disequalities.append((item_a, item_b))
    
    def retrieve_comparisons(self):
        rv = []
        for cls in self.classes:
            a = cls[0]
            for b in cls[1:]:
               rv.append(AuxAtom('=', (a, b)))
        for disequality in self.disequalities:
            rv.append(AuxAtom('<', disequality))
        return rv
