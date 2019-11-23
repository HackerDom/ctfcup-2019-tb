while true; do socat -d TCP4-LISTEN:31337,reuseaddr,fork,keepalive exec:./main; sleep 3; done
