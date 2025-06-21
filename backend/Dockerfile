# backend/Dockerfile
FROM python:3.10-slim

# Установка зависимостей
WORKDIR /app
COPY backend /app
RUN pip install --no-cache-dir -r requirements.txt

# Команда запуска сервера
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
