"""
  A trivial web server in Python. 

  Based largely on https://docs.python.org/3.4/howto/sockets.html
  This trivial implementation is not robust:  We have omitted decent
  error handling and many other things to keep the illustration as simple
  as possible. 

  FIXME:
  Currently this program always serves an ascii graphic of a cat.
  Change it to serve files if they end with .html or .css, and are
  located in ./pages  (where '.' is the directory from which this
  program is run).  
"""

import CONFIG    # Configuration options. Create by editing CONFIG.base.py
import argparse  # Command line options (may override some configuration options)
import socket    # Basic TCP/IP communication on the internet
import _thread   # Response computation runs concurrently with main program
import os.path   # Used to check if requested file exists on server.


def listen(portnum):
    """
    Create and listen to a server socket.
    Args:
       portnum: Integer in range 1024-65535; temporary use ports
           should be in range 49152-65535.
    Returns:
       A server socket, unless connection fails (e.g., because
       the port is already in use).
    """
    # Internet, streaming socket
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Bind to port and make accessible from anywhere that has our IP address
    serversocket.bind(('', portnum))
    serversocket.listen(1)    # A real server would have multiple listeners
    return serversocket

def serve(sock, func):
    """
    Respond to connections on sock.
    Args:
       sock:  A server socket, already listening on some port.
       func:  a function that takes a client socket and does something with it
    Returns: nothing
    Effects:
        For each connection, func is called on a client socket connected
        to the connected client, running concurrently in its own thread.
    """
    while True:
        print("Attempting to accept a connection on {}".format(sock))
        (clientsocket, address) = sock.accept()
        _thread.start_new_thread(func, (clientsocket,))


##
## Starter version only serves cat pictures. In fact, only a
## particular cat picture.  This one.
##
CAT = """
     ^ ^
   =(   )=
"""

## HTTP response codes, as the strings we will actually send. 
##   See:  https://en.wikipedia.org/wiki/List_of_HTTP_status_codes
##   or    http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html
## 
STATUS_OK = "HTTP/1.0 200 OK\n\n"
STATUS_FORBIDDEN = "HTTP/1.0 403 Forbidden\n\n"
STATUS_NOT_FOUND = "HTTP/1.0 404 Not Found\n\n"
STATUS_NOT_IMPLEMENTED = "HTTP/1.0 401 Not Implemented\n\n"
FORBIDDEN_REQUESTS = ["//","~",".."]

def respond(sock):
    """
    This server responds only to GET requests (not PUT, POST, or UPDATE).
    Any valid GET request is answered with an ascii graphic of a cat. 
    """
    sent = 0
    request = sock.recv(1024)  # We accept only short requests
    request = str(request, encoding='utf-8', errors='strict')
    print("\nRequest was {}\n".format(request))

    parts = request.split()
    if len(parts) > 1 and parts[0] == "GET":
        options = get_options()
        path = options.directory
        request = parts[1]

        print("pre request: {}\n".format(request))
        print("path: {}\n".format(path))
        print("request substr: {}\n".format(request[:len(path)]))

        """
        If the request isn't for files within the default directory add the default
        path to the beggining of the request.
        """
        if request[:len(path)] != path: 
            request = path+request

        print("post request: {}\n".format(request))

        reply_status = parseStatus(request)
        print("reply_status dump: {}\n".format(reply_status))
        transmit(reply_status, sock)
        if reply_status == STATUS_OK:
            transmit(readFile(request), sock)
    else:
        transmit(STATUS_NOT_IMPLEMENTED, sock)        
        transmit("\nI don't handle this request: {}\n".format(request), sock)

    sock.close()
    return

def parseStatus(request):
    """
    A proper GET request has been received, building response to the request 
    returns string containing the propper http response status.
    """
    for forbbiden in FORBIDDEN_REQUESTS:
        if forbbiden in request:
            return STATUS_FORBIDDEN

    """
    After this point the http request is formatted correctly and not mallicous.
    Will attempt to locate the requested file and deliver it.
    """
    if os.path.isfile(request):
        return STATUS_OK
    else:
        return STATUS_NOT_FOUND

def readFile(request):
    """
    Read the reqested file to be sent to the requestor.
    """
    reply = CAT
    return reply


def transmit(msg, sock):
    """It might take several sends to get the whole message out"""
    sent = 0
    while sent < len(msg):
        buff = bytes( msg[sent: ], encoding="utf-8")
        sent += sock.send( buff )
    

###
#
# Run from command line
#
###

def get_options():
    """
    Options from command line or configuration file.
    Returns namespace object with option value for port
    """
    parser = argparse.ArgumentParser(description="Run trivial web server.")
    parser.add_argument("--port", "-p",  dest="port", 
                        help="Port to listen on; default is {}".format(CONFIG.PORT),
                        type=int, default=CONFIG.PORT)
    """
    Added argument for passing a root directory that files 
    to serve are located within. I did this to remove the
    hardcoded path and because I'm new to python so I felt
    it worth the learning experience to try and create my 
    own argument.
    """
    parser.add_argument("--dir","-d",  dest="directory",
                        help="Root directory that pages are located in; default is {}".format(CONFIG.PAGES_PATH),
                        type=str, default=CONFIG.PAGES_PATH)

    options = parser.parse_args()
    if options.port <= 1000:
        print("Warning: Ports 0..1000 are reserved by the operating system")
    return options
    

def main():
    options = get_options()
    port = options.port
    sock = listen(port)
    print("Listening on port {}".format(port))
    print("Socket is {}".format(sock))
    serve(sock, respond)

main()
    
