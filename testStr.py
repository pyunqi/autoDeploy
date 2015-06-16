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
        print 'can not login'.ip
    return sshConnection

def executeSSHCmdsInBackend(sshConnection):
    channel = sshConnection.invoke_shell()
    stdin = channel.makefile('wb')
    stdout = channel.makefile('rb')
    update_0 = "sed -i 's/,1800)/,60)/g' /home/www/default/FrontLogin.php"
    update_1 = "sed -i 's/,1800)/,60)/g' /home/www/default/testSubmit.php"
    update_2 = "sed -i 's/,1800)/,60)/g' /home/www/default/testEnd.php"
    update_3 = "sed -i 's/,1800)/,60)/g' /home/www/default/testAutoSave.php"
    update_4 = "sed -i 's/,1800)/,60)/g' /home/www/default/testKnow.php"
    update_5 = "sed -i 's/,1800)/,60)/g' /home/www/default/simulation-save-success.php"
    update_6 = "sed -i 's/,1800)/,60)/g' /home/www/default/testSaveSuccess.php"
    update_7 = "sed -i 's/,1800)/,60)/g' /home/www/default/testLeftStartTime.php"
    update_8 = "sed -i 's/,1800)/,60)/g' /home/www/default/testStartTest.php"
    update_9 = "sed -i 's/,1800)/,60)/g' /home/www/default/testList.php"
    e = 'exit'
    ok = '''
    %s
    %s
    %s
    %s
    %s
    %s
    %s
    %s
    %s
    %s
    %s
    '''%(update_0,update_1,update_2,update_3,update_4,update_5,update_6,update_7,update_8,update_9,e)
    stdin.write(ok)
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




