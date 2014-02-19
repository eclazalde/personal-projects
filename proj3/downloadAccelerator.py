import argparse
import os
import requests
import threading
import time

''' Downloader for a set of files '''
class Downloader:
    def __init__(self):
        ''' initialize the file where the list of URLs is listed, and the
        directory where the downloads will be stored'''
        self.args = None
        self.numthreads = '1'
        self.url = ''
        self.filename = 'default.txt'
        self.parse_arguments()

    def parse_arguments(self):
        ''' parse arguments, which include '-n' for the number of threads to use and
        'url' for the required url file to download'''
        parser = argparse.ArgumentParser(prog='Download Accelerator', description='Script which will download a file at a given URL with the given number of threads in parallel', add_help=True)
        parser.add_argument('-n', '--threads', type=str, action='store', help='Specify the number of threads to use',default='1', required=False)
        parser.add_argument('url', type=str, action='store', help='Specify the URL where the file is located')
        args = parser.parse_args()
        self.numthreads = args.threads
        self.url = args.url
    
    def download(self):
        total_size = 0
        chunk_size = 0
        
        r = requests.head(self.url)
        if 'Content-Length' in r.headers:
            total_size = r.headers['Content-Length']
            chunk_size = int(total_size) / int(self.numthreads) + 1
            #part = r.headers['Content-Type'].split(';')[0].split('/')
            
            if self.url[-1] == '/':
                self.filename = 'index.html'
            else:
                name = self.url.split('/')
                self.filename = name[len(name)-1]
                
            #print self.url   
            #print self.filename
            #print int(total_size)
            #print chunk_size
            
            sections = []
            current = -1
            while (int(current) < int(total_size)):
                if int(current + chunk_size) < int(total_size):
                    temp = {'s':current + 1, 'e':current + chunk_size}
                    sections.append(temp)
                    current = current + chunk_size
                else:
                    temp = {'s':current + 1, 'e':r.headers['Content-Length']}
                    sections.append(temp)
                    current = current + chunk_size
                    
            #for el in sections:
            #    print '%s - %s' % (el['s'], el['e'])
            
            doc = '' 
            # create a thread for each url
            # START TIMER
            t0 = time.time()
            threads = []
            for section in sections:
                d = DownThread(self.url,section['s'], section['e'])
                threads.append(d)
            for t in threads:
                t.start()
            for t in threads:
                t.join()
                doc += t.request.content
                #print t.request.status_code
            # END TIMER
            t1 = time.time()
            t_total = t1-t0
            f = open(self.filename, 'wb')
            f.write(doc)
            f.close()
            print '%s %s %s %s' % (self.url, self.numthreads, total_size, t_total)
        else:
            print 'No valid "Content-Length" header returned by HEAD request'

''' Use a thread to download one file given by url and stored in filename'''
class DownThread(threading.Thread):
    def __init__(self,url,s, e):
        self.url = url
        self.s = s
        self.e = e
        self.request = None
        threading.Thread.__init__(self)
        self._content_consumed = False

    def run(self):
        #print 'Downloading chunk: %s-%s' % (self.s, self.e)
        header = {'Range': 'bytes=%s-%s' % (self.s, self.e)}
        self.request = requests.get(self.url, headers=header)
 
if __name__ == '__main__':
    d = Downloader()
    d.download()
