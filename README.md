# 🚀 FastAPI + PostgreSQL + Docker Starter

Проект представляет собой базовую архитектуру для создания REST API с использованием FastAPI, SQLAlchemy, Alembic и PostgreSQL, обёрнутый в Docker.

---

## 🧱 Технологии

- [FastAPI](https://fastapi.tiangolo.com/) — высокопроизводительный веб-фреймворк
- [PostgreSQL](https://www.postgresql.org/) — реляционная СУБД
- [SQLAlchemy](https://www.sqlalchemy.org/) — ORM для работы с БД
- [Alembic](https://alembic.sqlalchemy.org/) — миграции БД
- [Docker](https://www.docker.com/) — контейнеризация
- [docker-compose](https://docs.docker.com/compose/) — оркестрация сервисов
- [pytest](https://docs.pytest.org/) — фреймворк для тестирования

---


### 🗃️ Структура проекта

my_api_project/
├── app/
│   ├── main.py             # Точка входа
│   ├── models/             # SQLAlchemy модели
│   ├── schemas/            # Pydantic схемы
│   ├── routers/            # FastAPI роутеры
│   ├── services/           # Логика приложения
│   ├── database.py         # Подключение к БД
│   └── config.py           # Конфигурация
│
├── alembic/                # Миграции Alembic
├── tests/                  # Тесты
├── .env                    # Переменные окружения
├── Dockerfile              # Docker-образ приложения
├── docker-compose.yml      # docker-compose конфигурация
├── requirements.txt        # Зависимости
└── README.md               # Документация проекта


## 📦 Установка и запуск
docker compose up --build


### ⚙️ Переменные окружения
DB_HOST=db
DB_PORT=5432
DB_NAME=mydb
DB_USER=user
DB_PASSWORD=password


### Тестирование

docker compose exec api pytest


### 1. Клонируй проект и перейди в папку

```bash
git clone <repo-url>
cd my_api_project
