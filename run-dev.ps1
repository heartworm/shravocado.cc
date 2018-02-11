$all_containers = (docker ps -a -q)
docker stop $all_containers
docker rm $all_containers
docker-compose build
docker run -v "$(gl)\nginx\nginx-root:/usr/share/nginx/html" --add-host "backend:172.22.111.1" -dp 80:80 shravocadocc_web
python ./backend/main.py