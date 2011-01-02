#!/usr/bin/env python

from socket import *
import pickle
import thread
import matplotlib
matplotlib.use('Agg') #Use non-Tk backend
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import os, sys
import uuid


ip = ''
port = 9898
socketobj = socket(AF_INET, SOCK_STREAM)
socketobj.bind((ip,port))
socketobj.listen(5)
print "Server listening on port %d" % port

activeChildren = []
def reapChildren():
    while activeChildren:
        pid, stat = os.waitpid(0, os.WNOHANG)
        if not pid: break
        activeChildren.remove(pid)

def handleClient(connection):
    """
    Receive data on each new connection to server
    """
    savstring = ''
    while True:
        cmdstring = connection.recv(1024)
        savstring += cmdstring
        if not cmdstring: break
    if savstring:
        doplot(savstring)
    connection.close()

def doplot(cmdstring_list):
    """
    Unpickle the command and send to matplotlib for action.  All matplotlib.pyplot commands are supported. Output to PNG file.
    """
    cmdstring_list = pickle.loads(cmdstring_list)
    try:
        for cmdstring in cmdstring_list:
            func = cmdstring['func']
            print "Processed ", len(cmdstring['args']), " arguments for the ", func, "function"
            if func == 'show':
                filename = str(uuid.uuid4()) + '.png'
                plt.savefig(filename, dpi=500)
            else:
                plt.__dict__[func](*cmdstring['args'], **cmdstring['kwargs'])
    except Exception as errordetail:
        print "Error: ", errordetail
    finally:
        os._exit(0)

def dispatcher():
    """
    Forks new process on each connection from the client to draw a figure
    """
    while True:
        connection, address = socketobj.accept()
        #reapChildren()
        childPid = os.fork()
        if childPid == 0:
            handleClient(connection)
        else:
            activeChildren.append(childPid)
        print activeChildren

dispatcher()
