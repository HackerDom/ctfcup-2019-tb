while true; do socat -d TCP4-LISTEN:7171,reuseaddr,fork,keepalive exec:./run.sh; sleep 3; done
