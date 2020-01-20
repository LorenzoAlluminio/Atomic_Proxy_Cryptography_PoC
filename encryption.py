

import random
import math
import sys

from elgamal import *


def encode(sPlaintext, iNumBits):
		byte_array = bytearray(sPlaintext,'utf-16')


		#z is the array of integers mod p
		z = []

		#each encoded integer will be a linear combination of k message bytes
		#k must be the number of bits in the prime divided by 8 because each
		#message byte is 8 bits long
		k = iNumBits//8

		#j marks the jth encoded integer
		#j will start at 0 but make it -k because j will be incremented during first iteration
		j = -1 * k
		#num is the summation of the message bytes
		num = 0
		#i iterates through byte array
		for i in range( len(byte_array) ):
                    #if i is divisible by k, start a new encoded integer

                    if i % k == 0:
                        j += k
                        num = 0
                        z.append(0)
                        #add the byte multiplied by 2 raised to a multiple of 8
                    z[j//k] += byte_array[i]*(2**(8*(i%k)))

		#example
				#if n = 24, k = n / 8 = 3
				#z[0] = (summation from i = 0 to i = k)m[i]*(2^(8*i))
				#where m[i] is the ith message byte

		#return array of encoded integers
		return z

def encryption(publicKey, plainText):
    z = encode(plainText, publicKey.iNumBits)
    cipher_pairs = []
    for i in z:
		#pick random y from (0, p-1) inclusive
	while True:
            k = random.randint(1, (publicKey.p - 1))
            if gcd(k, publicKey.p-1)==1:
                break
        #c = g^y mod p
        gk = modexp( publicKey.g, k, publicKey.p )
        c1 = (i*gk )% publicKey.p
        #d = ih^y mod p
        c2 = modexp( publicKey.h, k, publicKey.p )
        #add the pair to the cipher pairs list
        cipher_pairs.append( [c1, c2] )
    return cipher_pairs

def decryption(privateKey, cipher_pairs ):
    plaintext = []
    for i in cipher_pairs:
        c1 = i[0]
        c2 = i[1]
        s = modexp( c2, privateKey.x_inv, privateKey.p )

        plain = (c1*modinv( s,  privateKey.p)) % privateKey.p
        #add plain to list of plaintext integers
        plaintext.append( plain )
    decryptedText = decode(plaintext, privateKey.iNumBits)
    decryptedText = "".join([ch for ch in decryptedText if ch != '\x00'])
    return decryptedText

def decode(aiPlaintext, iNumBits):
		#bytes array will hold the decoded original message bytes
		bytes_array = []

		#same deal as in the encode function.
		#each encoded integer is a linear combination of k message bytes
		#k must be the number of bits in the prime divided by 8 because each
		#message byte is 8 bits long
		k = iNumBits//8

		#num is an integer in list aiPlaintext
		for num in aiPlaintext:
                    #get the k message bytes from the integer, i counts from 0 to k-1
                    for i in range(k):
                        #temporary integer
                        temp = num
                        #j goes from i+1 to k-1
                        for j in range(i+1, k):
                            #get remainder from dividing integer by 2^(8*j)
                            temp = temp % (2**(8*j))
                        #message byte representing a letter is equal to temp divided by 2^(8*i)
                        letter = temp // (2**(8*i))
                        #add the message byte letter to the byte array
                        bytes_array.append(letter)
                        #subtract the letter multiplied by the power of two from num so
                        #so the next message byte can be found
                        num = num - (letter*(2**(8*i)))

		#example
		#if "You" were encoded.
		#Letter        #ASCII
		#Y              89
		#o              111
		#u              117
		#if the encoded integer is 7696217 and k = 3
		#m[0] = 7696217 % 256 % 65536 / (2^(8*0)) = 89 = 'Y'
		#7696217 - (89 * (2^(8*0))) = 7696128
		#m[1] = 7696128 % 65536 / (2^(8*1)) = 111 = 'o'
		#7696128 - (111 * (2^(8*1))) = 7667712
		#m[2] = 7667712 / (2^(8*2)) = 117 = 'u'

		decodedText = bytearray(b for b in bytes_array).decode('utf-8')

		return decodedText
def calculateProxyKey(keyA,keyB):
    keyPiAB = ProxyKey(keyA.p,keyA.g,keyB.x * keyA.x_inv)
    return keyPiAB
def encryptionProxy(cipher_pairs,keyPiAB):
    newcipher_pairs = []
    for i in cipher_pairs:
        c1 = i[0]
        c2 = i[1]
        c2 = modexp( c2, keyPiAB.piab, keyPiAB.p )
        newcipher_pairs.append( [c1, c2] )

        #add plain to list of plaintext integers
    return newcipher_pairs

keysAlice = generate_keys(32)
#TODO ma sta g la teniamo o no???? funziona con tutti e due
keysBob  = generate_keys(32,p=keysAlice['publicKey'].p,g=keysAlice['publicKey'].g)
enc = encryption(keysAlice['publicKey'],"ciaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaadasdasdsadasdas")
keysPiAB = calculateProxyKey(keysAlice['privateKey'],keysBob['privateKey'])
print keysPiAB.piab
enc = encryptionProxy(enc,keysPiAB)
print enc
print decryption(keysBob['privateKey'],enc)
