# frontend/Dockerfile
FROM node:20-alpine

WORKDIR /app
COPY frontend /app

RUN npm install
RUN npm run build

# Установка сервера для отдачи статики
RUN npm install -g serve

# Запуск
CMD ["serve", "-s", "dist", "-l", "5173"]
