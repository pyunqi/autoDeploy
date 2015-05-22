#-*- coding: utf-8 -*-
#!/usr/bin/python
import paramiko
import threading
from commands import *
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

#Execute ssh commands remotely
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

def setRedis(args):
    ip = args[0]
    cmds = args[1]
    sshConnection = getSSHConnection(ip)
    # get internal ip
    internalIpaddress = executeSSHCmd(sshConnection,cmds[0])
    # update redis conf
    if(updateRedis):
        bindUpdate = 'bind 127.0.0.1 ' + internalIpaddress[0].strip()
        cmdUpdateRedis = cmds[1].replace('realinternalip',bindUpdate)
        executeSSHCmds(sshConnection,cmdUpdateRedis)
    else:
        print 'does not need to update.'
    # clear and stop redis
    # cmdClearRedis = cmds[2]
    cmdStopRedis = cmds[2]
    print cmdStopRedis
    # executeSSHCmd(sshConnection,cmdClearRedis)
    executeSSHCmd(sshConnection,cmdStopRedis)
    # copy redis dump.rdb
    cmdCopyRedisRDB = cmd[3]
    print cmdCopyRedisRDB
    executeSSHCmd(sshConnection,cmdCopyRedisRDB)
    # start redis
    cmdStartRedis = cmds[4]
    executeSSHCmd(sshConnection,cmdStartRedis)
    #关闭连接
    sshConnection.close()


if __name__=='__main__':
    #你要执行的命令列表
    cmds = 
    #登录信息
    # username = constants.uname
    # password = constants.passwd
    ips = []
    #Generate tasks list
    jobs = Queue.Queue()
    #Get node address
    if (useNodeName):
        for i in range(1,constants.nodeNumber+1):
            temp = constants.nodeNamePrefix+str(i)+constants.nodeAddrSubfix
            ips.append(temp)
    else:
        ips = constants.nodeIps

    for i in range(0,2):
        jobs.put((setRedis, (ips[i],cmds)))

    # while not jobs.empty():
    #     print jobs.get()

    work_manager =  WorkManager(jobs, 2)
    work_manager.wait_allcomplete()




