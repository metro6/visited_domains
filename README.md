visited_links project
--
#Инструкция для старта проекта:

```
git clone https://github.com/metro6/visited_domains.git
cd visited_domains
```
Создайте файл с настройками
```
touch src/custom_settings/custom_settings.py
nano src/custom_settings/custom_settings.py
```
Скопируйте эти настройки подключения к redis, postgres, smtp
```
#DATABASE CONFIGURATION
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'postgres',
        'USER': 'postgres',
        'HOST': 'postgres',
        'PORT': 5432,
    }
}

#REDIS CONFIGURATION
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://redis:6379/',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

#YOUR SMTP SERVER CONFIG
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'your_login'
EMAIL_HOST_PASSWORD = 'your_password'
EMAIL_PORT = 587
#END CONFIGURATION SMTP SERVER

```
Соберите и запустите проект:
```
(sudo) make build
(sudo) make up
```
Остановка проекта
```
(sudo) make down
```

После загрузки проект будет доступен по адресу localhost:8001
Соответственно ендпоинты для загрузок/выгрузок ссылок будут выглядеть так:
- localhost:8001/visited_links
- localhost:8001/visited_domains?from=154522123&to=1545217638000
#В проекте используются следующие технологии
- docker-compose*
- nginx*
- gunicorn*
- django
- postgresql**
- redis
Отмеченные * пункты могут не использоваться, но они значительно упрощают разворачивание проекта

postgres** ипользуется для долговременного хранения данных.

---
#Вы можете пользоваться и стандартными командами docker-compose
```bash
(sudo) docker-compose build
(sudo) docker-compose up
(sudo) docker-compose down
```