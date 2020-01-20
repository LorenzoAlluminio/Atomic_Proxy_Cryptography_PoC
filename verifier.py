from random import *
from elgamal import *
from math import *
import sys
from pwn import *

p = int(sys.argv[2])
g = int(sys.argv[3])
ga = int(sys.argv[1])
print ga
port = int(sys.argv[4])
print port
nRound = int(sys.argv[5])

if(len(sys.argv) > 6):
    gb = int(sys.argv[7])
    proxyKey = int(sys.argv[6])
l = listen(int(port))
for i in range(1,nRound):
    s1str = l.recvline()
    s1 = int(s1str)
    print s1str
    b = random.randint( 0, 1 )
    print b
    l.sendline(str(b))
    s2str = l.recvline()
    s2 = int(s2str)
    if(len(sys.argv) > 6):
        if(b == 1):
           s2 = (s2*proxyKey)%(p-1)
           print "new s2 --> " + str(s2)
           res = modexp(gb, s2, p)
        else:
           res = modexp(g, s2, p)
    else:
        if(b == 1):
            res = modexp(ga, s2, p)
        else:
            res = modexp(g, s2, p)
    print res
    print s1
    print s2
    if res == s1:
        if(len(sys.argv) > 6):
            print "Bob identificated"
        else:
            print "Alice identificated"
    else:
        print "ERROR"
