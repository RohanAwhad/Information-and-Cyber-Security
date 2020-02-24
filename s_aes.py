#!/usr/bin/env python3

SBOX = [[9, 10, 13, 8], [4, 11, 1, 5], [6, 0, 12, 15], [2, 3, 14, 7]]
INV_SBOX = [[10, 9, 1, 8], [5, 11, 7, 15], [6, 2, 12, 13], [0, 3, 4, 14]]
RCON = ['10000000', '00110000']
M_E = [1, 4, 4, 1]
INVERSE_M_E = [9, 2, 2, 9]

def multiplicationx(a, b):
	m = 19
	ans = []
	for i in range(1, len(b) + 1):
		if b[-i] == '0':
			ans.append(0)
		else:
			ans.append(int(a + '0'*(i-1), 2))

	final_ans = ans[0]
	for i in range(1, len(ans)):
		final_ans ^= ans[i]

	while True:
		len_final_ans = len(bin(final_ans))
		len_m = len(bin(m))

		if len_final_ans >= len_m:
			final_ans ^= int(bin(m)[2:] + '0'*(len_final_ans-len_m), 2)
		else:
			break

	print(f"{a} x {b} = {'{:04b}'.format(final_ans)}")
	return final_ans

def mix_col(S, M_e):
	S_dash = []
	for i in range(0, 4, 2):
		for j in range(0, 4, 2):
			ans = '{:04b}'.format(multiplicationx('{:04b}'.format(M_e[j]), S[i]) ^ multiplicationx('{:04b}'.format(M_e[j+1]), S[i+1]))
			S_dash.append(ans)

	return S_dash

def get_sbox_val(s, S_BOX):
	row = int(s[0] + s[3], 2)
	col = int(s[1] + s[2], 2)

	ret = '{:04b}'.format(S_BOX[row][col])
	print(f"{s} -> SBOX -> {ret}")
	return ret

def keygen(w0, w1, i):
	w1_1 = w1[:4]
	w1_2 = w1[4:]

	w1_1, w1_2 = w1_2, w1_1
	w1_1 = get_sbox_val(w1_1, SBOX)
	w1_2 = get_sbox_val(w1_2, SBOX)

	w2 = '{:08b}'.format(int(w0,2) ^ int(w1_1 + w1_2, 2) ^ int(RCON[i], 2))
	w3 = '{:08b}'.format(int(w2, 2) ^ int(w1, 2))

	return [w2, w3]

def encrypt_main_round(text, key):
	text_split = []
	for i in range(0, 16, 4):
		text_split.append(text[i:i+4])
	assert len(text_split) == 4

	sbox_op = []
	for i in range(len(text_split)):
		sbox_op.append(get_sbox_val(text_split[i], SBOX))
	print(f"Applying SBOX on {' '.join(i for i in text_split)} gives output {' '.join(i for i in sbox_op)}")

	sbox_op[1], sbox_op[3] = sbox_op[3], sbox_op[1]

	mix_col_op = mix_col(sbox_op, M_E)
	print(f"Applying MIXCOL operation on {' '.join(i for i in sbox_op)} gives output {' '.join(i for i in mix_col_op)}")

	combine = ''.join(i for i in mix_col_op)

	ret = '{:016b}'.format(int(combine, 2) ^ int(key, 2))
	return ret

def encrypt_final_round(text, key):
	text_split = []
	for i in range(0, 16, 4):
		text_split.append(text[i:i+4])
	assert len(text_split) == 4

	for i in range(len(text_split)):
		text_split[i] = get_sbox_val(text_split[i], SBOX)

	text_split[1], text_split[3] = text_split[3], text_split[1]

	combine = ''.join(i for i in text_split)

	ret = '{:016b}'.format(int(combine, 2) ^ int(key, 2))
	return ret
	
def encryption(plaintext, keys):
	pr_op = '{:016b}'.format(int(plaintext, 2) ^ int(keys[0], 2))
	print(f"PreRound Key Addition : {pr_op}")

	main_op = encrypt_main_round(pr_op, keys[1])
	print(f"Main Round output : {main_op}")

	final_op = encrypt_final_round(main_op, keys[2])
	print(f"Final Round output : {final_op}")

	return final_op

def decrypt_main_round(text, key):
	add_key = '{:016b}'.format(int(text, 2) ^ int(key, 2))
	print(f"Add Round 1 Key output : {add_key}")

	text_split = [add_key[i:i+4] for i in range(0, 16, 4)]
	text_split = mix_col(text_split, INVERSE_M_E)
	print(f"Inverse Mix Col Output : {' '.join(i for i in text_split)}")

	text_split[1], text_split[3] = text_split[3], text_split[1]

	inv_sbox_op = [get_sbox_val(i, INV_SBOX) for i in text_split]
	print(f"Inverse SBOX Output : {' '.join(i for i in inv_sbox_op)}")

	ret = ''.join(i for i in inv_sbox_op)
	return ret

def decrypt_final_round(text, key):
	add_key = '{:016b}'.format(int(text, 2) ^ int(key, 2))
	print(f"Add Round 2 Key output : {add_key}")

	text_split = [add_key[i:i+4] for i in range(0, 16, 4)]
	text_split[1], text_split[3] = text_split[3], text_split[1]

	inverse_sbox_op = [get_sbox_val(i, INV_SBOX) for i in text_split]
	print(f"Inverse SBOX Output : {' '.join(i for i in inverse_sbox_op)}")
	
	ret = ''.join(i for i in inverse_sbox_op)
	return ret

def decryption(ciphertext, keys):
	final_op = decrypt_final_round(ciphertext, keys[0])
	print(f"Final Round output : {final_op}")
	
	main_op = decrypt_main_round(final_op, keys[1])
	print(f"Main Round output : {main_op}")
	
	ret = '{:016b}'.format(int(main_op, 2) ^ int(keys[2], 2))

	return ret

if __name__=='__main__':
	plaintext = '1001001110110001' # 16 bit
	ip_key = '0101011010111101' # 16 bit
	
	print(f"PlainText : {plaintext} | Input Key : {ip_key}")

	keys = [ip_key[:8], ip_key[8:]]
	for i in range(2):
		keys.extend(keygen(keys[-2], keys[-1], i))

	print(f"Generated Keys : {' | '.join(keys[i]+keys[i+1] for i in range(0, len(keys), 2))}")

	encrypt_keys = [keys[i]+keys[i+1] for i in range(0, len(keys), 2)]
	decrypt_keys = encrypt_keys.copy()
	decrypt_keys.reverse()

	print(f"Encryption Keys : {' | '.join(encrypt_keys[i] for i in range(0, len(encrypt_keys)))}")
	print(f"Decryption Keys : {' | '.join(decrypt_keys[i] for i in range(0, len(decrypt_keys)))}")
	
	ciphertext = encryption(plaintext, encrypt_keys)
	print(f"Encrypted ciphertext : {ciphertext}")
	decrypted_plaintext = decryption(ciphertext, decrypt_keys)
	print(f"Decrypted ciphertext : {decrypted_plaintext}")
