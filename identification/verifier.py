from random import *
from elgamal import *
from math import *



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

#TODO give a seed to random gen

def round(i,keys):
    print "---------- ROUND " + str(i)
    a = keys['privateKey'].x
    ga = keys['publicKey'].h
    qq=keys['publicKey'].p - 1
    p=qq+1
    g=keys['publicKey'].g
    print "Generator --> " + str(g)
    print "p --> " + str(p)
    while True:
        k = randint(1, qq)
        if gcd(k, qq)==1:
                       break
    print "Random k --> " + str(k)
    s1=modexp(g, k, p)
    print "s1 --> " + str(s1)
    b = raw_input("insert 0 or 1: ")
    print "chosen b = " + str(b)
    if str(b)=='0':
        s2 = k
        res = modexp(g, s2, p)
    else:
        inva = inverse(a, p-1)
        s2 = (k*inva) % (p-1)
        res = modexp(ga, s2, p)
    print "s2 --> " + str(s2)
    print "res --> " + str(res)
    if res == s1:
        print "Alice identificathed"
        return [b,s1,s2]
    else:
        print "ERROR"

def generate_proxy_key(a,b,p):
    invb = inverse(b, p-1)
    return (a*invb)

import sys
from pwn import *
p = int(sys.argv[2])
g = int(sys.argv[3])
ga = int(sys.argv[1])
nRound = int(sys.argv[5])
port = int(sys.argv[4])

if(len(sys.argv) > 6):
    gb = int(sys.argv[7])     
    proxyKey = int(sys.argv[6])
l = listen(int(port))
for i in range(1,nRound):
    s1str = p.recvline()
    s1 = int(s1str)
    print s1str
    b = random.randint( 0, 1 )
    print b
    p.sendline(str(b))
    s2str = p.recvline()
    s2 = int(s2str)
    if(proxyKey):
        s2 = s2*proxyKey    
    if(b == 1):
        res = modexp(ga, s2, p)
    else:
        res = modexp(g, s2, p)
    
    if res == s1:
        print "Alice identificathed"
    else:
        print "ERROR"

