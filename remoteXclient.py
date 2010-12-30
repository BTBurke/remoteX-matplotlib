#!/usr/bin/env python

from socket import *
import pickle

class remoteXclient:

    def __init__(self):
        self.socketup()
        if not self.serverup:
            print "RemoteX Client: server not found.  Using X11 forwarding."
        self.socketdown()

    def socketup(self, ip='', port=9898):
        self.socketobj = socket(AF_INET, SOCK_STREAM)
        try:
            self.socketobj.connect((ip,port))
            self.serverup = True
        except:
            self.serverup = False


    def plot(self, *args, **kwargs):

        self.socketup()
        if self.serverup:
            cmdstring = {'args': args, 'kwargs': kwargs}
            self.socketobj.send(pickle.dumps(cmdstring,2))
            self.socketdown()
        else:
            print "RemoteX Client: server is down, cannot forward."
        
    def socketdown(self):
        self.socketobj.close()

if __name__ == '__main__':
    remX = remoteXclient()
    remX.plot(range(10),range(5),linewidth=0.5)

