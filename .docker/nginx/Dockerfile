FROM nginx:1.19.0-alpine

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d
COPY views /usr/src/app/static/views/

EXPOSE 80

WORKDIR /usr/src/app

CMD ["nginx", "-g", "daemon off;"]