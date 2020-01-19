from pwn import *
from elgamal import *
import sys


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
a=int(sys.argv[1])
p=int(sys.argv[2])
qq=p-1
g=int(sys.argv[3])
port=int(sys.argv[4])
nRound=int(sys.argv[5])

io = remote('localhost', port)
print "im live"
for i in range(1,nRound):
    print "---------- ROUND " + str(i)
    print "Generator g --> " + str(g)
    print "Modulus p --> " + str(p)
    while True:
        k = randint(1, qq)
        if gcd(k, qq)==1:
                       break
    print "Random k --> " + str(k)
    s1=modexp(g, k, p)
    print "sending s1 --> " + str(s1)
    io.sendline(str(s1))
    b = io.recvline()
    print "received b --> " + b
    if int(b)==0:
        s2 = k
    else:
        inva = inverse(a, p-1)
        s2 = (k*inva) % (p-1)
    print "sending s2 --> " + str(s2)
    io.sendline(str(s2))
