from random import *
from elgamal import *
from math import *
from hashlib import *
from struct import *
from termcolor import *

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
    print colored("s1 --> ", "red") + str(s1)
    print colored("generated hash --> ", "red") + hash
    bits = []
    for i in range(0,l):
        bits.append(unpack("<B",hash[i])[0]%2)

    print colored("extracted bits --> ", "red") + str(bits)

    s2 = []
    for i in range(0,l):
        #TODO potential timing attack
        inva = inverse(a, p-1)
        if bits[i] == 1:
            s2.append((k[i]-m)*inva)
        else:
            s2.append(k[i]*inva)

    if proxyKey != None:
        print colored("using proxy key " + str(proxyKey) + " to rencode s2\n","red") + str(s2)
        for i in range(0,l):
                s2[i] = s2[i]*proxyKey;
        print colored("Transformed message:\n","red") + str(s2)
    else:
        print colored("s2 --> ", "red") + str(s2)
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

    print colored("generated hash --> ", "red") + hash
    bits = []
    for i in range(0,l):
        bits.append(unpack("<B",hash[i])[0]%2)

    print colored("extracted bits --> ", "red") + str(bits)

    for i in range(0,l):
        inv = inverse(modexp(g, m*bits[i], p), p)
        if modexp(ga,s2[i],p) != ((s1[i]*inv) % p):
            return False

    return True

#Data shared among different rounds
keysAlice=generate_keys(32,32)
keysBob=generate_keys(32,32,keysAlice['publicKey'].p,keysAlice['publicKey'].g) # we need to pass Alice's p and g because they have to be shared in orther to create a valid proxy key
m= int(sys.argv[1])
proxyKey = generate_proxy_key(keysAlice['privateKey'].x,keysBob['privateKey'].x,keysAlice['publicKey'].p)

#Signing with Alice key
print colored("Signing the message " + str(m) +" with Alice private key", "green")
signature = sign(m,keysAlice)
print colored("Verify with Alice publickKey: ","green")
print colored ("Result: ", "red") + str(verify(m,signature,keysAlice['publicKey']))
print colored("Verify with Bob publickKey: ","green")
print colored("Result: ","red") + str(verify(m,signature,keysBob['publicKey']))


#Signing with alice key and then applying proxy key
print colored("Signing the message " + str(m) + " with Alice private key and then applying the proxy key", "green")
signature = sign(m,keysAlice,proxyKey)
print colored("Verify with Alice publickKey: ","green")
print colored ("Result: ", "red") + str(verify(m,signature,keysAlice['publicKey']))
print colored("Verify with Bob publickKey: ","green")
print colored("Result: ","red") + str(verify(m,signature,keysBob['publicKey']))
