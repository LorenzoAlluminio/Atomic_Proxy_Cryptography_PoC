from random import *
from elgamal import *
from pwn import *
import os
# TODO increase number of bits

def generate_keys_bob(iNumBits=256, iConfidence=32,p = None):                                      
                #p is the prime                     
                #g is the primitve root             
                #x is random in (0, p-1) inclusive                                                 
                #h = g ^a mod p 
                if(p == None):
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
                privateKey = PrivateKey(p, g,a, iNumBits)

                return {'privateKey': privateKey, 'publicKey': publicKey}

nRound = 10
port = 12345
def generate_proxy_key(a,b,p):
    invb = inverse(b, p-1)
    return (a*invb)

keysAlice=generate_keys(32,32)
keysBob=generate_keys_bob(32,32,keysAlice['publicKey'].p)


print "python verifier.py " +  str(keysAlice['publicKey'].h) + " " + str(keysAlice['publicKey'].p) +" " +str(keysAlice['privateKey'].g) + " " + str(port) +" "+ str(nRound)
print "python proover.py " +  str(keysAlice['privateKey'].x) + " " +str(keysAlice['privateKey'].p) + " "+str(keysAlice['privateKey'].g)+ " "+ str(port) +" "+ str(nRound)
while(1):
    print p1.recvline()
    print p2.recvline()
p1.wait()
