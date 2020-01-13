#!/usr/bin/env python3


def create_matrix(keyword):
	matrix = []
	char_complete = set()
	keyword_index = 0
	alphabet_list = [chr(x) for x in range(ord('a'), ord('z') + 1)]
	alphabet_list.remove('j')
	alphabet_index = 0
	i, j = 0, 0
	while (i < 5):
		j = 0
		temp = []
		while (j < 5):
			if keyword_index < len(keyword):
				letter = keyword[keyword_index]
				keyword_index += 1
			else:
				letter = alphabet_list[alphabet_index]
				alphabet_index += 1
			if letter in char_complete:
				continue
			else:
				temp.append(letter)
				char_complete.add(letter)
			j += 1
		matrix.append(temp)
		i += 1

	return matrix

def encrypt(matrix, plaintext):
	ciphertext = []

	# Get pairs
	pairs = []
	i = 0
	while (i < len(plaintext)):
		if (i+1) == len(plaintext): 
			pairs.append((plaintext[i], 'x'))
		elif plaintext[i] != plaintext[i+1]: 
			pairs.append((plaintext[i], plaintext[i+1]))
		else:
			pairs.append((plaintext[i], 'x'))
			i -= 1
		i += 2

	for (a,b) in pairs:
		# Get positions
		pos = []
		for j in range(5):
			if a in matrix[j]:
				a_pos = (j, matrix[j].index(a))
			if b in matrix[j]:
				b_pos = (j, matrix[j].index(b))

		pos.append(a_pos)
		pos.append(b_pos)

		# Convert to cipher
		
		# same row
		if pos[0][0] == pos[1][0]:
			ciphertext.append((matrix[pos[0][0]][(pos[0][1] + 1) % 5], matrix[pos[1][0]][(pos[1][1] + 1) % 5]))

		# same col
		elif pos[0][1] == pos[1][1]:
			ciphertext.append((matrix[(pos[0][0]+1) % 5][pos[0][1]], matrix[(pos[1][0]+1) % 5][pos[1][1]]))

		# neither
		else:
			ciphertext.append((matrix[pos[0][0]][pos[1][1]], matrix[pos[1][0]][pos[0][1]]))

	ciphertext = ''.join(i+j for (i,j) in ciphertext)
	return ciphertext

def decrypt(matrix, ciphertext):

	plaintext = []

	# Get pairs
	pairs = []
	i = 0
	while (i < len(ciphertext)):
		pairs.append((ciphertext[i], ciphertext[i+1]))
		i += 2

	for (a,b) in pairs:
		# Get positions
		pos = []
		for j in range(5):
			if a in matrix[j]:
				a_pos = (j, matrix[j].index(a))
			if b in matrix[j]:
				b_pos = (j, matrix[j].index(b))

		pos.append(a_pos)
		pos.append(b_pos)

		# Convert to plain
		
		# same row
		if pos[0][0] == pos[1][0]:
			plaintext.append((matrix[pos[0][0]][pos[0][1] - 1], matrix[pos[1][0]][pos[1][1] - 1]))

		# same col
		elif pos[0][1] == pos[1][1]:
			plaintext.append((matrix[pos[0][0] - 1][pos[0][1]], matrix[pos[1][0] - 1][pos[1][1]]))

		# neither
		else:
			plaintext.append((matrix[pos[0][0]][pos[1][1]], matrix[pos[1][0]][pos[0][1]]))

	plaintext = ''.join(i+j for (i,j) in plaintext)
	return plaintext

if __name__ == '__main__':
	keyword = input('Enter Keyword: ').lower()
	matrix = create_matrix(keyword)

	plaintext = input('Enter Your Message: ')
	plaintext = ''.join(i for i in plaintext.lower().split())
	print('Original Message:', plaintext)
	ciphertext = encrypt(matrix, plaintext)
	print('-'*30, 'Encryption', '-'*30)
	print('Encrypted Message:', ciphertext)
	
	plaintext = decrypt(matrix, ciphertext)
	print('-'*30, 'Encryption', '-'*30)
	print('Decrypted Message:', plaintext)
