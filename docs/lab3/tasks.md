# Лабораторная работа 3: Контейнеризация приложений с Docker

## Цель работы
Освоить основы контейнеризации приложений с использованием Docker, научиться создавать и запускать контейнеры с backend-сервисами

## Ход работы

## 1. Создание простого FastAPI backend-сервиса

Создаем директорию где будут находится файлы для запуска и работы сервиса.

    docker-fastapi/
        main.py
        Dockerfile
        requrements.txt
        .dockerignore
        docker-compose.yml

- FastAPI() - создает экземпляр веб-приложения
- BaseModel - используется для валидации данных
- Эндпоинты обрабатывают HTTP запросы (GET, POST)
- uvicorn - ASGI-сервер для запуска приложения

```py
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

app = FastAPI(title="Lab 3 Backend Service", version="1.0.0")

class Item(BaseModel):
    name: str
    description: str = None
    price: float
    tax: float = None

items_db = []

@app.get("/")
async def read_root():
    return {"message": "Добро пожаловать в Backend Service Lab 3!"}

@app.get("/items/")
async def read_items():
    return {"items": items_db, "count": len(items_db)}

@app.post("/items/")
async def create_item(item: Item):
    items_db.append(item.dict())
    return {"message": "Item created", "item": item}

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    if 0 <= item_id < len(items_db):
        return items_db[item_id]
    return {"error": "Item not found"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": "2024-01-01T00:00:00"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

## 2. Разработка Dockerfile для приложения

Docker - это платформа для разработки, доставки и запуска приложений в контейнерах. Контейнеры позволяют упаковать приложение со всеми его зависимостями в стандартизированный unit.

Сначала создаем файл с зависимостями requirements.txt, чтобы в контейнер были загружены необходимые библиотеки, которые требуются для работы программы.

- fastapi - веб-фреймворк для создания API
- uvicorn - сервер для запуска FastAPI приложений
- pydantic - библиотека для валидации данных

```txt
fastapi==0.104.1
uvicorn==0.24.0
pydantic==2.5.0
```

Основной файл для работы Docker следующий.

```Docker
# Используем официальный Python образ
FROM python:3.9-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файл с зависимостями
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем исходный код
COPY main.py .

# Открываем порт для FastAPI
EXPOSE 8000

# Запускаем приложение
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
```

- FROM - базовый образ для сборки
- WORKDIR - рабочая директория в контейнере
- COPY - копирование файлов с хоста в контейнер
- RUN - выполнение команд при сборке образа
- EXPOSE - указание портов для прослушивания
- CMD - команды по умолчанию при запуске контейнера

## 3. Сборка Docker образа

```bash
# Собираем образ
docker build -t lab3-fastapi .

# Просматриваем список образов
docker images
```

- docker build - собирает образ из Dockerfile
- -t lab3-fastapi - задает имя и тег образа
- . - указывает на текущую директорию с Dockerfile

![d1](../docs/images/lab3/d1.png)

Видим в списке образов и наш созданный образ с названием lab3-fastapi.

## 4. Запуск и тестирование контейнера

```bash
docker run -d -p 8000:8000 --name fastapi-container lab3-fastapi

# Просмотр запущенных контейнеров
docker ps

# Просмотр логов контейнера
docker logs fastapi-container
```
- -d - запуск в фоновом режиме (detached)
- -p 8000:8000 - проброс портов (хост:контейнер)
- --name - имя контейнера для удобства управления

Запускаем контейнер и смотрим как он работает.

![d2](../docs/images/lab3/d2.png)

![d3](../docs/images/lab3/d3.png)

![d4](../docs/images/lab3/d4.png)

## 5. Настройка портов и переменных окружения

Чтобы запускать контейнер по простой команде `docker-compose up -d` и останавливать с помощью команды `docker-compose up -d` можем создать следующий yml файл.

```yml
version: '3.8'

services:
  fastapi-app:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - .:/app
    environment:
      - ENVIRONMENT=development
    restart: unless-stopped
    container_name: lab3-fastapi-backend
```

Проверим работу

![d4](../docs/images/lab3/d5.png)