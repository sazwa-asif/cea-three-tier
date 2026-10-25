FROM nginx:1.27-alpine

COPY nginx.conf.template /etc/nginx/templates/default.conf.template
COPY html /usr/share/nginx/html

ENV APP_UPSTREAM=app:5000 \
    DNS_RESOLVER=127.0.0.11

EXPOSE 80
