#!/usr/bin/python
#
# keycracker.py - Key Cracker testing
#
# Mayank Gureja (ECE-C 353), Ayush Sobti (CS 283)
#
# Sun Aug 19 19:57:35 EDT 2012


import sys
import miniRSA


def decrypt(message, e, c) :
	"""
	Method to decrypt incoming message using given public keys
	"""

	words = message.split(",");
	decrypted_data = "";
	for i in range(0, len(words)-1) :
		decrypted_data += str(miniRSA.decode(miniRSA.endecrypt(words[i], e, c)))
	return decrypted_data

	
def test_example() :
	"""
	Automated text example for key cracking
	"""

	e, c = 277, 737

	d = miniRSA.key_cracker(e, c)
	print "\n** Private key: (%0d, %0d) **\n" % (d, c)

	message = "37,635,418,54"
	print "Message to decrypt: %s\n" % message

	print "Decrypted message:"
	print decrypt(message, e, c)


def test_keycracker() :
	"""
	Uses user input to test key cracking
	"""

	e = int(raw_input("\nEnter e from public key to crack: "))
	c = int(raw_input("Enter c from public key to crack: "))

	d = miniRSA.key_cracker(e, c)
	print "\n** Private key: (%0d, %0d) **\n" % (d, c)

	message = str(raw_input("Enter message to crack (no spaces): "))

	print "Decrypted message:"
	print decrypt(message, e, c)


def main() :
	"""
	Main
	"""

	while(1) :
		print "\n***** MAIN MENU *****"
		print "1. Test Key Cracker with coded example"
		print "2. Test Key Cracker with your own example"
		print "0. Exit"
		print "***********************"

		option = int(raw_input("Your option: "))

		if option == 1 :
			test_example()
		elif option == 2 :
			test_keycracker()
		elif option == 0 :
			print "Quiting..."
			sys.exit(0)
		else :
			raw_input("\n* ERROR - Input is NOT recognized *\nPress Enter to continue")


# Execution begins
main()


