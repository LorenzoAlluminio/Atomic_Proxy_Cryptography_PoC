from random import *
from elgamal import *
import os
# TODO increase number of bits
keys=generate_keys(32,32)

nRound = 10
port = 1234

keys2=generate_keys(32,32)
os.system("python verifier.py " +  str(keys2['publicKey'].h) + " " + str(keys2['publicKey'].p) +" " str(keys2['privateKey'].g) + str(port) +" "+ str(nRound))
os.system("python proover.py " +  str(keys2['privateKey'].x) + " " +str(keys2['privateKey'].p) + " "+str(keys2['privateKey'].g)+ " "+ str(port) +" "+ str(nRound))

