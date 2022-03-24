# Referal Application

### An application via people can subscribe to each other with their referal codes

___

## Build & Run

### requirements

* docker
* .env file in root directory with following rules:

```shell

SECRET_KEY= 
DEBUG=True

POSTGRES_ENGINE=django.db.backends.postgresql
POSTGRES_HOST=db
POSTGRES_PORT=5432

POSTGRES_USER=ref_app
POSTGRES_PASSWORD=ref_pass
POSTGRES_DB=ref_base

REDIS_HOST=redis
REDIS_PORT=6379
REDIS_DB=0
```

Use **docker-compose up --build** command to run app in docker

## Description

1. Авторизация с помощью сгенерированного 4х значного кода и номера телефона
2. Каждый пользовтелель имеет свой собственный реферальный 6и значный код
3. Профиль пользователя имеет всю необходимую информацию: собственные данные, код человека на которого сам подписан и список телефонов людей, которые непосредственно подписались сами на пользователя
4. Пользователь может посмотреть профили других людей, но с ограниченной информацией о них
5. Возможность подписаться с проверкой:
    * правильности введенного кода
    * существоания пользователя с таким кодом
    * проверки отличности кода от собственного
    * возможностью подписаться только 1 рааз

# API

* api/v1/user/login/initial/ - Ввести телефон и получить 4х значный код
* api/v1/user/login/complete/ - Отправить телефон и код и получить access- refresh- токены для авторизации
* api/v1/user/token/refresh/ - Обновить access токен благодаря отпавки refresh токена
* api/v1/profile/id{pk}/ - Получить профиль пользователя со всеми данными
* api/v1/profile/id3/subscribe/ - подписаться на пользователя с валидным инвайт кодом