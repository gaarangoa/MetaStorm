FROM php:7.2-apache

RUN apt update
RUN apt install -y openssh-server
RUN mkdir -R /var/www/.ssh/
RUN chmod 777 /var/www/.ssh/