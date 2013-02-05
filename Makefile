# Mayank Gureja (ECE-C 353), Ayush Sobti (CS 283)
# Assignment 3 - ECE-C353 - Summer 2012
# Makefile

.PHONY : server client cracker clean

server :
	@echo "Starting Server on port 1337..."
	./serverclient.py server 1337

client :
	@echo "Starting Client on port 1337..."
	./serverclient.py client 1337

cracker :
	@echo "Launching Key Cracker..."
	./keycracker.py

clean : 
	- \rm *.pyc
