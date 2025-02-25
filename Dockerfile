FROM mariadb:latest

COPY ./sql/init.sql /docker-entrypoint-initdb.d/
