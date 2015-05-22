
import subprocess
from commands import *
import os

def subprocess_cmd(command):
    process = subprocess.Popen(command,stdout=subprocess.PIPE, shell=True)
    proc_stdout = process.communicate()[0].strip()
    return proc_stdout


if __name__=='__main__':
    
    # Detect if redis is running or not
    pf ="/var/run/redis.pid"
    needToStop = False
    if (os.path.exists(pf)):
        needToStop = True
        # print 'need to stop'
    # Get command for adding internal ip in Redis conf 
    getInternalIp = cmds[0]
    internalIpaddress = subprocess_cmd(getInternalIp)
    bindUpdate = 'bind ' + internalIpaddress + ' 127.0.0.1'
    cmdUpdateRedis = cmds[1].replace('realinternalip',bindUpdate)
    # Check if need to stop Redis Server
    if (needToStop) :
        cmdStopDefaultRedis = cmds[2]
        subprocess.call(cmdStopDefaultRedis,shell=True)
        print 'stopped redis servers'
    # Update redis server conf
    subprocess.call(cmdUpdateRedis,shell=True)
    # Copy Redis RDB from test backend server
    cmdCopyRedisRDB = cmds[3]
    # print cmdCopyRedisRDB
    subprocess.call(cmdCopyRedisRDB,shell=True)
    # Start Redis Server
    cmdStartRedis = cmds[4]
    # print cmdStartRedis
    subprocess.call(cmdStartRedis,shell=True)
    print internalIpaddress, ' ~ OK'


