from random import *
from elgamal import *
from math import *
import sys
from pwn import *
from termcolor import *

width = 300
p = int(sys.argv[2])
g = int(sys.argv[3])
ga = int(sys.argv[1])
port = int(sys.argv[4])
nRound = int(sys.argv[5])
gb = int(sys.argv[6])
Alice = 0
Bob = 0
l = listen(int(port))
for i in range(1,nRound):
    s1str = l.recvline()
    s1 = int(s1str)
    b = random.randint( 0, 1 )
    print (str(b) + colored(" <-- sending randomly choosen b","cyan")).rjust(width)
    l.sendline(str(b))
    s2str = l.recvline()
    s2 = int(s2str)
    resA=0
    resB=0
    if(b == 1):
      resB = modexp(gb, s2, p)
      resA = modexp(ga, s2, p)
    else:
       resA=resB = modexp(g, s2, p)

    print (colored("Output of identification for Bob ","yellow") + str(resB)).rjust(width)
    print (colored("Output of identification for Alice ","yellow") + str(resA)).rjust(width)
    identificated = 0
    if resA == s1 and resB == s1:
        print colored("Prover knows random number k", "yellow").rjust(width)
    else:
        if resA == s1:
            print colored("Alice identificated", "yellow").rjust(width)
            identificated = 1
            Alice = 1
        if resB == s1:
            print colored("Bob identificated", "yellow").rjust(width)
            identificated = 1
            Bob = 1
        if identificated == 0:
            print colored("Error during identification", "yellow").rjust(width)
            exit()

if Bob == 1 and Alice == 0:
    print '\033[1m' + colored("Bob completely identificated", "yellow").rjust(width)
elif Bob == 0 and Alice == 1:
    print '\033[1m' + colored("Alice completely identificated", "yellow").rjust(width)
else:
    print '\033[1m' + colored("No one identificated, please use more rounds", "yellow").rjust(width)
