#!/usr/bin/env python3

import numpy as np
import random
import math

if __name__=='__main__':
	prime_no = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]
	clients = {'A': {}, 'B': {} }
	for k, v in clients.items():
		p = random.choice(prime_no)
		q = random.choice(prime_no)
		while q == p:
			p = random.choice(prime_no)

		n = p * q
		phi_n = (p-1) * (q-1)

		e = np.random.randint(2, phi_n)
		while math.gcd(phi_n, e) != 1:
			e = np.random.randint(2, phi_n)

		d = 1
		while ((e*d)%phi_n != 1) and (e != d):
			d += 1

		v['PR'] = (d, n)
		v['PU'] = (e, n)

		print(f'Client = {k} P = {p} Q = {q} N = {n} Phi(N) = {phi_n} E = {e} D = {d}')


	m = 3
	print(f'Client A sending M = {m} to client B')
	
	b_e, b_n = clients['B']['PU']
	c = (m**b_e) % b_n
	print(f'Encrypted Message using PU(B) = {clients["B"]["PU"]}\nCipher Text is {c}')

	b_d, b_n = clients['B']['PR']
	m = (c**b_d) % b_n
	print(f'Decrypted Message using PR(B) = {clients["B"]["PR"]}\nOriginal Message is {m}')
