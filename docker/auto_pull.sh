#!/bin/bash
# E.g. crontab -l
# */3 * * * * /home/flin/opencv-text-detect/docker/auto_pull.sh /home/flin/opencv-text-detect

if [ $# -lt 1 ]; then
    echo "Usage: ${0} <path-to-this-git-folder>"
    exit -1
fi

cd ${1}
PULL_RES=`git pull`
if [ $? -eq 0 ]; then
    CHECK_RES=`echo $PULL_RES | grep 'up-to-date'`
    if [ "${CHECK_RES}" == "" ]; then
        docker tag t4 t4-delete
        docker rmi t4
        docker build -t t4 .
        docker rm -f t4
        docker run -dt --name t4 -p 5050:5000 t4
        docker rmi t4-delete
    fi
fi
cd - >/dev/null