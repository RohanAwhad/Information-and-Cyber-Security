#!/usr/bin/env python3

import random
import numpy as np

def is_primitive(alpha, q):
	n = []
	for i in range(1, q):
		a = (alpha**i) % q
		if a in n: return False
		n.append(a)
	return True

if __name__ == '__main__':
	prime_no = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]

	q = random.choice(prime_no)
	alpha = 2
	while not is_primitive(alpha, q):
		alpha += 1
	print(f"Q = {q} Alpha = {alpha}")

	clients = {'A': {}, 'B': {} }
	for k, v in clients.items():
		x = np.random.randint(2, q)
		y = (alpha**x) % q
		v['X'] = x
		v['Y'] = y

	x_a = clients['A']['X']
	y_a = clients['A']['Y']
	x_b = clients['B']['X']
	y_b = clients['B']['Y']

	key_a = (y_b**x_a) % q
	key_b = (y_a**x_b) % q

	clients['A']['KEY'] = key_a
	clients['B']['KEY'] = key_b

	for k, v in clients.items():
		print(f"For client {k}")
		print(f"  X = {v['X']} Y = {v['Y']} Key = {v['KEY']}")

	
