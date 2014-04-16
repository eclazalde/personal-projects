import time
import os.path

def get_request(r_file, host, media):
    date_time = time.strftime("%a, %d %b %Y %H:%M:%S GMT", time.gmtime())
    if(r_file == '/'):
        m_file = open(host + '/index.html', 'r').readlines()
        html = ''
        for line in m_file:
            html += line
        response = 'HTTP/1.1 200 OK\r\n'
        response += 'Date: %s\r\n' % (date_time)
        response += 'Server: Mega-Awesome/1.0\r\n'
        response += 'Content-Type: text/html\r\n'
        response += 'Content-Length: %s\r\n' % (len(html))
        response += 'Last-Modified: %s\r\n\r\n' % time.ctime(os.path.getmtime(host + '/index.html'))
        response += html
    else:
        try:
            f = open(host + r_file, 'r')
            m_file = f.read()
            #f.close()
            c_type = r_file.split('.')[1]
            response = 'HTTP/1.1 200 OK\r\n'
            response += 'Date: %s\r\n' % (date_time)
            response += 'Server: Mega-Awesome/1.0\r\n'
            response += 'Content-Type: %s\r\n' % media[c_type].rstrip()
            response += 'Content-Length: %s\r\n' % (len(m_file))
            response += 'Last-Modified: %s\r\n\r\n' % time.ctime(os.path.getmtime(host + r_file))
            response += m_file
        except IOError as (errno, strerror):
            if errno == 13:
                #403 forbidden
                date_time = time.strftime("%a, %d %b %Y %H:%M:%S GMT", time.gmtime())
                html = '<!DOCTYPE html>\n<html>\n<body>\n<h1>:(</h1>\n<p>403 Forbidden</p>\n</body>\n</html>'
                response = 'HTTP/1.1 403 Forbidden\r\n'
                response += 'Date: %s\r\n' % (date_time)
                response += 'Server: Mega-Awesome/1.0\r\n'
                response += 'Content-Type: text/html\r\n'
                response += 'Content-Length: %s\r\n' % (len(html))
                response += 'Last-Modified: %s\r\n\r\n' % (date_time)
                response += html
            elif errno == 2:
                #404 File not found
                date_time = time.strftime("%a, %d %b %Y %H:%M:%S GMT", time.gmtime())
                html = '<!DOCTYPE html>\n<html>\n<body>\n<h1>:(</h1>\n<p>404 Not Found</p>\n</body>\n</html>'
                response = 'HTTP/1.1 404 Not Found\r\n'
                response += 'Date: %s\r\n' % (date_time)
                response += 'Server: Mega-Awesome/1.0\r\n'
                response += 'Content-Type: text/html\r\n'
                response += 'Content-Length: %s\r\n' % (len(html))
                response += 'Last-Modified: %s\r\n\r\n' % (date_time)
                response += html
            else:
                #500 Internal Server Error
                date_time = time.strftime("%a, %d %b %Y %H:%M:%S GMT", time.gmtime())
                html = '<!DOCTYPE html>\n<html>\n<body>\n<h1>:(</h1>\n<p>500 Internal Server Error</p>\n</body>\n</html>'
                response = 'HTTP/1.1 500 Internal Server Error\r\n'
                response += 'Date: %s\r\n' % (date_time)
                response += 'Server: Mega-Awesome/1.0\r\n'
                response += 'Content-Type: text/html\r\n'
                response += 'Content-Length: %s\r\n' % (len(html))
                response += 'Last-Modified: %s\r\n\r\n' % (date_time)
                response += html
    return response

def bad_request():
    date_time = time.strftime("%a, %d %b %Y %H:%M:%S GMT", time.gmtime())
    html = '<!DOCTYPE html>\n<html>\n<body>\n<h1>:(</h1>\n<p>400 Bad Request</p>\n</body>\n</html>'
    response = 'HTTP/1.1 400 Bad Request\r\n'
    response += 'Date: %s\r\n' % (date_time)
    response += 'Server: Mega-Awesome/1.0\r\n'
    response += 'Content-Type: text/html\r\n'
    response += 'Content-Length: %s\r\n' % (len(html))
    response += 'Last-Modified: %s\r\n\r\n' % (date_time)
    response += html
    return response

def serv_error():
    date_time = time.strftime("%a, %d %b %Y %H:%M:%S GMT", time.gmtime())
    html = '<!DOCTYPE html>\n<html>\n<body>\n<h1>:S</h1>\n<p>500 Internal Server Error</p>\n</body>\n</html>'
    response = 'HTTP/1.1 500 Internal Server Error\r\n'
    response += 'Date: %s\r\n' % (date_time)
    response += 'Server: Mega-Awesome/1.0\r\n'
    response += 'Content-Type: text/html\r\n'
    response += 'Content-Length: %s\r\n' % (len(html))
    response += 'Last-Modified: %s\r\n\r\n' % (date_time)
    response += html
    return response

def not_implemented():
    date_time = time.strftime("%a, %d %b %Y %H:%M:%S GMT", time.gmtime())
    html = '<!DOCTYPE html>\n<html>\n<body>\n<h1>:o</h1>\n<p>501 Not Implemented</p>\n</body>\n</html>'
    response = 'HTTP/1.1 501 Not Implemented\r\n'
    response += 'Date: %s\r\n' % (date_time)
    response += 'Server: Mega-Awesome/1.0\r\n'
    response += 'Content-Type: text/html\r\n'
    response += 'Content-Length: %s\r\n' % (len(html))
    response += 'Last-Modified: %s\r\n\r\n' % (date_time)
    response += html
    return response

def get_host(host_line):
    host = host_line.split(' ')[1].split(":")[0]
    return host
    
    
    
    
