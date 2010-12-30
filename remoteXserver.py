#!/usr/bin/env python

from socket import *
import pickle
import matplotlib.pyplot as plt

class remoteXserver:

    def __init__(self, ip='', port=9898):
        self.socketobj = socket(AF_INET, SOCK_STREAM)
        self.socketobj.bind((ip,port))
        self.socketobj.listen(5)

        
        while True:
            connection, address = self.socketobj.accept()
            savstring = ''
            while True:
                cmdstring = connection.recv(1024)
                savstring += cmdstring
              #  print cmdstring
               # print savstring
                if not cmdstring: break
            connection.close()
            if savstring:
                self.doplot(savstring)

    def doplot(self, cmdstring):
        cmdstring = pickle.loads(cmdstring)
        plt.plot(*cmdstring['args'], **cmdstring['kwargs'])


if __name__ == '__main__':
    remX = remoteXserver()
