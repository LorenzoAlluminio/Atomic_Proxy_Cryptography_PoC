from random import *
from elgamal import *
from math import *
from hashlib import *
from struct import *

def egcd(a, b):
    """Extended gcd of a and b. Returns (d, x, y) such that
    d = a*x + b*y where d is the greatest common divisor of a and b."""
    x0, x1, y0, y1 = 1, 0, 0, 1
    while b != 0:
        q, a, b = a // b, b, a % b
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
    return a, x0, y0

def inverse(a, n):
    """Returns the inverse x of a mod n, i.e. x*a = 1 mod n. Raises a
    ZeroDivisionError if gcd(a,n) != 1."""
    d, a_inv, n_inv = egcd(a, n)
    if d != 1:
        raise ZeroDivisionError('{} is not coprime to {}'.format(a, n))
    else:
        return a_inv % n

#TODO increase l
l = 10

def sign(m,keys):
    a = keys['privateKey'].x
    p=keys['publicKey'].p
    g=keys['publicKey'].g
    h = sha256()
    k = []
    s1 = []
    for i in range(0,l):
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
    for i in range(0,l):
        #TODO potential timing attack
        inva = inverse(a, p-1)
        if bits[i] == 1:
            s2.append((k[i]-m)*inva)
        else:
            s2.append(k[i]*inva)

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

keys=generate_keys(32,32)
m = 1001
signature = sign(m,keys)
#signature[0][1] = 100
print verify(m,signature,keys['publicKey'])
