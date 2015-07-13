<?php
require("class-excel-xml.inc.php");
include_once('./lib/cart.class.php') ;
include_once('./lib/redis.arr.class.php') ;
include "./lib/libchart/classes/libchart.php";
$conns = $this->actionConnectRedis() ;
$allResponse = array() ;
foreach($conns as $i => $conn){
                    $resList = $conn->get('redis_respondents_1_2898') ;
                    $resList = unserialize($resList) ;
                    //var_dump($resList) ;
                    if(!empty($resList)){
                            return $resList ;
                    }
            }

    function actionConnectRedis(){

                $redis_slave_config = FLEA::getAppInf('computer') ;
                $redis_slave_count =  $redis_slave_config[slave_count] ;
                $redisSlave = FLEA::getAppInf("redis_slave") ;
                $conns=array();
                foreach($redisSlave as $redis){
                        $redis_connect = new Redis() ;
                        $redis_connect->connect($redis["ip"],$redis["port"]);
                        $conns[]=$redis_connect;
                }
                return $conns ;
        }

?>

