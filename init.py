from random import *
from elgamal import *
from pwn import *
import os
# TODO increase number of bits

nRound = 10
port = 12345
def generate_proxy_key(a,b,p):
    invb = inverse(b, p-1)
    return (a*invb)%(p)

keysAlice=generate_keys(32,32)
keysBob=generate_keys(32,32,keysAlice['publicKey'].p)
proxyKey = generate_proxy_key(keysAlice['privateKey'].x,keysBob['privateKey'].x,keysAlice['publicKey'].p)

print "python verifier.py " +  str(keysAlice['publicKey'].h) + " " + str(keysAlice['publicKey'].p) +" " +str(keysAlice['privateKey'].g) + " " + str(port) +" "+ str(nRound) + " "+ str(proxyKey) + " "+str(keysBob['publicKey'].h) 
print "python proover.py " +  str(keysAlice['privateKey'].x) + " " +str(keysAlice['privateKey'].p) + " "+str(keysAlice['privateKey'].g)+ " "+ str(port) +" "+ str(nRound)
