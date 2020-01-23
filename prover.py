from pwn import *
from elgamal import *
import sys
import time
from termcolor import *

a=int(sys.argv[1])
p=int(sys.argv[2])
qq=p-1
g=int(sys.argv[3])
port=int(sys.argv[4])
nRound=int(sys.argv[5])

io = remote('localhost', port)
time.sleep(1)
print colored("Public Parameters " , "green").rjust(50) + '\n'
print colored("Generator g ","cyan") + str(g)
print colored("Modulus p ","cyan") + str(p)

if(len(sys.argv) > 6):
    gb = int(sys.argv[7])
    proxyKey = int(sys.argv[6])
    print colored("Proxy key ","cyan") + str(proxyKey) +'\n'
else:
    print '\n'


for i in range(1,nRound):

    print colored("ROUND " + str(i), "green").rjust(50) + '\n'

    while True:
        k = randint(1, qq)
        if gcd(k, qq)==1:
           break
    print colored("Randomly generated k ", "cyan") + str(k)
    s1=modexp(g, k, p)
    print colored("sending s1 --> ", "cyan") + str(s1)
    io.sendline(str(s1))
    b = io.recvline()
    if int(b)==0:
        s2 = k
    else:
        inva = inverse(a, p-1)
        s2 = (k*inva) % (p-1)
        if(len(sys.argv) > 6):
            s2 = (s2*proxyKey)%(p-1)
    print colored("sending s2 --> ", "cyan") + str(s2)
    io.sendline(str(s2))
    time.sleep(1)
