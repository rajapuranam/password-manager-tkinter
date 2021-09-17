from random import randint

def encrypt(plain_text):
	ascii_values = [ str(ord(ch)).zfill(3) for ch in plain_text ]
	ind = len(ascii_values) // 2
	rotated = ascii_values[ind:] + ascii_values[:ind]
	inversed = [ch[::-1] for ch in rotated]
	padded_1, padded_2 = [], []

	for v in inversed:
		padded_1.append(v)
		r = randint(100, 127)
		padded_1.append(str(r))

	for i in range(0, len(padded_1), 2):
		padded_2.append(padded_1[i])
		padded_2.append(padded_1[i+1])
		r = randint(32, 99)
		padded_2.append(str(r))

	cipher_text = ''.join(padded_2)
	return cipher_text

# def decrypt(cipher_text):
# 	d1, d2 = '', []
# 	for i in range(0, len(cipher_text), 8):
# 		d1 += (cipher_text[i:i+6])
# 	for i in range(0, len(d1), 6):
# 		d2.append(d1[i:i+3])

# 	if len(d2) % 2 == 0:
# 		ind = len(d2) // 2
# 	else:
# 		ind = (len(d2) // 2)+1

# 	ascii_values = d2[ind:] + d2[:ind]
# 	plain_text = ''.join([chr(int(v[::-1])) for v in ascii_values])

# 	return plain_text

