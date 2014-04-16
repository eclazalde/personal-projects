import select
import socket
import sys
import time
import requests
import errno
import traceback

class Poller:
    """ Polling server """
    def __init__(self,port):
        self.host = ""
        self.port = port
        self.open_socket()
        self.clients = {}
        self.size = 10000
        
        self.methods = ['HEAD', 'POST', 'PUT', 'DELETE', 'TRACE', 'CONNECT']
        self.fdtime = {}
        self.t_old = time.time()
        self.client_data = {}
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
            if e[0] == 'parameter':
                self.timeout = e[2]
        print 'Mega-Awesome server running...'

    def open_socket(self):
        """ Setup the socket for incoming clients """
        try:
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
            self.server.bind((self.host,self.port))
            self.server.listen(5)
            self.server.setblocking(0)
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
                t_current = time.time()
                if (t_current - self.t_old) > float(self.timeout):
                    self.cleanup(t_current)
                    self.t_old = time.time()
            except:
                print traceback.format_exc()
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
            del self.client_data[fd]

    def handleServer(self):
        # accept as many clients as possible
        while True:
            try:
                (client,address) = self.server.accept()
                self.fdtime[client.fileno()] = time.time()
            except socket.error, (value, message):
                # if socket clock because no clients are available,
                # then return
                if value == errno.EAGAIN or errno.EWOULDBLOCK:
                    return
                print traceback.format_exc()
                sys.exit()
            # set client socket to be non blocking
            client.setblocking(0)
            self.clients[client.fileno()] = client
            self.poller.register(client.fileno(), self.pollmask)

    # Server stuff
    def handleClient(self,fd):
        try:
            data = self.clients[fd].recv(self.size)
        except socket.error, (value, message):
            # if no data is available, move on to another client
            if value == errno.EAGAIN or errno.EWOULDBLOCK:
                return
            print traceback.format_exc()
            sys.exit()
        
        if fd not in self.client_data:
            self.client_data[fd] = ''
        if len(data) == 0:
            self.c_close(fd, 'empty string recv')
            return
        self.client_data[fd] += data
            
        response = ''
        if len(self.client_data[fd]) > 0:
            request = self.client_data[fd]
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
                return
            total_sent = 0
            while total_sent < len(response):
                try:   
                    sent = self.clients[fd].send(response[total_sent:])
                except socket.error, (value, message):
                    if value == errno.EAGAIN or errno.EWOULDBLOCK:
                        continue
                    else:
                        self.c_close(fd, 'send')
                        return
                total_sent += sent
            del self.client_data[fd]
            self.fdtime[fd] = time.time()
        else:
            self.c_close(fd, 'else')
            
    def cleanup(self, t):
        #print 'cleaning...'
        trash = []
        for fd in self.fdtime:
            if (t - self.fdtime[fd]) > float(self.timeout):
                trash.append(fd)
                self.c_close(fd, 'cleanup')
        for item in trash:
            del self.fdtime[item]
        #print ('cleaned %s') % len(trash)
    
    def c_close(self, fd, where):
        #print ('closed %s from %s') % (fd, where)
        self.poller.unregister(fd)
        if fd in self.client_data:
            del self.client_data[fd]   
        if fd in self.clients:
            self.clients[fd].close()     
            del self.clients[fd]