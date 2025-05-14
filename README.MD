# **_UrRent_**
Сервис для бронирования помещений.  

Стек: Python, FastAPI, SQLalchemy, aiosqlite, Pydantic  

**Как запустить проект:**
-----------
Клонировать репозиторий и перейти в него в командной строке:

```bash
git clone https://github.com/TatianaSharova/urRent.git
```

Создать и активировать виртуальное окружение:
```bash
poetry install
poetry env activate
source .venv/Scripts/activate
```

**Документация:**  
-----------
Документацию к API после запуска проекта можно посмотреть по адресам:
```
http://127.0.0.1:8000/docs
http://127.0.0.1:8000/redoc
```

## Pre-commit
Этот проект использует [pre-commit](https://pre-commit.com/) для автоматического запуска линтеров перед коммитом.

### Настройка pre-commit
Установи хуки:

```bash
poetry run pre-commit install
```

### Ручной запуск

Проверить все файлы вручную:
```bash
pre-commit run --all-files
```
Проверить конкретный файл:
```bash
pre-commit run --files path/to/file.py
```

### Автор
[Татьяна Шарова](https://github.com/TatianaSharova)
