#!/usr/bin/env python

from socket import *
import pickle
import thread
import matplotlib.pyplot as plt

#class remoteXserver:

def startserver(ip='', port=9898):
    socketobj = socket(AF_INET, SOCK_STREAM)
    socketobj.bind((ip,port))
    socketobj.listen(5)

        
    while True:
        connection, address = socketobj.accept()
        savstring = ''
        while True:
            cmdstring = connection.recv(1024)
            savstring += cmdstring
            #print cmdstring
            # print savstring
            if not cmdstring: break
        connection.close()
        if savstring:
            thread.start_new_thread(doplot, (savstring,))
            #self.doplot(savstring)

def doplot(cmdstring):
    cmdstring = pickle.loads(cmdstring)
    print cmdstring
    try:
        #curfig = plt.gcf()
        #if not curfig:
        #    plt.figure(1)
        #plt.ioff()
        plt.figure()
        plt.plot(*cmdstring['args'], **cmdstring['kwargs'])
        plt.draw()
        plt.show()
        plt.ioff()
        #plt.close()
    except:
        print "Error: "
        #plt.close()
        

if __name__ == '__main__':
    startserver()
