#!/usr/bin/env python

from socket import *
import pickle

class remoteXclient:

    def __init__(self):
        self.cmdstring_list = []
        #self.socketup()
        #if not self.serverup:
        #    print "RemoteX Client: server not found. Please start the server on your local machine."
        #self.socketdown()

    def __getattr__(self, func):
        def interceptmethod(*args, **kwargs):
            #self.socketup()
            cmdstring = {'func': func, 'args': args, 'kwargs': kwargs}
            self.cmdstring_list.append(cmdstring)
            if func == 'show':
                self.socketup()
                if self.serverup:
                    self.socketobj.send(pickle.dumps(self.cmdstring_list,2))
                    self.socketdown()
                else:
                    print "RemoteX Client: server is down, cannot forward."
                    print cmdstring
                self.cmdstring_list = []
            #else:
             #   self.cmdstring_list.append(cmdstring)

        return interceptmethod

    def socketup(self, ip='', port=9898):
        self.socketobj = socket(AF_INET, SOCK_STREAM)
        try:
            self.socketobj.connect((ip,port))
            self.serverup = True
        except:
            self.serverup = False
        
    def socketdown(self):
        self.socketobj.close()

if __name__ == '__main__':
    remX = remoteXclient()
    remX.figure()
    remX.plot(range(20),range(20),linewidth=0.5)
    remX.show()
    remX.figure()
    remX.plot(range(10), range(10))
    remX.title('Test Title, 2nd Figure')
    remX.show()
