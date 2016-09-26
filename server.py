import socket
import sys

PORT = sys.argv[1]
PWD = sys.argv[2]


# checking PORT values (repeat of bash)
try:
    PORT = int(PORT)
except:
    sys.exit("PORT value invalid")

print type(PORT)

if PORT > 1023:
    if PORT < 65536:
        pass
    else:
        sys.exit("PORT out of bounds")
else:
    sys.exit("PORT out of bounds")

# check password




print PORT, PWD

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('localhost', PORT)
print >>sys.stderr, 'starting up on %s port %s' % server_address
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

while True:
    # Wait for a connection
    print >>sys.stderr, 'waiting for a connection'
    connection, client_address = sock.accept()

    try:
        print >>sys.stderr, 'connection from', client_address

        # Receive the data in small chunks and retransmit it
        while True:
            data = connection.recv(1024)
            print >>sys.stderr, 'received "%s"' % data
            if data:

                # start data handling here.


                print >>sys.stderr, 'sending data back to the client'
                connection.sendall(data)
            else:
                print >>sys.stderr, 'no more data from', client_address
                break

    finally:
        # Clean up the connection
        connection.close()