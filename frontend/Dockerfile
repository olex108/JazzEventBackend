# ЭТАП 1: Сборка (Build stage)
# Используем стабильную версию Node.js на легком образе Alpine
FROM node:20-alpine AS build-stage

# Увеличиваем лимит памяти для Node.js (критично для Tailwind в Docker)
ENV NODE_OPTIONS="--max-old-space-size=2048"

# Устанавливаем рабочую директорию
WORKDIR /app

# Сначала копируем только файлы зависимостей.
# Это позволяет Docker кэшировать слой с node_modules и не переустанавливать их при каждом изменении кода.
# Кэшируем зависимости
COPY package*.json ./
# Используем ci для более быстрой и чистой установки
RUN npm ci || npm install


# Копируем все исходники фронтенда (включая vite.config.js, tailwind.config.js и src)
COPY . .

# Копируем все исходники фронтенда (включая vite.config.js, tailwind.config.js и src)
#COPY src/ ./src/
#COPY vite.config.js ./
#COPY tailwind.config.js ./
#COPY postcss.config.js ./

# Шаг 4: Запускаем сборку
# Добавляем флаг --logLevel info, чтобы видеть, если что-то пойдет не так
#RUN npm run build -- --logLevel info

COPY dist ./dist

# ЭТАП 2: Раздача (Final stage)
# Нам не нужно оставлять исходники и node_modules в итоговом образе.
# Мы используем легкий nginx только как "контейнер" для передачи файлов.
FROM alpine:3.19

WORKDIR /app

# Копируем только готовый билд
COPY --from=build-stage /app/dist ./dist

# Просто держим контейнер активным для передачи файлов в Volume
CMD ["echo", "Frontend build delivered"]