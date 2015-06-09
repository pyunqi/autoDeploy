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

    stopRedis = cleanCmds[0]
    subprocess.call(stopRedis,shell=True)

    rmRedisiConf = cleanCmds[1]
    subprocess.call(rmRedisiConf,shell=True)

    rmDump = cleanCmds[2]
    subprocess.call(rmDump,shell=True)
 
    print ' ~ OK'


