from __future__ import print_function
import sys, random

cells = [] #  program cells
delta = (1,0) # current direction
ip = (0,0) # current position of IP
stack = [] # program stack
string_mode = False # string mode (on or off)

# -------- cmd functions -- #

def mv_right():
	global delta
	delta = (1,0)

def mv_down():
	global delta
	delta = (0,1)

def mv_left():
	global delta
	delta = (-1,0)

def mv_up():
	global delta
	delta = (0,-1)

def mv_rand():
	random.choice([mv_right, mv_down, mv_left, mv_up])()

def out_int():
	print(pop())

def out_char():
	try:
		print(chr(pop()), end='')
	except ValueError:
		print(0)

def in_int():
	try:
		push(int(raw_input('int: ')))
	except ValueError: # couldn't parse
		push(0) # maybe end?

def in_char():
	input = raw_input('char: ')
	if len(input)>0:
		try:
			push(ord(input[0]))
		except TypeError: # non ascii char
			push(0)
	else:
		stack.append(0)

def op_add():
	push(pop() + pop())

def op_sub():
	push(-pop() + pop())

def op_mult():
	push(pop() * pop())

def op_div():
	a = pop()
	b = pop()
	try:
		push(b / a)
	except ZeroDivisionError:
		push(0) # ask for input?

def op_mod():
	a = pop()
	b = pop()
	try:
		push(b % a)
	except ZeroDivisionError:
		push(0) # ask for input?

def op_gt():
	push(int(pop() < pop()))

def op_eq():
	push(int(pop() == pop()))

def op_not():
	push(int(not pop()))

def if_hor():
	if pop():
		mv_left()
	else:
		mv_right()

def if_ver():
	if pop():
		mv_up()
	else:
		mv_down()

def stk_dup():
	a = pop()
	push(a)
	push(a)

def stk_swap():
	a = pop()
	b = pop()
	push(a)
	push(b)

def stk_pop():
	pop()

def strmode():
	global string_mode
	string_mode = not string_mode

def bridge():
	update_ip()

def end():
	sys.exit()

# ----------------- cmds -- #

cmd = \
{
	'>':mv_right,
	'v':mv_down,
	'<':mv_left,
	'^':mv_up,
	'?':mv_rand,
	'.':out_int,
	',':out_char,
	'&':in_int,
	'~':in_char,
	'+':op_add,
	'-':op_sub,
	'*':op_mult,
	'/':op_div,
	'%':op_mod,
	'`':op_gt,
	'=':op_eq,
	'!':op_not,
	'_':if_hor,
	'|':if_ver,
	':':stk_dup,
	'\\':stk_swap,
	'$':stk_pop,
	'"':strmode,
	'#':bridge,
	'@':end
}

# --------- program flow -- #

def update_ip():
	global ip
	ip = (ip[0]+delta[0], ip[1]+delta[1])

def prog():
	while True:
		x = ip[0]
		y = ip[1]
		symbol = cells[y][x]
		if symbol == ord('"'):
			strmode()
		elif string_mode:
			try:
				push(symbol)
			except TypeError: # non ascii char
				push(0)
		elif symbol in [ord(x) for x in cmd.keys()]:
			cmd[chr(symbol)]()
		elif symbol == ord(' '):
			pass
		elif symbol in [ord(x) for x in '0123456789']:
			push(int(chr(symbol)))
		else:
			print('Syntax error:', ip)
			end()
		update_ip()

# ----- stack operations -- #

def push(x):
	stack.append(x)

def pop():
	try:
		return stack.pop()
	except IndexError: # empty
		return 0

# ----------------- init -- #

def format_cells():
	global cells
	m = max(map(len, cells))
	for row in cells:
		while len(row) < m:
			row.append(ord(' '))

def main():
	global cells
	cells = [list(map(ord, x.rstrip('\n'))) for x in sys.stdin.readlines()]
	sys.stdin = open('/dev/tty')
	format_cells()
	prog()

if __name__ == '__main__':
	main()