NUM_WORKERS=3
TIMEOUT=120

exec gunicorn ${DJANGO_WSGI_MODULE}:application \
--name $NAME \
--workers $NUM_WORKERS \
--timeout $TIMEOUT \
--log-level=debug \
--bind=127.0.0.1:9000 \
--pid=$PIDFILE