#!/bin/bash
# chkconfig: 2345 66 36
# /etc/rc.d/init.d/opt/python
# description: spython
#
case "$1" in
  start)
        echo -n "Starting python: "
        echo start
        cd  /root/IotPlatform
	./run.py &
        echo "Done."
        ;;
  stop)
        echo -n "Shutting Down python Listeners: "
        echo "python"
        killall -9 run.py
        echo "Done."
        ;;
  *)
  echo "Usage: python { start | stop | restart }"
  exit 1
esac
exit 0