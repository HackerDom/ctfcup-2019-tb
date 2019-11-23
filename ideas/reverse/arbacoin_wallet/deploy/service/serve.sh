while true; do socat -d TCP4-LISTEN:31337,reuseaddr,fork,keepalive exec:./run.sh; sleep 3; done
