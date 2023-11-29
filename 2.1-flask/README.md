# Домашнее задание к лекции «Flask»

## Документация по учебному проекту

Для запуска проекта необходимо:

- Установить зависимости:
```bash
pip install -r requirements.txt
```
- Создать и активировать виртуальное окружение в папке проекта `./env`
- Определить переменные окружения `???` в директории ```env/.env```:

  - POSTGRES_USER= `???`
  - POSTGRES_PASSWORD= `???`
  - POSTGRES_DB= `???`
  - PG_DSN= `???`
  - PGADMIN_DEFAULT_EMAIL=admin@yandex.ru
  - PGADMIN_DEFAULT_PASSWORD=admin1
  - PGADMIN_CONFIG_SERVER_MODE=False
  - TOKEN_TTL=86400


- Cоздать базу данных и подключения к PgAdmin для отображения
таблиц:
```bash
docker-compose up -d
```

- Запустить модуль локального [сервера](./server.py)

- Открыть PgAdmin по адресу http://localhost:5050/ и создать сервер

- Тестовые запросы в модуле [client.py](./client.py)