#! /usr/bin/python
#
# serverclient.py - 2-way Chat Server with RSA encryption
#
# Ayush Sobti (CS 283), Mayank Gureja (ECE-C 353)
#
# Sun Aug 19 18:35:39 EDT 2012


import sys
import os
import socket
import SocketServer
import threading
import miniRSA


def main():
    """
    Main - Checks for correct input arguments and runs the appropriate methods
    """

    if (len(sys.argv) < 3):
        print 'Usage: python serverclient.py <server|client> <port>\n'
        return -1
    else:
        if sys.argv[1].lower() == 'server':
            Server(sys.argv[2])
        elif sys.argv[1].lower() == 'client':
            Client(sys.argv[2])
        else:
            print 'Unrecognized argument: ', sys.argv[1]
            return -1
    return 0


def Server(port):
    """
    Creates the server instance, sets it up
    """
    host = 'localhost'
    port = int(port)

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)

    # blocking call to accept()
    print 'Waiting for partner to join conversation...\n'
    (conn, client_addr) = server.accept()
    print 'Client connected: ', client_addr[0]

    # wait to receive client's public key
    key = conn.recv(1024)
    key = key.split(',')
    keyTuple = (key[0], key[1])
    print 'Client\'s Public Key received'

    e, d, c = miniRSA.keygen()
    sendPublic = str(d) + ',' + str(c)
    conn.send(sendPublic)
    print 'Public Key sent'

    privateTuple = (e, c)

    print 'Type your message below and hit enter to send. Type \'EXIT\' to end conversation.\n'

    ReadThread = Thread_Manager('read', conn, keyTuple, None)
    WriteThread = Thread_Manager('write', conn, None, privateTuple)

    ReadThread.start()
    WriteThread.start()

    # wait until client dc's
    ReadThread.join()
    print 'Your partner has left the conversation. Press any key to continue...\n'

    # stop the write thread
    WriteThread.stopWrite()
    WriteThread.join()

    # shut down client connection
    try:
        conn.shutdown(socket.SHUT_RDWR)
        conn.close()
    except:
        # connection already closed
        pass

    # shut down server
    print 'Shutting server down...'
    server.shutdown(socket.SHUT_RDWR)
    server.close()

    return 0


def Client(port):
    """
    Creates the client instance, sets up the client
    """

    host = 'localhost'
    port = int(port)

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))

    e, d, c = miniRSA.keygen()
    sendPublic = str(d) + "," + str(c)
    client.send(sendPublic)
    print 'Public key sent'

    key = client.recv(1024)
    key = key.split(',')
    keyTuple = (key[0], key[1])
    print 'Server\'s Public Key received'

    privateTuple = (e, c)

    print 'Connected to chat. Type your messages below and hit enter to send. Send \'EXIT\' to leave the conversation.\n'

    ReadThread = Thread_Manager('read', client, keyTuple, None)
    WriteThread = Thread_Manager('write', client, None, privateTuple)

    ReadThread.start()
    WriteThread.start()

    ReadThread.join()
    print 'Your partner has left the conversation. Press any key to continue...\n'

    # stop the write thread
    WriteThread.stopWrite()
    WriteThread.join()

    # shut down client connection
    try:
        client.shutdown(socket.SHUT_RDWR)
        client.close()
    except:
        # connection already killed
        pass


class Thread_Manager(threading.Thread):
    """
    Creates threads for asynchronoues reading and writing
    """

    def __init__(self, action, conn, public, private):
        """
        Constructor for Thread_Manager class
        """

        threading.Thread.__init__(self)
        self.action = action.lower()
        self.conn = conn
        self.dowrite = True
        self.exitcode = 'EXIT'

        if public is not None:
            self.setPublic(public)
        if private is not None:
            self.setPrivate(private)

    def run(self):
        """
        Invoked when new thread is executed
        """

        if (self.action == 'read'):
            self.read()
        else:
            self.write()

    def setPublic(self, public):
        """
        Sets public key from other party for decryption
        """

        self.public = public

    def setPrivate(self, private):
        """
        Sets private key for encryption
        """

        self.private = private

    def stopWrite(self):
        """
        Terminates the write loop
        """

        self.dowrite = False

    def decrypt(self, buff):
        """
        Decrypts input integer list into sentences
        """

        words = buff.split(",")
        decrypted_data = ""
        # print words;
        # sys.exit();
        for i in range(0, len(words) - 1):
            decrypted_data += str(miniRSA.decode(miniRSA.endecrypt(words[i], self.public[0], self.public[1])))
        return decrypted_data

    def read(self):
        """
        Responsible for reading in data from the client and displaying stdout
        """

        buff = self.conn.recv(1024)
        buff = self.decrypt(buff)
        while buff.strip() != self.exitcode and len(buff) > 0:
            print 'Message received: ', buff.strip()
            buff = self.conn.recv(1024)
            buff = self.decrypt(buff)
        # client disconnected
        self.stopWrite

    def encrypt(self, data):
        encrypted_data = ""
        for i in range(0, len(data)):
            encrypted_data += str(miniRSA.endecrypt(ord(data[i]), self.private[0], self.private[1])) + ","
        return encrypted_data

    def write(self):
        """
        Responsible for reading in data from stdin and sending to client
        """

        while self.dowrite:
            data = sys.stdin.readline()
            data = self.encrypt(data)
            self.conn.send(data)

            if (data.strip() == self.exitcode):
                self.conn.shutdown(socket.SHUT_RDWR)
                self.conn.close()
                self.dowrite = False

# Entry point
if __name__ == "__main__":
    sys.exit(main())
