# Atomic Proxy Cryptography PoC

Big Data Security project on Atomic Proxy Cryptography.

## Team members
- Lorenzo Alluminio
- Giulia Clerici
- Fulvio Di Girolamo
- Raffaele Stelluti
- Edoardo Giordano

**THIS IS ONLY FOR DEMO PURPOSES!**

## ENCRYPTION

```
python encryption.py <message>
```

## SIGNATURE

```
python encryption.py <messageInteger>
```


## IDENTIFICATION

This init script executes the identification protocol implemented in the scripts verifier.py and prover.py

```
python init.py <useProxyKey> <numberOfrounds>
```

### PROVER

Prover side of the identification

without proxy key:
```
python prover.py <privateKey> <modulus> <generator> <port> <numberOfRounds>
```

with proxy key:
```
python prover.py <privateKey> <modulus> <generator> <port> <numberOfRounds> <proxyKey> <publicKeyOfOtherParty>
```
### VERIFIER

Verifier side of the identification

```
python prover.py <publicKey> <modulus> <generator> <port> <numberOfRounds> <publicKeyOfOtherParty>
```



