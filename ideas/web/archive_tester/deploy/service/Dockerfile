FROM ubuntu:18.04

RUN apt update && \
    apt install -y php-fpm unzip

RUN useradd -s /bin/false -m task

RUN mkdir -p /var/www/html/

WORKDIR /var/www/html/

ADD php/php.ini php/php-fpm.conf /etc/

ADD .secret_flag_file_05f85a4b8c8927fbbfd3f664a3204ecd081cc307e52c8822775d7e5b42056110.php index.php ./

RUN mv /usr/sbin/php-fpm* /usr/sbin/php-fpm 

ENTRYPOINT ["php-fpm", "-F", "-O", "-y", "/etc/php-fpm.conf", "-c", "/etc/php.ini"]

