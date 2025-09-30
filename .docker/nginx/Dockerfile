FROM nginx:alpine

RUN apk update && apk upgrade && rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d
COPY views /usr/src/app/static/views/

EXPOSE 80

WORKDIR /usr/src/app

CMD ["nginx", "-g", "daemon off;"]