import select
import socket
import sys
import time
import requests

class Poller:
    """ Polling server """
    def __init__(self,port):
        self.host = ""
        self.port = port
        self.open_socket()
        self.clients = {}
        self.size = 1024
        self.methods = ['HEAD', 'POST', 'PUT', 'DELETE', 'TRACE', 'CONNECT']
        self.media = {}
        self.hosts = {}
        self.timeout = 0
        f = open('web.conf', 'r')
        cf = f.readlines()
        for line in cf:
            e = line.split(' ')
            if e[0] == 'host':
                self.hosts[e[1]] = e[2].rstrip()
            if e[0] == 'media':
                self.media[e[1]] = e[2]

    def open_socket(self):
        """ Setup the socket for incoming clients """
        try:
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
            self.server.bind((self.host,self.port))
            self.server.listen(5)
        except socket.error, (value,message):
            if self.server:
                self.server.close()
            print "Could not open socket: " + message
            sys.exit(1)

    def run(self):
        """ Use poll() to handle each incoming client."""
        self.poller = select.epoll()
        self.pollmask = select.EPOLLIN | select.EPOLLHUP | select.EPOLLERR
        self.poller.register(self.server,self.pollmask)
        while True:
            # poll sockets
            try:
                fds = self.poller.poll(timeout=1)
            except:
                return
            for (fd,event) in fds:
                # handle errors
                if event & (select.POLLHUP | select.POLLERR):
                    self.handleError(fd)
                    continue
                # handle the server socket
                if fd == self.server.fileno():
                    self.handleServer()
                    continue
                # handle client socket
                result = self.handleClient(fd)

    def handleError(self,fd):
        self.poller.unregister(fd)
        if fd == self.server.fileno():
            # recreate server socket
            self.server.close()
            self.open_socket()
            self.poller.register(self.server,self.pollmask)
        else:
            # close the socket
            self.clients[fd].close()
            del self.clients[fd]

    def handleServer(self):
        (client,address) = self.server.accept()
        self.clients[client.fileno()] = client
        self.poller.register(client.fileno(),self.pollmask)

    # Server stuff
    def handleClient(self,fd):
        response = ''
        data = self.clients[fd].recv(self.size)
        if data:
            request = data
            request = request.split('\r\n')
            method = request[0].split(' ')
            host = requests.get_host(request[1])
            if method[0] == 'GET':
                response = requests.get_request(method[1], self.hosts[host],self.media)
            elif method[0] not in self.methods:
                response = requests.bad_request()
            elif method[0] in self.methods:
                response = requests.not_implemented()
            else:
                response = request.serv_error()
            
            self.clients[fd].send(response)
        else:
            self.poller.unregister(fd)
            self.clients[fd].close()
            del self.clients[fd]
