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

# Собираем статику и применяем миграции
RUN python manage.py collectstatic --noinput
RUN python manage.py migrate --noinput

# Переменные окружения для суперпользователя
ENV DJANGO_SUPERUSER_USERNAME=shop_admin
ENV DJANGO_SUPERUSER_PASSWORD=shop_admin_password
ENV DJANGO_SUPERUSER_EMAIL=admin@example.com

# Создаём суперпользователя (если его нет)
RUN python manage.py createsuperuser --noinput || true

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]