FROM nginx:alpine

RUN apk add --no-cache nginx-mod-http-auth-request || true

COPY nginx.conf /etc/nginx/nginx.conf

RUN mkdir -p /var/cache/nginx/auth && \
    chown nginx:nginx /var/cache/nginx/auth