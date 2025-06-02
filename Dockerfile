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

# Переменные окружения для суперпользователя
ENV DJANGO_SUPERUSER_USERNAME=shop_admin_aaa
ENV DJANGO_SUPERUSER_PASSWORD=shop_admin_password
ENV DJANGO_SUPERUSER_EMAIL=admin@example.com

# Создаём суперпользователя (если его нет)
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
