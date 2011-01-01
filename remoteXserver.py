#!/usr/bin/env python

from socket import *
import pickle
import thread
import matplotlib.pyplot as plt

#class remoteXserver:

def startserver(ip='', port=9898):
    """
    Starts server on local machine and accepts pickled matplotlib.pyplot commands    """
    socketobj = socket(AF_INET, SOCK_STREAM)
    socketobj.bind((ip,port))
    socketobj.listen(5)
    print "Server listening on port %d" % port
        
    while True:
        connection, address = socketobj.accept()
        savstring = ''
        while True:
            cmdstring = connection.recv(1024)
            savstring += cmdstring
            if not cmdstring: break
        connection.close()
        if savstring:
            thread.start_new_thread(doplot, (savstring,))

def doplot(cmdstring):
    """
    In a new thread, unpickle the command and sent to matplotlib for action.  All matplotlib.pyplot commands are supported.
    """
    cmdstring = pickle.loads(cmdstring)
    try:
        func = cmdstring['func']
        print "Processed ", len(cmdstring['args']), " arguments for the ", func, "function"
        print len(cmdstring['args'])
        plt.__dict__[func](*cmdstring['args'], **cmdstring['kwargs'])
    except Exception as errordetail:
        print "Error: ", errordetail
        #plt.close()
        
if __name__ == '__main__':
    startserver()
