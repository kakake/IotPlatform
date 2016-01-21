#!/bin/bash
# chkconfig: 2345 66 36
# /etc/rc.d/init.d/opt/python
# description: spython
#
case "$1" in
  start)
        echo -n "Starting python: "
        echo "---------------------------------------------------------------------------------" >>/var/log/python
        date +"! %T %a %D : Starting python ." >>/var/log/python
        echo "---------------------------------------------------------------------------------" >>/var/log/python
	echo start
        cd  /root/IotPlatform
	./run.py &
	#sh /root/finmonAgent/startpy
        echo "Done."
        echo ""
        echo "---------------------------------------------------------------------------------" >>/var/log/python
        date +"! %T %a %D : Finished." >>/var/log/python
        echo "---------------------------------------------------------------------------------" >>/var/log/python
        touch /var/lock/subsys/python
        ;;
  stop)
        echo -n "Shutting Down python Listeners: "
        echo "---------------------------------------------------------------------------------" >>/var/log/python
        date +"! %T %a %D : Shutting Down python." >>/var/log/python
        echo "---------------------------------------------------------------------------------" >>/var/log/python
	echo "python"
        killall -9 run.py
        echo "Done."
        rm -f /var/lock/subsys/python      
        echo "Done."
        echo "---------------------------------------------------------------------------------" >>/var/log/python
        date +"! %T %a %D : Finished." >>/var/log/python
        echo "---------------------------------------------------------------------------------" >>/var/log/python
        ;;
  *)
  echo "Usage: python { start | stop | restart }"
  exit 1
esac
exit 0