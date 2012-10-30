
#!/bin/bash

# Replace these three settings.
PROJDIR="/home/garbos/unicorn7/unicorn7/"
PIDFILE="$PROJDIR/site.pid"
SOCKET="$PROJDIR/site.sock"

cd $PROJDIR
if [ -f $PIDFILE ]; then
    kill `cat -- $PIDFILE`
    rm -f -- $PIDFILE
fi

exec /usr/bin/env - \
  PYTHONPATH="../python:.." \
  python2.6 manage.py runfcgi socket=$SOCKET pidfile=$PIDFILE