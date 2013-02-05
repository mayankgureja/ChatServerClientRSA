#!/usr/bin/python
#
# miniRSA.py - miniRSA Library, including encrypt, decrypt and key cracking tests
#
# Mayank Gureja (ECE-C 353), Ayush Sobti (CS 283)
#
# Sun Aug 12 21:01:35 EDT 2012


import sys
import random
import fractions


def coPrime(x) :
	"""
	Finds a random co-prime of given number
	"""

	n = x*2 + 100000 # upper limit for range of random integers
	y = random.randint(x*2, n)
	if (fractions.gcd(x, y) != 1) :
		return coPrime(x)	
	else :
		return y


def mod_inverse(base, m) :
	"""
	Calculates modular multiplicate inverse
	"""
	
	g, x, y = mod_inverse_iterative(base, m)
	if (g != 1) :
		return None
	else :
#		print "Modular inverse of %0d mod %0d is %0d" % (base, m, x % m)
		return (x % m)
	

def mod_inverse_iterative(a, b) :
	"""
	Helps mod_inverse work
	"""

	x, y, u, v = 0, 1, 1, 0
	while a != 0 :
		q, r = b / a, b % a; m, n = x-u*q, y-v*q
		b, a, x, y, u, v = a, r, u, v, m, n
	return b, x, y


def modulo(a, b, c) :
	"""
	Calculates modulo
	"""

	#print "Modulo of %0d^%0d mod %0d is %0d" % (a, b, c, (int(a)**int(b)) % int(c))
	#print a,b,c;
	return ((int(a)**int(b)) % int(c))


def totient(n) :
	"""
	Calculates Euler's totient
	"""

	count = 0;
	for i in range(1, n) :
		if (fractions.gcd(n, i) == 1) :
			count = count + 1;

#	print "Euler's totient for %0d is %0d" % (n, count)
	return count;


def gen_prime() :
	"""
	Generates random prime numbers between 2 and n
	"""

	"""
	n = 100000 # 2 to n, range to choose prime numbers from

	noprimes = [j for i in range(2, 8) for j in range(i*2, n, i)]
	primes = [x for x in range(n-10000, n) if x not in noprimes]
#	print "Random prime number: %0d" % (primes[random.randint(1, len(primes)-1)])
	return (primes[random.randint(1, len(primes)-1)])
	"""
	
	n = 100
	if n == 2 : 
		return [2]
	elif n < 2 :
		return []
	s = range(3, n+1, 2)
	mroot = n ** 0.5
	half = (n+1)/2-1
	i = 0
	m = 3
	while m <= mroot:
		if s[i]:
			j = (m*m-3)/2
			s[j] = 0
			while j<half:
				s[j] = 0
				j += m
		i=i+1
		m=2*i+3
	primes = [2]+[x for x in s if x]
	return (primes[random.randint(1, len(primes)-1)])


def prime_factors(n) :
	"""
	Factorizes given prime number
	"""

        factors = []
        lastresult = n
        c = 2
        while lastresult != 1 :
                if lastresult %c == 0 and c%2 > 0 :
                        factors.append(c)
                        lastresult /= c
                        c += 1
                else :
                        c += 1
        return factors[0], factors[1]


def endecrypt(x, e, c) :
	"""
	Encrpyts/decrypts given ASCII character value, via the RSA crypto algorithm
	"""

	return modulo(x, e, c)


def decode(x) :
	"""
	Decodes given ASCII character value into ASCII character
	"""

	try :
		#print "Decoded string is %0s" % str(unichr(x))
		# return str(x);
		return str(unichr(x))
	except ValueError :
		print "** ERROR - Decoded character is unrecognized **"


def key_cracker(e, c) :
	"""
	RSA Key Cracker
	"""

	print "Public Key: (%0d, %0d)" % (e, c)
	a, b = prime_factors(c)
	print "[a, b] : [%0d, %0d]" % (a, b)
	m = (a-1)*(b-1)
	print "Totient: %0d" % (totient(m))
	d = mod_inverse(e, m)
	#print "d : %0d" % d
	return d
 	#x = int(raw_input("\nEnter number to decrypt\n"))
	#decode(endecrypt(x, d, c))


def keygen() :
	"""
	Generates random RSA keys
	"""

	a = gen_prime()
	b = gen_prime()
	if a == b :
		keygen()
	
#	print "a is %0d" % a
#	print "b is %0d" % b


	c = a*b
#	print "c is %0d" % c

	m = (a-1)*(b-1)
#	print "m is %0d" % m

	e = coPrime(m)
#	print "e is %0d" % e

	d = mod_inverse(e, m)
#	print "d is %0d" % d

	print "Public Key: (%0d, %0d)" % (e, c)
	#print "private key: (%0d, %0d)" % (d, c)

	## ONLY FOR TESTING ##
	return (e, d, c)


def test_helpers() : 
	"""
	Test function for utility functions
	"""

	print "GCD of 8 and 12 is %0d" % fractions.gcd(8,12)

	print "%0d and %0d are co-prime" % (2, coPrime(2))
	print "%0d and %0d are co-prime" % (6, coPrime(6))

	mod_inverse(11, 60)

	modulo(2, 3, 4)

	totient(24)


#def test_encryption() :
def test_encryption(e, c) : # ONLY FOR TESTING ##
	"""
	Test function for encryption
	"""

#	e = int(raw_input("\nEnter e from public key\n"))
#	c = int(raw_input("\nEnter c from public key\n"))

	string = raw_input("\nEnter word to encrpyt\n")
	for i in range(0, len(string)) :
		print endecrypt(ord(string[i]), e, c)


#def test_encryption() :
def test_decryption(d, c) : # ONLY FOR TESTING ##
	"""
	Test function for decryption
	"""

#	d = int(raw_input("\nEnter d from public key\n"))
#	c = int(raw_input("\nEnter c from public key\n"))

	x = int(raw_input("\nEnter number to decrypt\n"))
	decode(endecrypt(x, d, c))


def test_endecrypt() :
	"""
	Runs all cryptographic method tests
	"""

	e, d, c = keygen()

	test_encryption(e, c)
	test_decryption(d, c)
	key_cracker(e, c)


def main() :
	"""
	Main
	"""

#	test_helpers()
	test_endecrypt()



# Execution begins
#main()


