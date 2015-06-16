#-*- coding: utf-8 -*-
#!/usr/bin/python
# 修改所有服务器的 session timeout 到60分钟
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
        print 'can not login'.ip
    return sshConnection

def executeSSHCmdsInBackend(sshConnection):
    channel = sshConnection.invoke_shell()
    stdin = channel.makefile('wb')
    stdout = channel.makefile('rb')
    updateSessionTimeout = '''
    sed -i 's/,1800)/,3600)/g' /home/www/default/FrontLogin.php
    sed -i 's/,1800)/,3600)/g' /home/www/default/testSubmit.php
    sed -i 's/,1800)/,3600)/g' /home/www/default/testEnd.php
    sed -i 's/,1800)/,3600)/g' /home/www/default/testAutoSave.php
    sed -i 's/,1800)/,3600)/g' /home/www/default/testKnow.php
    sed -i 's/,1800)/,3600)/g' /home/www/default/simulation-save-success.php
    sed -i 's/,1800)/,3600)/g' /home/www/default/testSaveSuccess.php
    sed -i 's/,1800)/,3600)/g' /home/www/default/testLeftStartTime.php
    sed -i 's/,1800)/,3600)/g' /home/www/default/testStartTest.php
    sed -i 's/,1800)/,3600)/g' /home/www/default/testList.php
    exit
    '''
    stdin.write(updateSessionTimeout)
    print stdout.read()
    stdout.close()
    stdin.close()
    sshConnection.close()


# Execute ssh command remotely
def executeSSHCmd(sshConnection,cmd):
    stdin, stdout, stderr = sshConnection.exec_command(cmd)
    out = stdout.readlines()
    return out

  
def updateNode(args):
    ip = args
    print ip
    sshConnection = getSSHConnection(ip)
    # Execute Python "Setup Node" script
    result = executeSSHCmdsInBackend(sshConnection)
    sshConnection.close()
    print 'update',ip, result

if __name__=='__main__':

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
        jobs.put((updateNode, (ips[i])))

    # while not jobs.empty():
    #     print jobs.get()

    work_manager =  WorkManager(jobs, threadNum)
    work_manager.wait_allcomplete()




