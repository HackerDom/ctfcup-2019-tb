while true; do socat -d TCP4-LISTEN:8484,reuseaddr,fork,keepalive exec:./docker_run.sh,pty; sleep 10; done
