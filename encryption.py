

import random
import math
import sys



#computes the jacobi symbol of a, n
def jacobi( a, n ):
		if a == 0:
				if n == 1:
						return 1
				else:
						return 0
		#property 1 of the jacobi symbol
		elif a == -1:
				if n % 2 == 0:
						return 1
				else:
						return -1
		#if a == 1, jacobi symbol is equal to 1
		elif a == 1:
				return 1
		#property 4 of the jacobi symbol
		elif a == 2:
				if n % 8 == 1 or n % 8 == 7:
						return 1
				elif n % 8 == 3 or n % 8 == 5:
						return -1
		#property of the jacobi symbol:
		#if a = b mod n, jacobi(a, n) = jacobi( b, n )
		elif a >= n:
				return jacobi( a%n, n)
		elif a%2 == 0:
				return jacobi(2, n)*jacobi(a//2, n)
		#law of quadratic reciprocity
		#if a is odd and a is coprime to n
		else:
				if a % 4 == 3 and n%4 == 3:
						return -1 * jacobi( n, a)
				else:
						return jacobi(n, a )



#solovay-strassen primality test.  tests if num is prime
def gcd( a, b ):
		while b != 0:
			c = a % b
			a = b
			b = c
		#a is returned if b == 0
		return a

def SS( num, iConfidence ):
		#ensure confidence of t
		for i in range(iConfidence):
				#choose random a between 1 and n-2
				a = random.randint( 1, num-1 )

				#if a is not relatively prime to n, n is composite
				if gcd( a, num ) > 1:
						return False

				#declares n prime if jacobi(a, n) is congruent to a^((n-1)/2) mod n
				if not jacobi( a, num ) % num == modexp ( a, (num-1)//2, num ):
						return False

		#if there have been t iterations without failure, num is believed to be prime
		return True

class PrivateKey(object):                                                                                                                                                                     
        def __init__(self, p=None, g=None, a=None,a_inv=None, iNumBits=0):                                                                                                                               
                self.p = p                                                                                                                                                                    
                self.g = g                                                                                                                                                                    
                self.a = a  
                self.a_inv  = a_inv
                self.iNumBits = iNumBits                                                                                                                                                      
                                                                                                                                                                                              
class PublicKey(object):                                                                                                                                                                      
        def __init__(self, p=None, g=None, ga=None, iNumBits=0):                                                                                                                               
                self.p = p                                                                                                                                                                    
                self.g = g                                                                                                                                                                    
                self.ga =ga                                                                                                                                                                    
                self.iNumBits = iNumBits  

def find_primitive_root( p ):
		if p == 2:
				return 1
		#the prime divisors of p-1 are 2 and (p-1)/2 because
		#p = 2x + 1 where x is a prime
		p1 = 2
		p2 = (p-1) // p1

		#test random g's until one is found that is a primitive root mod p
		while( 1 ):
				g = random.randint( 2, p-1 )
				#g is a primitive root if for all prime factors of p-1, p[i]
				#g^((p-1)/p[i]) (mod p) is not congruent to 1
				if not (modexp( g, (p-1)//p1, p ) == 1):
						if not modexp( g, (p-1)//p2, p ) == 1:
								return g
def modexp( base, exp, modulus ):
            return pow(base, exp, modulus)
#find n bit prime
def find_prime(iNumBits, iConfidence):
		#keep testing until one is found
		while(1):
				#generate potential prime randomly
				p = random.randint( 2**(iNumBits-2), 2**(iNumBits-1) )
				#make sure it is odd
				while( p % 2 == 0 ):
						p = random.randint(2**(iNumBits-2),2**(iNumBits-1))

				#keep doing this if the solovay-strassen test fails
				while( not SS(p, iConfidence) ):
						p = random.randint( 2**(iNumBits-2), 2**(iNumBits-1) )
						while( p % 2 == 0 ):
								p = random.randint(2**(iNumBits-2), 2**(iNumBits-1))

				#if p is prime compute p = 2*p + 1
				#if p is prime, we have succeeded; else, start over
				p = p * 2 + 1
				if SS(p, iConfidence):
						return p
def egcd(a, b):
        if a == 0:
            return (b, 0, 1)
        else:
            g, y, x = egcd(b % a, a)
            return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m
    return pow(base, exp, modulus)

def generate_keys(iNumBits=256, iConfidence=32):                                      
                #p is the prime                     
                #g is the primitve root             
                #x is random in (0, p-1) inclusive                                                 
                #h = g ^a mod p
                p = find_prime(iNumBits, iConfidence)                              
                g = find_primitive_root(p)                      
                g = modexp( g, 2, p )                                                                 
                while True:                                         
                       a = random.randint(1, (p - 1))
                       #instead of calculating the gcd we could check if a%2 == 0 && a%q == 0                                                              
                       if gcd(a, p-1)==1:
                               break
                a_inv = modinv(a,p-1)
                h = modexp( g, a, p )
                publicKey = PublicKey(p, g, h, iNumBits)
                privateKey = PrivateKey(p, g,a , a_inv, iNumBits)

                return {'privateKey': privateKey, 'publicKey': publicKey}

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
        c2 = modexp( publicKey.ga, k, publicKey.p )
        #add the pair to the cipher pairs list
        cipher_pairs.append( [c1, c2] )
    return cipher_pairs

def decryption(privateKey, cipher_pairs ):
    plaintext = []
    for i in cipher_pairs:
        c1 = i[0]
        c2 = i[1]
        s = modexp( c2, privateKey.a_inv, privateKey.p )
    		
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

keys = generate_keys(32) 
enc = encryption(keys['publicKey'],"ciaadsasdfijhiasodufadgshuygfadsygfdsgfyudsagfyusadgfads")
print enc
print decryption(keys['privateKey'],enc)


