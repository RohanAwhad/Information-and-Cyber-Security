#!/usr/bin/env python3

import random
from sys import exit

P10 = [3, 5, 2, 7, 4, 10, 1, 9, 8, 6]
P8 = [6, 3, 7, 4, 8, 5, 10, 9]
IP = [2, 6, 3, 1, 4, 8, 5, 7]
IP_INVERSE = [4, 1, 3, 5, 7, 2, 8, 6]
EP = [4, 1, 2, 3, 2, 3, 4, 1]
P4 = [2, 4, 3, 1]
S0 = [[1, 0, 3, 2], [3, 2, 1, 0], [0, 2, 1, 3], [3, 1, 3, 2]]
S1 = [[0, 1, 2, 3], [2, 0, 1, 3], [3, 0, 1, 0], [2, 1, 0, 3]]
BIN_TO_INT = {'00' : 0, '01' : 1, '10' : 2, '11' : 3}
INT_TO_BIN = {0 : '00', 1 : '01', 2 : '10', 3 : '11'}

def left_shift(s, n):
	ret = s[n:] + s[:n]
	print(f'Left Shift of "{s}" by {n}: "{ret}"')
	return ret

def apply_table(ip, n, table, txt):
	ret = ''
	for i in range(n):
		ret += ip[table[i] - 1]

	print(f'{txt} : {ret}')
	return ret

def key_gen(key, rounds):
	keys = []

	p10_op = apply_table(key, 10, P10, 'P10')
	
	first_half = p10_op[:5]
	second_half = p10_op[5:]

	for i in range(rounds):
		first_half = left_shift(first_half, i+1)
		second_half = left_shift(second_half, i+1)

		combine = first_half + second_half

		p8_op = apply_table(combine, 8, P8, 'P8')

		keys.append(p8_op)

	return keys


def exor(s1, s2):
	exor_op = ''
	assert len(s1) == len(s2)
	for i in range(len(s1)):
		if s1[i] == s2[i]: 
			exor_op = exor_op + '0'
		else:
			exor_op = exor_op + '1'
	
	print(f'"{s1}" EXOR "{s2}" => "{exor_op}"')
	return exor_op

def s_box(ip, s):
	s_row = BIN_TO_INT[ip[0] + ip[3]]
	s_col = BIN_TO_INT[ip[1] + ip[1]]
	s_op = INT_TO_BIN[s[s_row][s_col]]
	return s_op

def func_X(right_half, key):
	ep_op = apply_table(right_half, 8, EP, 'EP')

	exor_op = exor(ep_op, key)

	s0_ip = exor_op[:4]
	s1_ip = exor_op[4:]
	s0 = s_box(s0_ip, S0)
	s1 = s_box(s1_ip, S1)
	combine = s0 + s1

	p4_op = apply_table(combine, 4, P4, 'P4')

	return p4_op

def algo(text, keys):
	ip_tbl_op = apply_table(text, 8, IP, 'IP')

	left_half = ip_tbl_op[:4]
	right_half = ip_tbl_op[4:]

	left_half = exor(left_half, func_X(right_half, keys[0]))

	left_half, right_half = right_half, left_half
	
	left_half = exor(left_half, func_X(right_half, keys[1]))

	combine = left_half + right_half
	ip_inverse_op = apply_table(combine, 8, IP_INVERSE, 'IP_INVERSE')

	return ip_inverse_op

if __name__ == '__main__':
	
	plaintext = '10011011'
	key = '1010000010'
	print(f'Original Message : {plaintext} Key : {key}')

	rounds = 2

	keys = key_gen(key, rounds)
	print(f'Keys : {" ".join(i for i in keys)}')
	
	encrypt_keys = keys.copy()
	decrypt_keys = keys.copy()
	decrypt_keys.reverse()

	ciphertext = algo(plaintext, encrypt_keys)
	print(f'Encrypted Message : {ciphertext}')

	decrypted_plaintext = algo(ciphertext, decrypt_keys)
	print(f'Decrypted Message : {decrypted_plaintext}')

