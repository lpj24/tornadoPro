#/bin/bash
evaluationBot_container=`docker ps -a -f name=evaluationBotServer_server -q`
echo ${#evaluationBot_container}
if test -z $evaluationBot_container
then
    echo "container not exists"
else
    echo "container exists"
    docker rm -f evaluationBotServer_server 
fi

docker build -t evaluation_image .
docker_exec_status=`docker run -p 8888:8888 -it -d --name evaluationBotServer_server evaluation_image`

if test -z $docker_exec_status
then
    echo "启动失败" + $docker_exec_status
else
    echo "容器启动成功" + $docker_exec_status
fi
