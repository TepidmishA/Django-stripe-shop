# Магазин на Django с интеграцией Stripe

Это простое Django-приложение с интеграцией Stripe, позволяющее:
- просматривать товары (`Item`).
- Создавать заказы (`Order`) из нескольких товаров с возможностью применения скидки (`Discount`) и налога (`Tax`).
- Оплачивать либо один товар, либо весь заказ сразу через `Stripe Payment Intent` или `Stripe Session`.

## Функциональность
**Модели**
- `Item` - название, описание, цена, валюта (usd или pln).
- `Discount` - код скидки и процент.
- `Tax` - название налога и процент.
- `Order` - множество товаров, опционально прикреплённые скидка/налог.

**Просмотр товара**
- URL - `/item/<item_id>/`.
- Отображается информация о товаре и кнопка "Buy".

**Оплата одного товара**
- При нажатии кнопки "Buy" на странице товара может происходить либо:
  - Перенаправление на `Stripe Checkout` (если используется `Stripe Session`).
  - Либо открываться встроенное меню с оплатой прямо на этой же странице (если используется `Stripe Payment Intent`).
- Для этого реализованы два метода:
  - `GET /buy/<item_id>/` - создаёт `tripe Checkout Session` и возвращает `{ "id": session_id }`.
  - `GET /item/<item_id>/intent/` - создаёт `Stripe Payment Intent` и возвращает `{ "client_secret": ... }`.

**Просмотр заказа**
- URL - `/order/<order_id>/`.
- Отображается список товаров заказа, показаны `subtotal`, `discount`, `tax` и итоговая сумма. Кнопка “Pay”.

**Оплата заказа**
- При нажатии кнопки "Buy" на странице заказа может происходить либо:
  - Перенаправление на `Stripe Checkout` (если используется `Stripe Session`).
  - Либо открываться встроенное меню с оплатой прямо на этой же странице (если используется `Stripe Payment Intent`).
- Для этого реализованы два метода:
  - `GET /order/<order_id>/create-checkout-session/` - создаёт `tripe Checkout Session` и
    возвращает `{ "id": session_id }`.
  - `GET /order/<order_id>/create-payment-intent/` - создаёт `Stripe Payment Intent` и
    возвращает `{ "client_secret": ... }`.

## Переменные окружения
Для корректной работы приложения необходимо задать следующие переменные окружения:
- `DJANGO_SECRET_KEY` - секретный ключ Django, используется для подписи сессий, CSRF и других криптографических операций.
- `DEBUG` - режим отладки (True или False).
- `ALLOWED_HOSTS` - список доменов или IP (через запятую), с которых разрешён доступ к приложению.
- `DJANGO_SUPERUSER_USERNAME` - имя суперпользователя, который будет автоматически создан.
- `DJANGO_SUPERUSER_PASSWORD` - пароль для этого суперпользователя.
- `DJANGO_SUPERUSER_EMAIL` - email суперпользователя.
- `STRIPE_SECRET_KEY` - секретный ключ Stripe (начинается на sk_test_…), необходим для серверной части операций с API.
- `STRIPE_PUBLISHABLE_KEY` - публичный ключ Stripe (начинается на pk_test_…), используется в JavaScript для инициализации Stripe.js.
- `STRIPE_USE_PAYMENT_INTENT` - флаг (True или False), определяющий, использовать ли Payment Intent (встроенная форма)
  вместо Checkout Session (редирект).
- `DATABASE_URL` - URL подключения к базе данных. Если не задана, локально приложение будет использовать SQLite (db.sqlite3).

## Публичный доступ к приложению
Приложение запущено на удалённом сервере Render.com и использует базу данных PostgreSQL.  
Ниже приведены ссылки на некоторые публичные страницы:
- Страница с информацией и оплатой заказа № 1:
  https://django-stripe-shop.onrender.com/order/1
- Страница с информацией и оплатой товара № 1:
  https://django-stripe-shop.onrender.com/item/1
  
Также была реализована админ-панель для управления моделями (Item, Discount, Tax, Order):
- Админ-панель: https://django-stripe-shop.onrender.com/admin (логин/пароль суперпользователя)

В указанных разделах полностью реализована описанная в ТЗ функциональность: просмотр деталей заказа или товара,
расчёт стоимости с учётом скидки/налога и встроенная оплата через Stripe Payment Intent
(или редирект на Stripe Checkout при выборе соответствующего режима).

## Быстрый старт (с Docker Compose)
Все команды выполняются в PowerShell (Windows).

1. Клонирование репозитория
  ```bash
  git clone https://github.com/TepidmishA/Django-stripe-shop.git
  cd Django-stripe-shop
  ```
2. Создание файла `.env` с переменными окружения
- В корне проекта уже есть файл `.env.example` - шаблон конфигурации.
- Скопируйте его в новый файл `.env`:
  ```bash
  copy .env.example .env
  ```
- Откройте `.env` и заполните значения переменных окружения.

3. Сборка и запуск через Docker Compose
  ```bash
  docker-compose up --build
  ```
При локальном запуске приложение будет доступно по адресу: http://localhost:8000/

## Быстрый старт (без Docker Compose)
Все команды выполняются в PowerShell (Windows).

1. Клонирование репозитория
  ```bash
  git clone https://github.com/TepidmishA/Django-stripe-shop.git
  cd Django-stripe-shop
  ```

2. Настройка виртуального окружения и установка зависимостей
```bash
# Create and activate a virtual environment (for Windows PowerShell)
python -m venv .venv
.venv\Scripts\activate

# Upgrade pip and install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Copy environment variables example and configure them
copy .env.example .env
```
- Откройте `.env` и заполните значения переменных окружения.

3. Применение миграций и запуск сервера
```bash
# Apply database migrations
python manage.py makemigrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Run the server
python manage.py runserver
```
При локальном запуске приложение будет доступно по адресу: http://localhost:8000/
