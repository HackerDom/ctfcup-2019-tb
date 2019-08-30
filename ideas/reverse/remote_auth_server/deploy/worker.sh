while true; do socat -d TCP4-LISTEN:1337,reuseaddr,fork,keepalive exec:./run.sh; sleep 10; done
