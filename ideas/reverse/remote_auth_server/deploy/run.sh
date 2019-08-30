#!/bin/bash
docker run -i -m 10m --cpus=".04" --network none --rm ras | cat

