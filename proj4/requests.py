import time
import os.path

def get_request(r_file, host, media):
    date_time = time.strftime("%a, %d %b %Y %H:%M:%S GMT", time.gmtime())
    response = 'HTTP/1.1 200 OK\r\n'
    response += 'Date: %s\r\n' % (date_time)
    response += 'Server: Mega-Awesome/1.0\r\n'
    if(r_file == '/'):
        m_file = open(host + '/index.html', 'r').readlines()
        html = ''
        for line in m_file:
            html += line
        response += 'Content-Type: text/html\r\n'
        response += 'Content-Length: %s\r\n' % (len(html))
        response += 'Last-Modified: %s\r\n\r\n' % time.ctime(os.path.getmtime(host + '/index.html'))
        response += html
    else:
        c_type = r_file.split('.')[1]
        print c_type
        m_file = open(host + r_file, 'r').readlines()
        m = ''
        for line in m_file:
            m += line
        response += 'Content-Type: %s\r\n' % media[c_type].rstrip()
        response += 'Content-Length: %s\r\n' % (len(m))
        response += 'Last-Modified: %s\r\n\r\n' % time.ctime(os.path.getmtime(host + r_file))
        print response
        response += m
    #print r_file
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
    
    
    
    
