from random import *
from elgamal import *
from math import *
from hashlib import *
from struct import *

#TODO increase l
l = 10

def generate_proxy_key(a,b,p):
    invb = inverse(b, p-1)
    return (a*invb)%(p-1)

def sign(m,keys,proxyKey=None):
    a = keys['privateKey'].x
    p=keys['publicKey'].p
    g=keys['publicKey'].g
    h = sha256()
    k = []
    s1 = []
    for i in range(0,l):
        # k is take between 1 and p-1 beacuse is applied to g;
        #which is a generator of group of mod p-1
        k.append(randint(1,p-1))
        s1.append(modexp(g,k[i],p))
        h.update(str(s1[i]))
    hash = h.digest()
    print "s1 --> " + str(s1)
    print "generated hash --> " + hash
    bits = []
    for i in range(0,l):
        bits.append(unpack("<B",hash[i])[0]%2)

    print "extracted bits --> " + str(bits)

    s2 = []
    if(proxyKey != None):
        print "using proxy key: " + str(proxyKey) + " to rencode message " + str(m)
    for i in range(0,l):
        #TODO potential timing attack
        inva = inverse(a, p-1)
        if bits[i] == 1:
            temp = (k[i]-m)*inva
            if(proxyKey != None):
                temp = (temp * proxyKey)
            s2.append(temp)
        else:
            temp = k[i]*inva
            if(proxyKey != None):
                temp = (temp * proxyKey)
            s2.append(temp)

    print "s2 --> " + str(s2)
    return [s1,s2]

def verify(m,signature,pk):
    s1 = signature[0]
    s2 = signature[1]
    ga = pk.h
    g = pk.g
    p = pk.p

    h = sha256()
    for i in range(0,l):
        h.update(str(s1[i]))
    hash = h.digest()

    print "generated hash --> " + hash
    bits = []
    for i in range(0,l):
        bits.append(unpack("<B",hash[i])[0]%2)

    print "extracted bits --> " + str(bits)

    for i in range(0,l):
        inv = inverse(modexp(g, m*bits[i], p), p)
        if modexp(ga,s2[i],p) != ((s1[i]*inv) % p):
            return False

    return True

keysAlice=generate_keys(32,32)
keysBob=generate_keys(32,32,keysAlice['publicKey'].p,keysAlice['publicKey'].g)
m = 1001
signature = sign(m,keysAlice)
print "Verify with Alice publickKey: " + str(verify(m,signature,keysAlice['publicKey']))
print "Verify with Bob publickKey: " + str(verify(m,signature,keysBob['publicKey']))

proxyKey = generate_proxy_key(keysAlice['privateKey'].x,keysBob['privateKey'].x,keysAlice['publicKey'].p)
m = 1001
signature = sign(m,keysAlice,proxyKey)
print "appying verify on: " + str(m)
print "Verify with Alice publickKey: " + str(verify(m,signature,keysAlice['publicKey']))
print "Verify with Bob publickKey: " + str(verify(m,signature,keysBob['publicKey']))
