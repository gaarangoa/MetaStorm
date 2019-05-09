FROM php:7.2-apache

RUN apt update
RUN apt install -y openssh-server
RUN mkdir -p /var/www/.ssh/
COPY ./ssh/id_rsa /var/www/.ssh/
COPY ./ssh/id_rsa.pub /var/www/.ssh/
RUN chown www-data:www-data -R /var/www/.ssh