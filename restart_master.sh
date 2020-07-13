#!/bin/bash -l
kill -9  $(lsof -t -i:8070)     #先杀死已存在uwsgi的端口
kill -9  $(lsof -t -i:8071)     #杀死asgi
echo 'close the master service'

cd /home/meme/master/ZhiFou     #Zhifou路劲
yes  | python3 manage.py rebuild_index

#daphne.py所在路劲  --access-log日志文件可要可不要
/usr/local/bin/daphne  -p 8071 -b 127.0.0.1 --access-log /home/meme/daphne_master.log  --proxy-headers  ZhiFou.asgi:application &> /home/meme/daphne_master.log   &
uwsgi --ini /home/meme/master/ZhiFou/uwsgi.ini &>  /home/meme/http_request_master.log  &  #make sure the port in uwsgi.ini ;
echo 'master  service restart' 
