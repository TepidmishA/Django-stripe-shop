# Используем официальный Python-образ
FROM python:3.12-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Открываем порт
EXPOSE 8000

# Команда по умолчанию
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
