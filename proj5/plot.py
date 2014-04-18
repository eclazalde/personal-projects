import optparse

import sys
import httplib
import time
import os.path

import matplotlib
matplotlib.use('Agg')
from pylab import *

# Class that parses a file and plots several graphs
class Plotter:
    def __init__(self):
        '''times = []
        count = 0
        conn = httplib.HTTPConnection("localhost", 3000)
        
        while count < 100:
            startTime = time.time()
            conn.request("GET",  "/static/img/beehive.png", None)
            response = conn.getresponse()
            
            if response.status == httplib.OK:
                text = response.read()
                endTime = time.time()
                times.append(endTime - startTime)
                count += 1
            else:
                print 'Test failed!'
                sys.exit()
            
        total = 0
        for i in times:
            total += i
        average = total / 100

        self.x = []
        self.y = []
        mu = 1 / average
        xLambda = 0
        
        while xLambda < mu:
            t = 1 / (mu - xLambda)
            self.y.append(t)
            self.x.append(xLambda / mu)
            xLambda =xLambda + 1
        
        f = open('lighttpd_data.txt', 'w')
        
        for i in self.y:
            f.write(str(i) + ' ' + '\n')
        f.close()
        print average
        print mu'''

    def equationPlot(self):
        """ Create a line graph of an equation. """
        clf()
        x = np.arange(0,9.9,0.1)
        plot(x,1/(10-x))
        xlabel('X')
        ylabel('1/(10-x)')
        savefig('equation.png')

    def linePlot(self):
        """ Create a line graph. """
        clf()
        plot(self.x,self.y)
        ylim(0,.01)
        xlabel('(Utilization (lambda/mu))')
        ylabel('(Server Response Time (1/mu-lambda))')
        title('Lighttpd Server Response Time')
        savefig('line.png')

    def boxPlot(self):
        """ Create a box plot. """
        clf()
        self.x = []
        self.y = []
        total = 168
        f = open('tests/my1000.txt').readlines()
        for i in f:
           self.y.append(float(i.split(' ')[5]))
           
        self.x.append(.1)
        ylim(0,.1)
        boxplot(self.y,positions=self.x,widths=0.5)
        xlabel('X Label (units)')
        ylabel('Y Label (units)')
        savefig('boxplot.png')

    def combinedPlot1(self):
        """ Create a graph that includes a line plot and a boxplot. """
        clf()
        # line stuff
        lines = []
        xlines = []
        lc = 0
        l = open('myserver_data.txt', 'r').readlines()
        for line in l:
            lines.append(float(line))
            xlines.append(float(lc / float(1579)))
            #print ('%s, %s') % (float(lc / 1579), line)
            lc += 1
        # boxplot stuff
        self.x = []
        self.y = []
        num = 1
        while num < 11:
            group = []
            fil = ('tests/my-load' + str(num) + '0.txt')
            b = open(fil, 'r').readlines()
            for line in b:
                group.append(float(line.split(' ')[5]))
            self.y.append(group)
            self.x.append(float(num) / 10)
            num += 1
        # plot the boxplot
        #xlim(0, 1.)
        #ylim(0,.01)
        boxplot(self.y,positions=self.x,widths=0.05)
        # plot the line
        xlim(0,1.1)
        ylim(0, .1)
        plot(xlines,lines)
        xlabel('(Utilization (lambda/mu))')
        ylabel('(Server Response Time (1/mu-lambda))')
        title('Lab 4 Server Response Time')
        savefig('myserver_combined.png')

    def combinedPlot2(self):
        """ Create a graph that includes a line plot and a boxplot. """
        clf()
        # line stuff
        lines = []
        xlines = []
        lc = 0
        l = open('lighttpd_data.txt', 'r').readlines()
        for line in l:
            lines.append(float(line))
            xlines.append(float(lc / float(1579)))
            #print ('%s, %s') % (float(lc / 1579), line)
            lc += 1
        # boxplot stuff
        self.x = []
        self.y = []
        num = 1
        while num < 11:
            group = []
            fil = ('tests/lt-load' + str(num) + '0.txt')
            b = open(fil, 'r').readlines()
            for line in b:
                group.append(float(line.split(' ')[5]))
            self.y.append(group)
            self.x.append(float(num) / 10)
            num += 1
        # plot the boxplot
        #xlim(0, 1.)
        #ylim(0,.01)
        boxplot(self.y,positions=self.x,widths=0.05)
        # plot the line
        xlim(0,1.1)
        ylim(0, .1)
        plot(xlines,lines)
        xlabel('(Utilization (lambda/mu))')
        ylabel('(Server Response Time (1/mu-lambda))')
        title('Lighttpd Server Response Time')
        savefig('lighttpd_combined.png')

    def histogramPlot(self):
        """ Create a histogram. """
        clf()
        hist(self.all,bins=range(0,20),rwidth=0.8)
        savefig('histogram.png')

if __name__ == '__main__':
    p = Plotter()
    #p.equationPlot()
    #p.linePlot()
    #p.boxPlot()
    p.combinedPlot1()
    p.combinedPlot2()
    #p.histogramPlot()
