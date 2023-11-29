# Домашнее задание к лекции «Aiohttp»

## Документация по учебному проекту

Для запуска проекта необходимо:

- Установить зависимости:
```bash
pip install -r requirements.txt
```
- Создать и активировать виртуальное окружение в папке проекта `./env`
- Определить переменные окружения `???` в файле ```.env``` корневой папки проекта:

  - PG_USER=???
  - PG_PASSWORD=???
  - PG_DB=???
  - PGADMIN_DEFAULT_EMAIL=admin@yandex.ru
  - PGADMIN_DEFAULT_PASSWORD=admin1
  - PGADMIN_CONFIG_SERVER_MODE=False


- Cоздать базу данных и подключениe к PgAdmin для отображения
таблиц:
```bash
docker-compose up -d
```

- Запустить модуль [app.py](./app.py)

- Открыть PgAdmin по адресу http://localhost:5050/ и создать новый сервер

- Тестовые запросы в модуле [client.py](./client.py)