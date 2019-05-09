FROM php:7.2-apache

RUN apt update
RUN apt install -y openssh-server
RUN mkdir -R /var/www/.ssh/
COPY ./ssh/ /var/www/.ssh/
RUN chown www-data:www-data -R /var/www/.ssh