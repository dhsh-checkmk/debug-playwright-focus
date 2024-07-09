#!/usr/bin/bash

set -e

CHECKMK_DOCKER="check-mk-cloud-docker-2.4.0-2024.07.09.tar.gz"
wget https://download.checkmk.com/checkmk/2.4.0-2024.07.09/${CHECKMK_DOCKER}

docker load < ./${CHECKMK_DOCKER}
docker container run \
    -dit \
    -p 8080:5000 \
    -p 8000:8000 \
    --tmpfs /opt/omd/sites/cmk/tmp:uid=1000,gid=1000 \
    --name monitoring \
    -v /etc/localtime:/etc/localtime:ro \
    --restart always \
    checkmk/check-mk-cloud:2.4.0-2024.07.09

echo "Wait for 30 seconds for the logs to populate."
sleep 30
docker container logs monitoring | grep "with\ password"
