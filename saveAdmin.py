#-*- coding: utf-8 -*-
#!/usr/bin/python

import paramiko
import threading
from constants import *
import Queue
from ThreadPool import *

# If set to True , will use node address
useNodeName = True

def getSSHConnection(ip):
    try :
        sshConnection = paramiko.SSHClient()
        sshConnection.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        #use default user 'root'
        sshConnection.connect(ip,22,'root',timeout=5)
    except :
        print 'can not login'
    return sshConnection

    
# Execute ssh command remotely
def executeSSHCmd(sshConnection,cmd):
    stdin, stdout, stderr = sshConnection.exec_command(cmd)
    out = stdout.readlines()
    return out


if __name__=='__main__':

    cleanRedis = "redis-cli save"
    ip = '123.56.109.9'
    sshConnection = getSSHConnection(ip)
    # Execute Python "Setup Node" script
    result = executeSSHCmd(sshConnection,cleanRedis)
    sshConnection.close()
    print 'Saved',ip,result



