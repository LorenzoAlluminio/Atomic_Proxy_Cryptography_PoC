from pwn import *
import sys

a=sys.argv[1]
p=sys.argv[2]
qq=p-1
g=sys.argv[3]
port=sys.argv[4]
nRound=sys.argv[5]

io = remote('localhost', port)

for i in range(1,nRound)
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
    if b=='0':
        s2 = k
    else:
        inva = inverse(a, p-1)
        s2 = (k*inva) % (p-1)
    print "sending s2 --> " + str(s2)
    io.sendline(str(s2))
