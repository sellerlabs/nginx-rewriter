FROM nginx
MAINTAINER Brian Whigham <oobx@itmonger.com>
RUN \
  apt-get update && \
  apt-get install -y python python-yaml 
RUN \
  rm -f /var/log/nginx/* && \
  mv /etc/nginx/conf.d/default.conf /etc/nginx/conf.d/zzz-default.conf && \
  ln -s /dev/stderr /var/log/nginx/error.log && \
  ln -s /dev/stdout /var/log/nginx/access.log
COPY start.py /
CMD ["/start.py"]
