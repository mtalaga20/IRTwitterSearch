# creates initial file structure
mkdir nginx_https_docker && cd nginx_https_docker
mkdir config
mkdir docker
touch config/nginx.conf docker/nginx.Dockerfile
touch docker-compose.yaml docker-compose-le.yaml