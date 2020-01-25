from random import *
from elgamal import *
from math import *
from hashlib import *
from struct import *
from termcolor import *
import os

#TODO increase l
l = 10

def generate_proxy_key(a,b,p):
    invb = inverse(b, p-1)
    return (a*invb)%(p-1)


def sign(m,keys,proxyKey=None):
    a = keys['privateKey'].x
    p = keys['publicKey'].p
    g = keys['publicKey'].g
    h = sha256()
    k = []
    s1 = []
    for i in range(0,l):
        # k is take between 1 and p-1 beacuse is applied to g;
        #which is a generator of group of mod p
        k.append(randint(1,p-1))
        s1.append(modexp(g,k[i],p))
        h.update(str(s1[i]))
    hash = h.digest()
    print colored("random vector k --> ","cyan") + str(k) + '\n'
    print colored("s1 --> ", "cyan") + str(s1) + '\n'
    print colored("generated hash --> ", "cyan") + hash.encode("base64") + '\n'

    bits = []
    for i in range(0,l):
        bits.append(unpack("<B",hash[i])[0]%2)

    print colored("extracted bits --> ", "cyan") + str(bits) + '\n'

    #Creating vector s2
    s2 = []
    for i in range(0,l):
        #TODO potential timing attack
        inva = inverse(a, p-1)
        if bits[i] == 1:
            s2.append((k[i]-m)*inva)
        else:
            s2.append(k[i]*inva)

    if proxyKey != None:
        print colored("using proxy key ","cyan") +colored( str(proxyKey),"yellow") +colored( " to rencode s2 --> ","cyan") + str(s2) + '\n'
        for i in range(0,l):
                s2[i] = s2[i]*proxyKey
        print colored("Transformed signature --> ","cyan") + str(s2) +'\n'
    else:
        print colored("s2 --> ", "cyan") + str(s2) + '\n'
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

    bits = []
    for i in range(0,l):
        bits.append(unpack("<B",hash[i])[0]%2)

    res = []
    flag = 0
    for i in range(0,l):
        inv = inverse(modexp(g, m*bits[i], p), p)
        res.append((modexp(ga,s2[i],p)*modexp(g, m*bits[i], p))%p)
        if modexp(ga,s2[i],p) != ((s1[i]*inv) % p):
            flag = 1

    print colored("Output of the verify --> ", "cyan")+ str(res) + '\n'
    #print str(v_inv)
    if flag == 1:
        return False

    return True

#Data shared among different rounds
keysAlice=generate_keys(32,32)
keysBob=generate_keys(32,32,keysAlice['publicKey'].p,keysAlice['publicKey'].g) # we need to pass Alice's p and g because they have to be shared in orther to create a valid proxy key
m= int(sys.argv[1])
proxyKey = generate_proxy_key(keysAlice['privateKey'].x,keysBob['privateKey'].x,keysAlice['publicKey'].p)

#Signing with Alice key
print colored("-------------------------- Signing the message ", "green") + colored(str(m),"yellow") + colored(" with Alice private key\n", "green")
signature = sign(m,keysAlice)
print colored("-------------------------- Verify with Alice public Key: ","green") + '\n'
print colored ("Result: ", "yellow") + str(verify(m,signature,keysAlice['publicKey'])) + '\n'
print colored("-------------------------- Verify with Bob public Key: ","green") + '\n'
print colored("Result: ","yellow") + str(verify(m,signature,keysBob['publicKey'])) + '\n'

raw_input("")

#Signing with alice key and then applying proxy key
print colored("-------------------------- Signing the message ", "green" ) + colored(str(m),"yellow") + colored( " with Alice private key and then applying the proxy key\n", "green")
signature = sign(m,keysAlice,proxyKey)
print colored("-------------------------- Verify with Alice public Key: ","green")+ '\n'
print colored ("Result: ", "yellow") + str(verify(m,signature,keysAlice['publicKey']))+ '\n'
print colored("-------------------------- Verify with Bob public Key: ","green") + '\n'
print colored("Result: ","yellow") + str(verify(m,signature,keysBob['publicKey'])) +'\n'
