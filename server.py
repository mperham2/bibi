import socket
import sys
import parser

PORT = sys.argv[1]
PWD = sys.argv[2]


# checking PORT values (repeat of bash)
try:
    PORT = int(PORT)
except:
    sys.exit("PORT value invalid")


# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('localhost', PORT)
print >>sys.stderr, 'starting up on %s port %s' % server_address

try:
    sock.bind(server_address)
except:
    print >>sys.stderr, 'port is busy'
    sys.exit(63)

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
            program = connection.recv(1024)
            print >>sys.stderr, 'received "%s"' % program
            if program:

                # start data handling here.
                
                # parse the program
                parsed_program = parser.parse(program) # add PWD check
                print parsed_program
                
                # save the program
                             
                # output = file storage module (parsed_program)
                	#(returns json of json files for each action)
                	#(uses additional module to read existing log)
                                               	

                print >>sys.stderr, 'sending data back to the client'
                connection.sendall(str(parsed_program)) #change to output
                break
            else:
                print >>sys.stderr, 'no more data from', client_address
                break

    finally:
        # Clean up the connection
        connection.close()
        sys.exit(0)