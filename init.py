from random import *
from elgamal import *
from pwn import *
from multiprocessing import Process
import os
import sys

def t1():
    if(useProxy):
        os.system("python verifier.py " +  str(keysAlice['publicKey'].h) + " " + str(keysAlice['publicKey'].p) +" " +str(keysAlice['privateKey'].g) + " " + str(port) +" "+ str(nRound) + " " + str(keysBob['publicKey'].h))
    else:
        os.system("python verifier.py " +  str(keysAlice['publicKey'].h) + " " + str(keysAlice['publicKey'].p) +" " +str(keysAlice['privateKey'].g) + " " + str(port) +" "+ str(nRound) + " " + str(keysBob['publicKey'].h))

def t2():
    if(useProxy):
        os.system( "python prover.py " +  str(keysAlice['privateKey'].x) + " " +str(keysAlice['privateKey'].p) + " "+str(keysAlice['privateKey'].g)+ " "+ str(port) +" "+ str(nRound)+ " "+ str(proxyKey) + " " + str(keysBob['publicKey'].h))
    else:
        os.system( "python prover.py " +  str(keysAlice['privateKey'].x) + " " +str(keysAlice['privateKey'].p) + " "+str(keysAlice['privateKey'].g)+ " "+ str(port) +" "+ str(nRound))


# TODO increase number of bits

useProxy = int(sys.argv[1])
nRound = int(sys.argv[2])
if(nRound ==  1):
    print("Insert more than 1 round please.")
    exit()
nRound += 1

port = 12345
def generate_proxy_key(a,b,p):
    invb = inverse(b, p-1)
    return (a*invb)%(p-1)

keysAlice=generate_keys(32,32)
keysBob=generate_keys(32,32,keysAlice['publicKey'].p,keysAlice['publicKey'].g)

if(useProxy):
    proxyKey = generate_proxy_key(keysAlice['privateKey'].x,keysBob['privateKey'].x,keysAlice['publicKey'].p)

p = Process(target=t1, args=())
p.start()
sleep(1)
p2 = Process(target=t2, args=())

p2.start()
p2.join()
p.join()
