#!/usr/bin/env python2.4

# copyright (c) domenico carbotta <domenico.carbotta@gmail.com>, 2005
# code released under the gnu gpl, see license.txt

'''
infinite.py
Infinite is not a finite state machine.
'''

from copy import copy, deepcopy

from lex import LexToken


class MachineStopException (Exception):
	pass


class NonFinalStateException (Exception):
	pass


class NonExistentStateException (Exception):
	pass


class ListUtils:
	
	@staticmethod
	def peek(lst):
		if len(lst) > 0:
			return lst[-1]
		else:
			return None
	
	@staticmethod
	def pop(lst):
		if len(lst) > 0:
			return lst.pop()
		else:
			return None
	
	@staticmethod
	def push(lst, item):
		if item is None:
			return
		elif type(item) in (list, tuple):
			lst.extend(map(deepcopy, item))
		else:
			lst.append(deepcopy(item))


class Transition (object):
	
	@staticmethod
	def copy_input(token, top):
		return token
	
	@staticmethod
	def copy_top(token, top):
		return top
	
	def __init__(self, expect, next_state, output=None, stack_output=None,
			is_epsilon=False):
		
		if callable(expect):
			# expect è una funzione: agli atti...
			self.expect = expect
		elif type(expect) is str:
			# expect è una stringa: è il tipo di token atteso in input
			self.expect = lambda token, top: token.type == expect
		elif type(expect) is tuple:
			# expect è una tupla: il primo elemento è il tipo di token
			# atteso in input, il secondo è il tipo di token atteso in cima
			# allo stack.
			if expect[0] is not None:
				self.expect = lambda token, top: (token.type == expect[0]
					and top.type == expect[1])
			else:
				# in particolare, se il tipo di token in input atteso è None,
				# il controllo viene effettuato solo sul tipo del token in
				# cima allo stack
				self.expect = lambda token, top: top.type == expect[1]
		
		if output is None:
			# se non è specificata la funzione di output, copiamo il token di
			# ingresso
			self._output = lambda token, top: token
		elif callable(output):
			# se output è una funzione: agli atti...
			self._output = output
		else:
			# se output è qualcos'altro, è il valore da restituire
			self._output = lambda token, top: output
		
		if stack_output is None:
			# se non è specificata la funzione di output sullo stack,
			# lasciamolo immutato.
			self._stack_output = lambda token, top: top
		elif callable(stack_output):
			self._stack_output = stack_output
		else:
			self._stack_output = lambda token, top: stack_output
		
		self.next_state = next_state
		self.is_epsilon = is_epsilon
	
	def ok(self, token, top):
		return self.expect(token, top)
	
	def output(self, token, top):
		return self._output(token, top)
	
	def stack_output(self, token, top):
		return self._stack_output(token, top)


class Machine (object):
	
	def __init__(self, initial_state, transitions, final_states):
		self.transitions = transitions
		self.final_states = final_states
		self.initial_state = initial_state
		self.reset()
		
	def reset(self, keep_input=False):
		self.output = []
		self.i = 0
		self.state = self.initial_state
		self.stack = [LexToken('Z0')]
		if not keep_input:
			self.input = []
	
	def feed(self, input):
		if input is not None:
			self.input[-1:] = deepcopy(input)

	def step(self):
		if self.i >= len(self.input):
			token = None
			eps = True	# siamo a fine stringa, accettiamo solo epsilon-mosse
		else:
			token = self.input[self.i]
			eps = False
		top = ListUtils.peek(self.stack)
		#
		#
		#
		print self.stack, eps, self.output
		#
		#
		#
		state_transitions = self.transitions[self.state]
		for transition in state_transitions:
			if eps and not transition.is_epsilon:
				continue
			elif transition.ok(token, top):
				top = ListUtils.pop(self.stack)
				output = transition.output(token, top)
				stack_output = transition.stack_output(token, top)
				return (transition.next_state, output, stack_output,
						transition.is_epsilon)
		return None, None, None, None
	
	def run(self, input=None):
		if input is None:
			self.reset(keep_input=True)
		else:
			self.reset(keep_input=False)
			self.feed(input)
		
		while 1:
			n_state, n_out, n_stack, n_eps = self.step()
			if n_state is None:
				if (self.i >= len(self.input) and
						self.state in self.final_states):
					out = copy(self.output)
					out.reverse()
					return out
				else:
					raise NonFinalStateException, self
				raise MachineStopException, self
			else:
				if n_state not in self.transitions:
					raise NonExistentStateException, nstate
				print n_state, n_out
				ListUtils.push(self.output, n_out)
				ListUtils.push(self.stack, n_stack)
				self.state = n_state
				if n_eps is not None:
					self.i += 1


if __name__ == '__main__':
	tt = {
		'q0':
			[Transition('ZERO', 'q0', [], lambda x, y: [y, x]),
			Transition('ONE', 'q0', [], lambda x, y: [y, x]),
			Transition('$', 'q1', [], None)],
		'q1':
			[Transition((None, 'ZERO'), 'q1', LexToken('ZERO'), [], True),
			Transition((None, 'ONE'), 'q2', LexToken('ONE'), [], True)],
		'q2':
			[Transition((None, 'ZERO'), 'q2', LexToken('ONE'), [], True),
			Transition((None, 'ONE'), 'q2', LexToken('ZERO'), [], True)]
	}
	ifsm = Machine('q0', tt, ['q1', 'q2'])
	n = [LexToken('ZERO'), LexToken('ONE'), LexToken('ONE'), LexToken('ONE'),
			LexToken('$')]
	print ifsm.run(input=n)
