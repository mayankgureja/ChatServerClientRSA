ChatServerClientRSA
===================

A Chat Server/Client with built-in RSA encryption written in Python

How To Run
----------

Use the provided Makefile

Description
------------

This is a Chat Server/Client with built-in RSA encryption written in Python. This program uses p2p (peer-to-peer) and not full duplex connecions.

serverclient.py contains the classes and methods that set up the chat server as well as a client. The server begins by creating a socket and listening for incoming connections. The client receives a port and connects to the server on localhost using that port. As soon as the connection is established, the server and client exchange Public Keys. Both the client and server spawn two threads each. One responsible for reading messages from stdin and sending to the conversation partner, and the other to accept messages from the partner and printing to stdout. serverclient.py imports miniRSA and encrypts all outgoing traffic and decrypts all incoming traffic. When a message 'EXIT' is received, the connection is closed. At this point, the server also shuts down the server.

miniRSA.py contains all the methods necessary to implement RSA encryption and cryptography to the Chat Server program as described in serverclient.py above. The library contains helper methods, methods for encryption, decryption and key cracking and some tester methods (these have been commented out). It should be noted that keeping performance in mind, and the need for a Chat program to seem like real-time communication, the range of prime numbers used for encryption had to kept at a maximum of 100. Anything more than that takes some time to decrypt and that made the program noticeably slower. That behavior was found to be unacceptable and decided to reduce the size of the cryptographic keys. However, increasing this is a simple matter of increasing variable 'n' in the gen_prime() method.

keycracker.py is the Key Cracker program. This program has a menu from which the user can either run an example cracking sequence or enter their own data for cracking purposes. The program takes in the Public Key of the target and then cracks the Private Key. After that, the user can enter the received encrypted message (a list of comma-separated integers) and the Key Cracker will decrypt it.

Collaborators
-------------

Built in collaboration with xbonez (http://github.com/xbonez)

