FROM nginx:stable-alpine

# Удаляем дефолтный конфиг
RUN rm /etc/nginx/conf.d/default.conf

# Копируем твой исправленный конфиг
COPY default.conf /etc/nginx/conf.d/default.conf