FROM nginx
MAINTAINER Brian Whigham <oobx@itmonger.com>
RUN \
	echo "deb http://ftp.debian.org/debian jessie-backports main" >> /etc/apt/sources.list.d/jessie-backports.list && \
  apt-get update && \
  apt-get install -y python python-pip python-yaml && \
  apt-get install -y certbot -t jessie-backports && \
  pip install cffi

RUN \
	mkdir -p /var/www/nginx-rewriter && \
	chmod -R 777 /var/www/nginx-rewriter

RUN \
  rm -f /var/log/nginx/* && \
  mv /etc/nginx/conf.d/default.conf /etc/nginx/conf.d/zzz-default.conf && \
  ln -s /dev/stderr /var/log/nginx/error.log && \
  ln -s /dev/stdout /var/log/nginx/access.log
COPY start.py /
CMD ["/start.py"]
