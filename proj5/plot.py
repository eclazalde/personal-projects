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
        times = []
        count = 0
        conn = httplib.HTTPConnection("localhost", 3000)
        
        '''while count < 100:
            startTime = time.time()
            conn.request("GET",  "/static/files/largefile.txt", None)
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
        
        f = open('myserver_data', 'w')
        
        for i in self.y:
            f.write(str(i) + '\n')
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
        ylim(0,.1)
        xlabel('(Utilization (lambda/mu))')
        ylabel('(Server Response Time (1/mu-lambda))')
        title('Lab 4 Server Response Time')
        savefig('line.png')

    def boxPlot(self):
        """ Create a box plot. """
        clf()
        self.x = []
        self.y = []
        total = 168
        f = open('tests/my10.txt').readlines()
        for i in f:
           self.y.append(float(i.split(' ')[5]))
           
        self.x.append(.1)
        ylim(0,.1)
        boxplot(self.y,positions=self.x,widths=0.5)
        xlabel('X Label (units)')
        ylabel('Y Label (units)')
        savefig('boxplot.png')

    def combinedPlot(self):
        """ Create a graph that includes a line plot and a boxplot. """
        clf()
        # plot the line
        plot(self.x,self.averages)
        # plot the boxplot
        boxplot(self.y,positions=self.x,widths=0.5)
        xlabel('X Label (units)')
        ylabel('Y Label (units)')
        savefig('combined.png')

    def histogramPlot(self):
        """ Create a histogram. """
        clf()
        hist(self.all,bins=range(0,20),rwidth=0.8)
        savefig('histogram.png')

if __name__ == '__main__':
    p = Plotter()
    #p.equationPlot()
    #p.linePlot()
    p.boxPlot()
    #p.combinedPlot()
    #p.histogramPlot()
