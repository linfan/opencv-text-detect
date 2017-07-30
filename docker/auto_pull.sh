if [ $# -lt 1 ]; then
    echo "Usage: ${0} <path-to-this-git-folder>"
    exit -1
fi

cd ${1}
PULL_RES=`git pull | grep 'up-to-date'`
if [ $? -eq 0 ] && [ "${PULL_RES}" == "" ]; then
    docker tag t4 t4-delete
    docker rmi t4
    docker build -t t4 .
    docker rm -f t4
    docker run -dt --name t4 -p 6000:5000 t4
    docker rmi t4-delete
fi
cd -