#!/bin/bash

mkdir /sys/fs/cgroup/{cpu,memory,pids}/NSJAIL
mkdir -p /var/log/nsjail

nsjail \
    -Mr \
    --rw \
    --cwd /app/ \
    --chroot / \
    --user nobody \
    --group nogroup \
    --hostname jail \
    --log /var/log/nsjail/nsjail.log \
    --time_limit 900 \
    --cgroup_cpu_ms_per_sec 100 \
    --cgroup_mem_max 134217728 \
    --cgroup_pids_max 512 \
    --disable_clone_newnet \
    --keep_env \
    --env PATH=/bin:/usr/bin:/usr/sbin \
    -- $@
