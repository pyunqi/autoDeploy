#-*- coding: utf-8 -*-
#!/usr/bin/python

import paramiko
import threading
from constants import *
import Queue
from ThreadPool import *

# If set to True , will use node address
useNodeName = True

def getSSHConnectionUP(ip,username,passwd):
    try :
        sshConnection = paramiko.SSHClient()
        sshConnection.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        sshConnection.connect(ip,22,username,passwd,timeout=5)
    except :
        print 'can not login'
    return sshConnection

def getSSHConnection(ip):
    try :
        sshConnection = paramiko.SSHClient()
        sshConnection.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        #use default user 'root'
        sshConnection.connect(ip,22,'root',timeout=5)
    except :
        print 'can not login'
    return sshConnection

#Execute mutiple ssh commands remotely sample
def executeSSHCmds(sshConnection,cmd):
    channel = sshConnection.invoke_shell()
    stdin = channel.makefile('wb')
    stdout = channel.makefile('rb')
    h = 'cd .ssh'
    l = 'ls'
    s = 'exit'
    ok = '''
    %s
    %s
    %s
    '''%(h,l,s)
    stdin.write(ok)
    print stdout.read()
    stdout.close()
    stdin.close()
    sshConnection.close()
    exit()
#Execute ssh command remotely
def executeSSHCmd(sshConnection,cmd):
    stdin, stdout, stderr = sshConnection.exec_command(cmd)
    out = stdout.readlines()
    return out

def setupNode(args):
    ip = args[0]
    cmds = args[1]
    sshConnection = getSSHConnection(ip)
    # Execute Python "Setup Node" script
    result = executeSSHCmd(sshConnection,cmds)
    sshConnection.close()
    print result

if __name__=='__main__':
    cmds = runSetupNode
    ips = []
    #Generate tasks list
    jobs = Queue.Queue()
    #Get node address
    if (useNodeName):
        for i in range(1,nodeNumber+1):
            temp = nodeNamePrefix+str(i)+nodeAddrSubfix
            ips.append(temp)
    else:
        ips = nodeIps

    for i in range(0,nodeNumber):
        jobs.put((setupNode, (ips[i],cmds)))

    # while not jobs.empty():
    #     print jobs.get()

    work_manager =  WorkManager(jobs, threadNum)
    work_manager.wait_allcomplete()




