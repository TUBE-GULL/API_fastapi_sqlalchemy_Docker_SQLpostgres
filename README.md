# 🚀 FastAPI + PostgreSQL + Docker Starter

Проект представляет собой базовую архитектуру для создания REST API с использованием FastAPI, SQLAlchemy, Alembic и PostgreSQL, обёрнутый в Docker.

---

<h1 align="center">🚀 FastAPI + PostgreSQL + Docker Starter + Alembic + Pytest</h1>

<h2 align="center">Used Libraries</h2>
<div align="center">

<a href="https://www.python.org" target="_blank" rel="noreferrer" style="display: inline-block;"> 
  <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" alt="python" width="60" height="60"/>
</a>

<a href="https://fastapi.tiangolo.com/" target="FastAPI" rel="noreferrer"> 
    <img src="https://avatars.githubusercontent.com/u/156354296?s=200&v=4" alt="FastAPI" width="60" height="60"/> 
</a>

<a href="https://www.postgresql.org/" target="Рostgresql" rel="noreferrer"> 
    <img src="https://www.postgresql.org/media/img/about/press/elephant.png" alt="postgresql" width="60" height="60"/> 
</a>

<a href="https://www.docker.com/" target="Docker" rel="noreferrer"> 
    <img src="https://avatars.githubusercontent.com/u/5429470?s=200&v=4" alt="Docker" width="60" height="60"/> 
</a>

<a href="https://github.com/sqlalchemy" target="sqlalchemy" rel="noreferrer"> 
    <img src="https://avatars.githubusercontent.com/u/6043126?s=200&v=4" alt="sqlalchemy" width="60" height="60"/> 
</a>

<a href="https://github.com/sqlalchemy/alembic" target="alembic" rel="noreferrer"> 
    <img src="https://avatars.githubusercontent.com/u/6043126?s=200&v=4" alt="alembic" width="60" height="60"/> 
</a>

<a href="pytest" target="pytest" rel="noreferrer"> 
    <img src="https://docs.pytest.org/en/stable/_static/pytest1.png" alt="pytest" width="60" height="60"/> 
</a>

</div>

### 🗃️ Структура проекта
```bash
my_api_project/
├── app/
│   ├── main.py             # Точка входа
│   ├── models/             # SQLAlchemy модели
│   ├── schemas/            # Pydantic схемы
│   ├── routers/            # FastAPI роутеры
│   ├── services/           # Логика приложения
│   ├── database.py         # Подключение к БД
│   ├── migrations/         # Миграции Alembic
│   └── config.py           # Конфигурация
│
├── tests/                  # Тесты
├── .env                    # Переменные окружения
├── .gitignore              # файлы для игнорирования git 
├── Dockerfile              # Docker-образ приложения
├── docker-compose.yml      # docker-compose конфигурация
├── requirements.txt        # Зависимости
└── README.md               # Документация проекта


## 📦 Установка и запуск
docker compose up --build


### ⚙️ Переменные окружения
DB_HOST=db
DB_PORT=5432
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=password


### Тестирование

docker compose exec api pytest


### 1. Клонируй проект и перейди в папку

```bash
git clone <repo-url>
cd MY_API
