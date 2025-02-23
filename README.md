## Wallet Management System_V2

### Описание

Это улучшенная версия апи для взаимодействия с кошельками.

### Изменения

* Приложение переписано на ассинхронном движке
* Для миграций использован alembic
* Изменена структура приложения, произведено горизонтальное разделение слоев.

## Технические требования

### Для работы приложения необходимы:

* Python версии >= 3.7
* Alembic
* FastAPI
* Uvicorn
* SQLAlchemy
* Asyncpg
* Python-dotenv
* Pytest
* Requests

### Установка

1. Клонируйте репозиторий на локальную машину:


    git clone https://github.com/Reus1509/wallet_system_v2.git
    cd wallet_system_v2

2. Установите зависимости:


    pip install -r requirements.txt

3. Запустите приложение:


    uvicorn app.main:app


### Запуск в контейнере

    docker compose up --build -d

### Запуск тестов

Запустите тесты с помощью следующей команды:

    pytest tests/test_endpoints.py

### Разработчик:

Кузнецов Никита

    Reus1509

### Руководство по использованию

Для начала ознакомьтесь с документацией и инструкциями по установке и настройке приложения.







