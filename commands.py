#Get internal ip address
cmdGetInternalIp = "/sbin/ifconfig eth0 | grep 'inet addr' | awk -F: '{print $2}' | awk '{print $1}'"

#Replace redis.conf bind ip with current server internal ip and local ip
#keyword is bindipwithinternalip
updateInternalIpForRedis = "sed 's/bindipwithinternalip/realinternalip/g' /etc/redis/redis.conf > /etc/redis/redisi.conf"

#Clear Redis
# clearRedis = "redis-cli flushall"
#Stop Redis
stopRedis = 'redis-cli shutdown'
#Copy Redis dump.rdb
copyRedisRDB = 'scp -i node root@10.170.216.102:/var/opt/dump.rdb /var/opt/dump.rdb'
#Start Redis
startRedis = 'redis-server /etc/redis/redisi.conf'

setupCmds = [cmdGetInternalIp,updateInternalIpForRedis,stopRedis,copyRedisRDB,startRedis]

#Clean node
rmRedisiConf = 'rm -f /etc/redis/redisi.conf'
rmDump =  'rm -f /var/opt/dump.rdb' 
cleanCmds = [stopRedis,rmRedisiConf,rmDump]
