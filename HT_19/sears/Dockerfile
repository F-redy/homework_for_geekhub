# Базовый образ
FROM python:3.12-slim

# Задаем рабочую директорию для контейнера
WORKDIR /code

# Копируем файлы
COPY . .

# Обновляем и устанавливаем дополнительные пакеты
RUN pip install --upgrade pip
RUN pip install -r requirements/development.txt --no-cache-dir

EXPOSE 8000
